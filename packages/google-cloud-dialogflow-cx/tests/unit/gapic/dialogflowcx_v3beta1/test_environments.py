# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

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
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.dialogflowcx_v3beta1.services.environments import (
    EnvironmentsAsyncClient,
    EnvironmentsClient,
    pagers,
    transports,
)
from google.cloud.dialogflowcx_v3beta1.types import environment as gcdc_environment
from google.cloud.dialogflowcx_v3beta1.types import environment
from google.cloud.dialogflowcx_v3beta1.types import webhook


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert EnvironmentsClient._get_default_mtls_endpoint(None) is None
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        EnvironmentsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert EnvironmentsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert EnvironmentsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert EnvironmentsClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert EnvironmentsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            EnvironmentsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert EnvironmentsClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert EnvironmentsClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert EnvironmentsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            EnvironmentsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert EnvironmentsClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert EnvironmentsClient._get_client_cert_source(None, False) is None
    assert (
        EnvironmentsClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        EnvironmentsClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                EnvironmentsClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                EnvironmentsClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    EnvironmentsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsClient),
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = EnvironmentsClient._DEFAULT_UNIVERSE
    default_endpoint = EnvironmentsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = EnvironmentsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        EnvironmentsClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        EnvironmentsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == EnvironmentsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EnvironmentsClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        EnvironmentsClient._get_api_endpoint(None, None, default_universe, "always")
        == EnvironmentsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EnvironmentsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == EnvironmentsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EnvironmentsClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        EnvironmentsClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        EnvironmentsClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        EnvironmentsClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        EnvironmentsClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        EnvironmentsClient._get_universe_domain(None, None)
        == EnvironmentsClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        EnvironmentsClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (EnvironmentsClient, "grpc"),
        (EnvironmentsAsyncClient, "grpc_asyncio"),
        (EnvironmentsClient, "rest"),
    ],
)
def test_environments_client_from_service_account_info(client_class, transport_name):
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
            "dialogflow.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dialogflow.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.EnvironmentsGrpcTransport, "grpc"),
        (transports.EnvironmentsGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.EnvironmentsRestTransport, "rest"),
    ],
)
def test_environments_client_service_account_always_use_jwt(
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
        (EnvironmentsClient, "grpc"),
        (EnvironmentsAsyncClient, "grpc_asyncio"),
        (EnvironmentsClient, "rest"),
    ],
)
def test_environments_client_from_service_account_file(client_class, transport_name):
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
            "dialogflow.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dialogflow.googleapis.com"
        )


def test_environments_client_get_transport_class():
    transport = EnvironmentsClient.get_transport_class()
    available_transports = [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsRestTransport,
    ]
    assert transport in available_transports

    transport = EnvironmentsClient.get_transport_class("grpc")
    assert transport == transports.EnvironmentsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest"),
    ],
)
@mock.patch.object(
    EnvironmentsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsClient),
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsAsyncClient),
)
def test_environments_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(EnvironmentsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(EnvironmentsClient, "get_transport_class") as gtc:
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
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
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
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc", "true"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc", "false"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", "true"),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    EnvironmentsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsClient),
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_environments_client_mtls_env_auto(
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
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
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
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
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
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [EnvironmentsClient, EnvironmentsAsyncClient])
@mock.patch.object(
    EnvironmentsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EnvironmentsClient)
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EnvironmentsAsyncClient),
)
def test_environments_client_get_mtls_endpoint_and_cert_source(client_class):
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

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize("client_class", [EnvironmentsClient, EnvironmentsAsyncClient])
@mock.patch.object(
    EnvironmentsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsClient),
)
@mock.patch.object(
    EnvironmentsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EnvironmentsAsyncClient),
)
def test_environments_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = EnvironmentsClient._DEFAULT_UNIVERSE
    default_endpoint = EnvironmentsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = EnvironmentsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport, "grpc"),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest"),
    ],
)
def test_environments_client_client_options_scopes(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            EnvironmentsClient,
            transports.EnvironmentsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (EnvironmentsClient, transports.EnvironmentsRestTransport, "rest", None),
    ],
)
def test_environments_client_client_options_credentials_file(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_environments_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.environments.transports.EnvironmentsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = EnvironmentsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
            EnvironmentsClient,
            transports.EnvironmentsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EnvironmentsAsyncClient,
            transports.EnvironmentsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_environments_client_create_channel_credentials_file(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            "dialogflow.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=None,
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environment.ListEnvironmentsRequest,
        dict,
    ],
)
def test_list_environments(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListEnvironmentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.ListEnvironmentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_environments_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.ListEnvironmentsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_environments(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.ListEnvironmentsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_environments_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_environments in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_environments
        ] = mock_rpc
        request = {}
        client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_environments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_environments_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_environments
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_environments
        ] = mock_rpc

        request = {}
        await client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_environments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_environments_async(
    transport: str = "grpc_asyncio", request_type=environment.ListEnvironmentsRequest
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListEnvironmentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.ListEnvironmentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_environments_async_from_dict():
    await test_list_environments_async(request_type=dict)


def test_list_environments_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = environment.ListEnvironmentsResponse()
        client.list_environments(request)

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
async def test_list_environments_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListEnvironmentsResponse()
        )
        await client.list_environments(request)

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


def test_list_environments_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListEnvironmentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_environments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_environments_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_environments(
            environment.ListEnvironmentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_environments_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListEnvironmentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListEnvironmentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_environments(
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
async def test_list_environments_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_environments(
            environment.ListEnvironmentsRequest(),
            parent="parent_value",
        )


def test_list_environments_pager(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_environments(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.Environment) for i in results)


def test_list_environments_pages(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_environments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_environments_async_pager():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_environments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, environment.Environment) for i in responses)


@pytest.mark.asyncio
async def test_list_environments_async_pages():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_environments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        environment.GetEnvironmentRequest,
        dict,
    ],
)
def test_get_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.Environment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.GetEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, environment.Environment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_environment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.GetEnvironmentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_environment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.GetEnvironmentRequest(
            name="name_value",
        )


def test_get_environment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_environment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_environment] = mock_rpc
        request = {}
        client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_environment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_environment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_environment
        ] = mock_rpc

        request = {}
        await client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_environment_async(
    transport: str = "grpc_asyncio", request_type=environment.GetEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.Environment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.GetEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, environment.Environment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_environment_async_from_dict():
    await test_get_environment_async(request_type=dict)


def test_get_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = environment.Environment()
        client.get_environment(request)

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
async def test_get_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.Environment()
        )
        await client.get_environment(request)

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


def test_get_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.Environment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_environment(
            environment.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.Environment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.Environment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_environment(
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
async def test_get_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_environment(
            environment.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_environment.CreateEnvironmentRequest,
        dict,
    ],
)
def test_create_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcdc_environment.CreateEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_environment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcdc_environment.CreateEnvironmentRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_environment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_environment.CreateEnvironmentRequest(
            parent="parent_value",
        )


def test_create_environment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_environment
        ] = mock_rpc
        request = {}
        client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_environment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_environment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_environment
        ] = mock_rpc

        request = {}
        await client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_environment_async(
    transport: str = "grpc_asyncio",
    request_type=gcdc_environment.CreateEnvironmentRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcdc_environment.CreateEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_environment_async_from_dict():
    await test_create_environment_async(request_type=dict)


def test_create_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_environment.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_environment(request)

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
async def test_create_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_environment.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_environment(request)

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


def test_create_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_environment(
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = gcdc_environment.Environment(name="name_value")
        assert arg == mock_val


def test_create_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_environment(
            gcdc_environment.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_environment(
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = gcdc_environment.Environment(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_environment(
            gcdc_environment.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_environment.UpdateEnvironmentRequest,
        dict,
    ],
)
def test_update_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gcdc_environment.UpdateEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_environment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gcdc_environment.UpdateEnvironmentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_environment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcdc_environment.UpdateEnvironmentRequest()


def test_update_environment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_environment
        ] = mock_rpc
        request = {}
        client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_environment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_environment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_environment
        ] = mock_rpc

        request = {}
        await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_environment_async(
    transport: str = "grpc_asyncio",
    request_type=gcdc_environment.UpdateEnvironmentRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gcdc_environment.UpdateEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_environment_async_from_dict():
    await test_update_environment_async(request_type=dict)


def test_update_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_environment.UpdateEnvironmentRequest()

    request.environment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcdc_environment.UpdateEnvironmentRequest()

    request.environment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment.name=name_value",
    ) in kw["metadata"]


def test_update_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_environment(
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].environment
        mock_val = gcdc_environment.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_environment(
            gcdc_environment.UpdateEnvironmentRequest(),
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_environment(
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].environment
        mock_val = gcdc_environment.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_environment(
            gcdc_environment.UpdateEnvironmentRequest(),
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environment.DeleteEnvironmentRequest,
        dict,
    ],
)
def test_delete_environment(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.DeleteEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_environment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.DeleteEnvironmentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_environment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.DeleteEnvironmentRequest(
            name="name_value",
        )


def test_delete_environment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_environment
        ] = mock_rpc
        request = {}
        client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_environment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_environment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_environment
        ] = mock_rpc

        request = {}
        await client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_environment_async(
    transport: str = "grpc_asyncio", request_type=environment.DeleteEnvironmentRequest
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.DeleteEnvironmentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_environment_async_from_dict():
    await test_delete_environment_async(request_type=dict)


def test_delete_environment_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = None
        client.delete_environment(request)

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
async def test_delete_environment_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_environment(request)

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


def test_delete_environment_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_environment_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_environment(
            environment.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_environment_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_environment(
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
async def test_delete_environment_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_environment(
            environment.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        environment.LookupEnvironmentHistoryRequest,
        dict,
    ],
)
def test_lookup_environment_history(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.LookupEnvironmentHistoryResponse(
            next_page_token="next_page_token_value",
        )
        response = client.lookup_environment_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.LookupEnvironmentHistoryRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.LookupEnvironmentHistoryPager)
    assert response.next_page_token == "next_page_token_value"


def test_lookup_environment_history_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.LookupEnvironmentHistoryRequest(
        name="name_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.lookup_environment_history(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.LookupEnvironmentHistoryRequest(
            name="name_value",
            page_token="page_token_value",
        )


def test_lookup_environment_history_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.lookup_environment_history
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.lookup_environment_history
        ] = mock_rpc
        request = {}
        client.lookup_environment_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.lookup_environment_history(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_lookup_environment_history_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.lookup_environment_history
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.lookup_environment_history
        ] = mock_rpc

        request = {}
        await client.lookup_environment_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.lookup_environment_history(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_lookup_environment_history_async(
    transport: str = "grpc_asyncio",
    request_type=environment.LookupEnvironmentHistoryRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.LookupEnvironmentHistoryResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.lookup_environment_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.LookupEnvironmentHistoryRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.LookupEnvironmentHistoryAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_lookup_environment_history_async_from_dict():
    await test_lookup_environment_history_async(request_type=dict)


def test_lookup_environment_history_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.LookupEnvironmentHistoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        call.return_value = environment.LookupEnvironmentHistoryResponse()
        client.lookup_environment_history(request)

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
async def test_lookup_environment_history_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.LookupEnvironmentHistoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.LookupEnvironmentHistoryResponse()
        )
        await client.lookup_environment_history(request)

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


def test_lookup_environment_history_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.LookupEnvironmentHistoryResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.lookup_environment_history(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_lookup_environment_history_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.lookup_environment_history(
            environment.LookupEnvironmentHistoryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_lookup_environment_history_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.LookupEnvironmentHistoryResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.LookupEnvironmentHistoryResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.lookup_environment_history(
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
async def test_lookup_environment_history_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.lookup_environment_history(
            environment.LookupEnvironmentHistoryRequest(),
            name="name_value",
        )


def test_lookup_environment_history_pager(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.lookup_environment_history(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.Environment) for i in results)


def test_lookup_environment_history_pages(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.lookup_environment_history(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_lookup_environment_history_async_pager():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.lookup_environment_history(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, environment.Environment) for i in responses)


@pytest.mark.asyncio
async def test_lookup_environment_history_async_pages():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.lookup_environment_history(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        environment.RunContinuousTestRequest,
        dict,
    ],
)
def test_run_continuous_test(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.RunContinuousTestRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_continuous_test_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.RunContinuousTestRequest(
        environment="environment_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_continuous_test(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.RunContinuousTestRequest(
            environment="environment_value",
        )


def test_run_continuous_test_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.run_continuous_test in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_continuous_test
        ] = mock_rpc
        request = {}
        client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.run_continuous_test(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_continuous_test_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.run_continuous_test
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.run_continuous_test
        ] = mock_rpc

        request = {}
        await client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.run_continuous_test(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_continuous_test_async(
    transport: str = "grpc_asyncio", request_type=environment.RunContinuousTestRequest
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.RunContinuousTestRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_continuous_test_async_from_dict():
    await test_run_continuous_test_async(request_type=dict)


def test_run_continuous_test_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.RunContinuousTestRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_continuous_test_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.RunContinuousTestRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        environment.ListContinuousTestResultsRequest,
        dict,
    ],
)
def test_list_continuous_test_results(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListContinuousTestResultsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_continuous_test_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.ListContinuousTestResultsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListContinuousTestResultsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_continuous_test_results_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.ListContinuousTestResultsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_continuous_test_results(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.ListContinuousTestResultsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_continuous_test_results_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_continuous_test_results
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_continuous_test_results
        ] = mock_rpc
        request = {}
        client.list_continuous_test_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_continuous_test_results(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_continuous_test_results_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_continuous_test_results
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_continuous_test_results
        ] = mock_rpc

        request = {}
        await client.list_continuous_test_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_continuous_test_results(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_continuous_test_results_async(
    transport: str = "grpc_asyncio",
    request_type=environment.ListContinuousTestResultsRequest,
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListContinuousTestResultsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_continuous_test_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.ListContinuousTestResultsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListContinuousTestResultsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_continuous_test_results_async_from_dict():
    await test_list_continuous_test_results_async(request_type=dict)


def test_list_continuous_test_results_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.ListContinuousTestResultsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        call.return_value = environment.ListContinuousTestResultsResponse()
        client.list_continuous_test_results(request)

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
async def test_list_continuous_test_results_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.ListContinuousTestResultsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListContinuousTestResultsResponse()
        )
        await client.list_continuous_test_results(request)

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


def test_list_continuous_test_results_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListContinuousTestResultsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_continuous_test_results(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_continuous_test_results_flattened_error():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_continuous_test_results(
            environment.ListContinuousTestResultsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_continuous_test_results_flattened_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = environment.ListContinuousTestResultsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListContinuousTestResultsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_continuous_test_results(
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
async def test_list_continuous_test_results_flattened_error_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_continuous_test_results(
            environment.ListContinuousTestResultsRequest(),
            parent="parent_value",
        )


def test_list_continuous_test_results_pager(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
                next_page_token="abc",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[],
                next_page_token="def",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                ],
                next_page_token="ghi",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_continuous_test_results(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.ContinuousTestResult) for i in results)


def test_list_continuous_test_results_pages(transport_name: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
                next_page_token="abc",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[],
                next_page_token="def",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                ],
                next_page_token="ghi",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_continuous_test_results(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_continuous_test_results_async_pager():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
                next_page_token="abc",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[],
                next_page_token="def",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                ],
                next_page_token="ghi",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_continuous_test_results(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, environment.ContinuousTestResult) for i in responses)


@pytest.mark.asyncio
async def test_list_continuous_test_results_async_pages():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
                next_page_token="abc",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[],
                next_page_token="def",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                ],
                next_page_token="ghi",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_continuous_test_results(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        environment.DeployFlowRequest,
        dict,
    ],
)
def test_deploy_flow(request_type, transport: str = "grpc"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = environment.DeployFlowRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_deploy_flow_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = environment.DeployFlowRequest(
        environment="environment_value",
        flow_version="flow_version_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.deploy_flow(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == environment.DeployFlowRequest(
            environment="environment_value",
            flow_version="flow_version_value",
        )


def test_deploy_flow_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.deploy_flow in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.deploy_flow] = mock_rpc
        request = {}
        client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.deploy_flow(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_deploy_flow_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EnvironmentsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.deploy_flow
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.deploy_flow
        ] = mock_rpc

        request = {}
        await client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.deploy_flow(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_deploy_flow_async(
    transport: str = "grpc_asyncio", request_type=environment.DeployFlowRequest
):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = environment.DeployFlowRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_deploy_flow_async_from_dict():
    await test_deploy_flow_async(request_type=dict)


def test_deploy_flow_field_headers():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.DeployFlowRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_deploy_flow_field_headers_async():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = environment.DeployFlowRequest()

    request.environment = "environment_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment=environment_value",
    ) in kw["metadata"]


def test_list_environments_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_environments in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_environments
        ] = mock_rpc

        request = {}
        client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_environments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_environments_rest_required_fields(
    request_type=environment.ListEnvironmentsRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_environments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_environments._get_unset_required_fields(jsonified_request)
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

    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = environment.ListEnvironmentsResponse()
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
            return_value = environment.ListEnvironmentsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_environments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_environments_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_environments._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_environments_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.ListEnvironmentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = environment.ListEnvironmentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_environments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*}/environments"
            % client.transport._host,
            args[1],
        )


def test_list_environments_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_environments(
            environment.ListEnvironmentsRequest(),
            parent="parent_value",
        )


def test_list_environments_rest_pager(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.ListEnvironmentsResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            environment.ListEnvironmentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        pager = client.list_environments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.Environment) for i in results)

        pages = list(client.list_environments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_environment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_environment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_environment] = mock_rpc

        request = {}
        client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_environment_rest_required_fields(
    request_type=environment.GetEnvironmentRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = environment.Environment()
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
            return_value = environment.Environment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_environment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_environment_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_environment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.Environment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
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
        return_value = environment.Environment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_environment(
            environment.GetEnvironmentRequest(),
            name="name_value",
        )


def test_create_environment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_environment
        ] = mock_rpc

        request = {}
        client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_environment_rest_required_fields(
    request_type=gcdc_environment.CreateEnvironmentRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = EnvironmentsClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_environment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_environment_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_environment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "environment",
            )
        )
    )


def test_create_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2/agents/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*}/environments"
            % client.transport._host,
            args[1],
        )


def test_create_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_environment(
            gcdc_environment.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=gcdc_environment.Environment(name="name_value"),
        )


def test_update_environment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_environment
        ] = mock_rpc

        request = {}
        client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_environment_rest_required_fields(
    request_type=gcdc_environment.UpdateEnvironmentRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_environment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = EnvironmentsClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_environment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_environment_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_environment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "environment",
                "updateMask",
            )
        )
    )


def test_update_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "environment": {
                "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{environment.name=projects/*/locations/*/agents/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_environment(
            gcdc_environment.UpdateEnvironmentRequest(),
            environment=gcdc_environment.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_environment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_environment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_environment
        ] = mock_rpc

        request = {}
        client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_environment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_environment_rest_required_fields(
    request_type=environment.DeleteEnvironmentRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_environment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EnvironmentsClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_environment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_environment_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_environment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_delete_environment_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_environment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/environments/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_environment_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_environment(
            environment.DeleteEnvironmentRequest(),
            name="name_value",
        )


def test_lookup_environment_history_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.lookup_environment_history
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.lookup_environment_history
        ] = mock_rpc

        request = {}
        client.lookup_environment_history(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.lookup_environment_history(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_lookup_environment_history_rest_required_fields(
    request_type=environment.LookupEnvironmentHistoryRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).lookup_environment_history._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).lookup_environment_history._get_unset_required_fields(jsonified_request)
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

    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = environment.LookupEnvironmentHistoryResponse()
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
            return_value = environment.LookupEnvironmentHistoryResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.lookup_environment_history(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_lookup_environment_history_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.lookup_environment_history._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


def test_lookup_environment_history_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.LookupEnvironmentHistoryResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
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
        return_value = environment.LookupEnvironmentHistoryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.lookup_environment_history(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{name=projects/*/locations/*/agents/*/environments/*}:lookupEnvironmentHistory"
            % client.transport._host,
            args[1],
        )


def test_lookup_environment_history_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.lookup_environment_history(
            environment.LookupEnvironmentHistoryRequest(),
            name="name_value",
        )


def test_lookup_environment_history_rest_pager(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                    environment.Environment(),
                ],
                next_page_token="abc",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[],
                next_page_token="def",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                ],
                next_page_token="ghi",
            ),
            environment.LookupEnvironmentHistoryResponse(
                environments=[
                    environment.Environment(),
                    environment.Environment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            environment.LookupEnvironmentHistoryResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
        }

        pager = client.lookup_environment_history(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.Environment) for i in results)

        pages = list(client.lookup_environment_history(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_run_continuous_test_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.run_continuous_test in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_continuous_test
        ] = mock_rpc

        request = {}
        client.run_continuous_test(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.run_continuous_test(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_run_continuous_test_rest_required_fields(
    request_type=environment.RunContinuousTestRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["environment"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).run_continuous_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["environment"] = "environment_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).run_continuous_test._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "environment" in jsonified_request
    assert jsonified_request["environment"] == "environment_value"

    client = EnvironmentsClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.run_continuous_test(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_run_continuous_test_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.run_continuous_test._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("environment",)))


def test_list_continuous_test_results_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_continuous_test_results
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_continuous_test_results
        ] = mock_rpc

        request = {}
        client.list_continuous_test_results(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_continuous_test_results(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_continuous_test_results_rest_required_fields(
    request_type=environment.ListContinuousTestResultsRequest,
):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_continuous_test_results._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_continuous_test_results._get_unset_required_fields(jsonified_request)
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

    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = environment.ListContinuousTestResultsResponse()
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
            return_value = environment.ListContinuousTestResultsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_continuous_test_results(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_continuous_test_results_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_continuous_test_results._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_continuous_test_results_rest_flattened():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.ListContinuousTestResultsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
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
        return_value = environment.ListContinuousTestResultsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_continuous_test_results(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v3beta1/{parent=projects/*/locations/*/agents/*/environments/*}/continuousTestResults"
            % client.transport._host,
            args[1],
        )


def test_list_continuous_test_results_rest_flattened_error(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_continuous_test_results(
            environment.ListContinuousTestResultsRequest(),
            parent="parent_value",
        )


def test_list_continuous_test_results_rest_pager(transport: str = "rest"):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
                next_page_token="abc",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[],
                next_page_token="def",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                ],
                next_page_token="ghi",
            ),
            environment.ListContinuousTestResultsResponse(
                continuous_test_results=[
                    environment.ContinuousTestResult(),
                    environment.ContinuousTestResult(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            environment.ListContinuousTestResultsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
        }

        pager = client.list_continuous_test_results(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, environment.ContinuousTestResult) for i in results)

        pages = list(client.list_continuous_test_results(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_deploy_flow_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.deploy_flow in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.deploy_flow] = mock_rpc

        request = {}
        client.deploy_flow(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.deploy_flow(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_deploy_flow_rest_required_fields(request_type=environment.DeployFlowRequest):
    transport_class = transports.EnvironmentsRestTransport

    request_init = {}
    request_init["environment"] = ""
    request_init["flow_version"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).deploy_flow._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["environment"] = "environment_value"
    jsonified_request["flowVersion"] = "flow_version_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).deploy_flow._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "environment" in jsonified_request
    assert jsonified_request["environment"] == "environment_value"
    assert "flowVersion" in jsonified_request
    assert jsonified_request["flowVersion"] == "flow_version_value"

    client = EnvironmentsClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.deploy_flow(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_deploy_flow_rest_unset_required_fields():
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.deploy_flow._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "environment",
                "flowVersion",
            )
        )
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EnvironmentsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = EnvironmentsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EnvironmentsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.EnvironmentsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
        transports.EnvironmentsRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = EnvironmentsClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_environments_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = environment.ListEnvironmentsResponse()
        client.list_environments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListEnvironmentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_environment_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = environment.Environment()
        client.get_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.GetEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_environment_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.CreateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_environment_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.UpdateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_environment_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = None
        client.delete_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeleteEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_lookup_environment_history_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        call.return_value = environment.LookupEnvironmentHistoryResponse()
        client.lookup_environment_history(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.LookupEnvironmentHistoryRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_run_continuous_test_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_continuous_test(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.RunContinuousTestRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_continuous_test_results_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        call.return_value = environment.ListContinuousTestResultsResponse()
        client.list_continuous_test_results(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListContinuousTestResultsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_deploy_flow_empty_call_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.deploy_flow(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeployFlowRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = EnvironmentsAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_environments_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListEnvironmentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_environments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListEnvironmentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_environment_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.Environment(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        await client.get_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.GetEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_environment_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.CreateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_environment_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.update_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.UpdateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_environment_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeleteEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_lookup_environment_history_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.LookupEnvironmentHistoryResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.lookup_environment_history(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.LookupEnvironmentHistoryRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_run_continuous_test_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.run_continuous_test(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.RunContinuousTestRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_continuous_test_results_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            environment.ListContinuousTestResultsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_continuous_test_results(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListContinuousTestResultsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_deploy_flow_empty_call_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.deploy_flow(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeployFlowRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = EnvironmentsClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_list_environments_rest_bad_request(
    request_type=environment.ListEnvironmentsRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_environments(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.ListEnvironmentsRequest,
        dict,
    ],
)
def test_list_environments_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.ListEnvironmentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = environment.ListEnvironmentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_environments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_environments_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_list_environments"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_list_environments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.ListEnvironmentsRequest.pb(
            environment.ListEnvironmentsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = environment.ListEnvironmentsResponse.to_json(
            environment.ListEnvironmentsResponse()
        )
        req.return_value.content = return_value

        request = environment.ListEnvironmentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environment.ListEnvironmentsResponse()

        client.list_environments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_environment_rest_bad_request(
    request_type=environment.GetEnvironmentRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_environment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.GetEnvironmentRequest,
        dict,
    ],
)
def test_get_environment_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.Environment(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = environment.Environment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_environment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, environment.Environment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_get_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_get_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.GetEnvironmentRequest.pb(
            environment.GetEnvironmentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = environment.Environment.to_json(environment.Environment())
        req.return_value.content = return_value

        request = environment.GetEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environment.Environment()

        client.get_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_environment_rest_bad_request(
    request_type=gcdc_environment.CreateEnvironmentRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_environment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_environment.CreateEnvironmentRequest,
        dict,
    ],
)
def test_create_environment_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/agents/sample3"}
    request_init["environment"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_configs": [{"version": "version_value"}],
        "update_time": {"seconds": 751, "nanos": 543},
        "test_cases_config": {
            "test_cases": ["test_cases_value1", "test_cases_value2"],
            "enable_continuous_run": True,
            "enable_predeployment_run": True,
        },
        "webhook_config": {
            "webhook_overrides": [
                {
                    "name": "name_value",
                    "display_name": "display_name_value",
                    "generic_web_service": {
                        "uri": "uri_value",
                        "username": "username_value",
                        "password": "password_value",
                        "request_headers": {},
                        "allowed_ca_certs": [
                            b"allowed_ca_certs_blob1",
                            b"allowed_ca_certs_blob2",
                        ],
                        "oauth_config": {
                            "client_id": "client_id_value",
                            "client_secret": "client_secret_value",
                            "token_endpoint": "token_endpoint_value",
                            "scopes": ["scopes_value1", "scopes_value2"],
                        },
                        "service_agent_auth": 1,
                        "webhook_type": 1,
                        "http_method": 1,
                        "request_body": "request_body_value",
                        "parameter_mapping": {},
                    },
                    "service_directory": {
                        "service": "service_value",
                        "generic_web_service": {},
                    },
                    "timeout": {"seconds": 751, "nanos": 543},
                    "disabled": True,
                }
            ]
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcdc_environment.CreateEnvironmentRequest.meta.fields["environment"]

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
    for field, value in request_init["environment"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["environment"][field])):
                    del request_init["environment"][field][i][subfield]
            else:
                del request_init["environment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_environment(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_create_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_create_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcdc_environment.CreateEnvironmentRequest.pb(
            gcdc_environment.CreateEnvironmentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = gcdc_environment.CreateEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_environment_rest_bad_request(
    request_type=gcdc_environment.UpdateEnvironmentRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "environment": {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.update_environment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gcdc_environment.UpdateEnvironmentRequest,
        dict,
    ],
)
def test_update_environment_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": {
            "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
        }
    }
    request_init["environment"] = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_configs": [{"version": "version_value"}],
        "update_time": {"seconds": 751, "nanos": 543},
        "test_cases_config": {
            "test_cases": ["test_cases_value1", "test_cases_value2"],
            "enable_continuous_run": True,
            "enable_predeployment_run": True,
        },
        "webhook_config": {
            "webhook_overrides": [
                {
                    "name": "name_value",
                    "display_name": "display_name_value",
                    "generic_web_service": {
                        "uri": "uri_value",
                        "username": "username_value",
                        "password": "password_value",
                        "request_headers": {},
                        "allowed_ca_certs": [
                            b"allowed_ca_certs_blob1",
                            b"allowed_ca_certs_blob2",
                        ],
                        "oauth_config": {
                            "client_id": "client_id_value",
                            "client_secret": "client_secret_value",
                            "token_endpoint": "token_endpoint_value",
                            "scopes": ["scopes_value1", "scopes_value2"],
                        },
                        "service_agent_auth": 1,
                        "webhook_type": 1,
                        "http_method": 1,
                        "request_body": "request_body_value",
                        "parameter_mapping": {},
                    },
                    "service_directory": {
                        "service": "service_value",
                        "generic_web_service": {},
                    },
                    "timeout": {"seconds": 751, "nanos": 543},
                    "disabled": True,
                }
            ]
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gcdc_environment.UpdateEnvironmentRequest.meta.fields["environment"]

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
    for field, value in request_init["environment"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["environment"][field])):
                    del request_init["environment"][field][i][subfield]
            else:
                del request_init["environment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_environment(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_update_environment"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_update_environment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcdc_environment.UpdateEnvironmentRequest.pb(
            gcdc_environment.UpdateEnvironmentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = gcdc_environment.UpdateEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_environment_rest_bad_request(
    request_type=environment.DeleteEnvironmentRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_environment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.DeleteEnvironmentRequest,
        dict,
    ],
)
def test_delete_environment_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = ""
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.delete_environment(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_environment_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_delete_environment"
    ) as pre:
        pre.assert_not_called()
        pb_message = environment.DeleteEnvironmentRequest.pb(
            environment.DeleteEnvironmentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        request = environment.DeleteEnvironmentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_environment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_lookup_environment_history_rest_bad_request(
    request_type=environment.LookupEnvironmentHistoryRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.lookup_environment_history(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.LookupEnvironmentHistoryRequest,
        dict,
    ],
)
def test_lookup_environment_history_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.LookupEnvironmentHistoryResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = environment.LookupEnvironmentHistoryResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.lookup_environment_history(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.LookupEnvironmentHistoryPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_lookup_environment_history_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_lookup_environment_history"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_lookup_environment_history"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.LookupEnvironmentHistoryRequest.pb(
            environment.LookupEnvironmentHistoryRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = environment.LookupEnvironmentHistoryResponse.to_json(
            environment.LookupEnvironmentHistoryResponse()
        )
        req.return_value.content = return_value

        request = environment.LookupEnvironmentHistoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environment.LookupEnvironmentHistoryResponse()

        client.lookup_environment_history(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_run_continuous_test_rest_bad_request(
    request_type=environment.RunContinuousTestRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.run_continuous_test(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.RunContinuousTestRequest,
        dict,
    ],
)
def test_run_continuous_test_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.run_continuous_test(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_run_continuous_test_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_run_continuous_test"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_run_continuous_test"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.RunContinuousTestRequest.pb(
            environment.RunContinuousTestRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = environment.RunContinuousTestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.run_continuous_test(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_continuous_test_results_rest_bad_request(
    request_type=environment.ListContinuousTestResultsRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_continuous_test_results(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.ListContinuousTestResultsRequest,
        dict,
    ],
)
def test_list_continuous_test_results_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = environment.ListContinuousTestResultsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = environment.ListContinuousTestResultsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_continuous_test_results(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListContinuousTestResultsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_continuous_test_results_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_list_continuous_test_results"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_list_continuous_test_results"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.ListContinuousTestResultsRequest.pb(
            environment.ListContinuousTestResultsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = environment.ListContinuousTestResultsResponse.to_json(
            environment.ListContinuousTestResultsResponse()
        )
        req.return_value.content = return_value

        request = environment.ListContinuousTestResultsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = environment.ListContinuousTestResultsResponse()

        client.list_continuous_test_results(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_deploy_flow_rest_bad_request(request_type=environment.DeployFlowRequest):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.deploy_flow(request)


@pytest.mark.parametrize(
    "request_type",
    [
        environment.DeployFlowRequest,
        dict,
    ],
)
def test_deploy_flow_rest_call_success(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "environment": "projects/sample1/locations/sample2/agents/sample3/environments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.deploy_flow(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_deploy_flow_rest_interceptors(null_interceptor):
    transport = transports.EnvironmentsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EnvironmentsRestInterceptor(),
    )
    client = EnvironmentsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EnvironmentsRestInterceptor, "post_deploy_flow"
    ) as post, mock.patch.object(
        transports.EnvironmentsRestInterceptor, "pre_deploy_flow"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = environment.DeployFlowRequest.pb(environment.DeployFlowRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = json_format.MessageToJson(operations_pb2.Operation())
        req.return_value.content = return_value

        request = environment.DeployFlowRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.deploy_flow(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_location_rest_bad_request(request_type=locations_pb2.GetLocationRequest):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
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
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    request_type=locations_pb2.ListLocationsRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_cancel_operation_rest_bad_request(
    request_type=operations_pb2.CancelOperationRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/operations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/operations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = "{}"
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/operations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/operations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    request_type=operations_pb2.ListOperationsRequest,
):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")

        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_initialize_client_w_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_environments_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        client.list_environments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListEnvironmentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_environment_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        client.get_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.GetEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_environment_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        client.create_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.CreateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_environment_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        client.update_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gcdc_environment.UpdateEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_environment_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        client.delete_environment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeleteEnvironmentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_lookup_environment_history_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.lookup_environment_history), "__call__"
    ) as call:
        client.lookup_environment_history(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.LookupEnvironmentHistoryRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_run_continuous_test_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.run_continuous_test), "__call__"
    ) as call:
        client.run_continuous_test(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.RunContinuousTestRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_continuous_test_results_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_continuous_test_results), "__call__"
    ) as call:
        client.list_continuous_test_results(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.ListContinuousTestResultsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_deploy_flow_empty_call_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.deploy_flow), "__call__") as call:
        client.deploy_flow(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = environment.DeployFlowRequest()

        assert args[0] == request_msg


def test_environments_rest_lro_client():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have an api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.EnvironmentsGrpcTransport,
    )


def test_environments_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.EnvironmentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_environments_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.environments.transports.EnvironmentsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.EnvironmentsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_environments",
        "get_environment",
        "create_environment",
        "update_environment",
        "delete_environment",
        "lookup_environment_history",
        "run_continuous_test",
        "list_continuous_test_results",
        "deploy_flow",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
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


def test_environments_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.environments.transports.EnvironmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EnvironmentsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_environments_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflowcx_v3beta1.services.environments.transports.EnvironmentsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EnvironmentsTransport()
        adc.assert_called_once()


def test_environments_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        EnvironmentsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
    ],
)
def test_environments_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EnvironmentsGrpcTransport,
        transports.EnvironmentsGrpcAsyncIOTransport,
        transports.EnvironmentsRestTransport,
    ],
)
def test_environments_transport_auth_gdch_credentials(transport_class):
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
        (transports.EnvironmentsGrpcTransport, grpc_helpers),
        (transports.EnvironmentsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_environments_transport_create_channel(transport_class, grpc_helpers):
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
            "dialogflow.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=["1", "2"],
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_environments_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.EnvironmentsRestTransport(
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
def test_environments_host_no_port(transport_name):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dialogflow.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dialogflow.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_environments_host_with_port(transport_name):
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dialogflow.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dialogflow.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_environments_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = EnvironmentsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = EnvironmentsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_environments._session
    session2 = client2.transport.list_environments._session
    assert session1 != session2
    session1 = client1.transport.get_environment._session
    session2 = client2.transport.get_environment._session
    assert session1 != session2
    session1 = client1.transport.create_environment._session
    session2 = client2.transport.create_environment._session
    assert session1 != session2
    session1 = client1.transport.update_environment._session
    session2 = client2.transport.update_environment._session
    assert session1 != session2
    session1 = client1.transport.delete_environment._session
    session2 = client2.transport.delete_environment._session
    assert session1 != session2
    session1 = client1.transport.lookup_environment_history._session
    session2 = client2.transport.lookup_environment_history._session
    assert session1 != session2
    session1 = client1.transport.run_continuous_test._session
    session2 = client2.transport.run_continuous_test._session
    assert session1 != session2
    session1 = client1.transport.list_continuous_test_results._session
    session2 = client2.transport.list_continuous_test_results._session
    assert session1 != session2
    session1 = client1.transport.deploy_flow._session
    session2 = client2.transport.deploy_flow._session
    assert session1 != session2


def test_environments_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EnvironmentsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_environments_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EnvironmentsGrpcAsyncIOTransport(
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
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.EnvironmentsGrpcTransport, transports.EnvironmentsGrpcAsyncIOTransport],
)
def test_environments_transport_channel_mtls_with_adc(transport_class):
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


def test_environments_grpc_lro_client():
    client = EnvironmentsClient(
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


def test_environments_grpc_lro_async_client():
    client = EnvironmentsAsyncClient(
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


def test_continuous_test_result_path():
    project = "squid"
    location = "clam"
    agent = "whelk"
    environment = "octopus"
    continuous_test_result = "oyster"
    expected = "projects/{project}/locations/{location}/agents/{agent}/environments/{environment}/continuousTestResults/{continuous_test_result}".format(
        project=project,
        location=location,
        agent=agent,
        environment=environment,
        continuous_test_result=continuous_test_result,
    )
    actual = EnvironmentsClient.continuous_test_result_path(
        project, location, agent, environment, continuous_test_result
    )
    assert expected == actual


def test_parse_continuous_test_result_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "agent": "mussel",
        "environment": "winkle",
        "continuous_test_result": "nautilus",
    }
    path = EnvironmentsClient.continuous_test_result_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_continuous_test_result_path(path)
    assert expected == actual


def test_environment_path():
    project = "scallop"
    location = "abalone"
    agent = "squid"
    environment = "clam"
    expected = "projects/{project}/locations/{location}/agents/{agent}/environments/{environment}".format(
        project=project,
        location=location,
        agent=agent,
        environment=environment,
    )
    actual = EnvironmentsClient.environment_path(project, location, agent, environment)
    assert expected == actual


def test_parse_environment_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "agent": "oyster",
        "environment": "nudibranch",
    }
    path = EnvironmentsClient.environment_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_environment_path(path)
    assert expected == actual


def test_service_path():
    project = "cuttlefish"
    location = "mussel"
    namespace = "winkle"
    service = "nautilus"
    expected = "projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}".format(
        project=project,
        location=location,
        namespace=namespace,
        service=service,
    )
    actual = EnvironmentsClient.service_path(project, location, namespace, service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "namespace": "squid",
        "service": "clam",
    }
    path = EnvironmentsClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_service_path(path)
    assert expected == actual


def test_test_case_path():
    project = "whelk"
    location = "octopus"
    agent = "oyster"
    test_case = "nudibranch"
    expected = "projects/{project}/locations/{location}/agents/{agent}/testCases/{test_case}".format(
        project=project,
        location=location,
        agent=agent,
        test_case=test_case,
    )
    actual = EnvironmentsClient.test_case_path(project, location, agent, test_case)
    assert expected == actual


def test_parse_test_case_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "agent": "winkle",
        "test_case": "nautilus",
    }
    path = EnvironmentsClient.test_case_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_test_case_path(path)
    assert expected == actual


def test_test_case_result_path():
    project = "scallop"
    location = "abalone"
    agent = "squid"
    test_case = "clam"
    result = "whelk"
    expected = "projects/{project}/locations/{location}/agents/{agent}/testCases/{test_case}/results/{result}".format(
        project=project,
        location=location,
        agent=agent,
        test_case=test_case,
        result=result,
    )
    actual = EnvironmentsClient.test_case_result_path(
        project, location, agent, test_case, result
    )
    assert expected == actual


def test_parse_test_case_result_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "agent": "nudibranch",
        "test_case": "cuttlefish",
        "result": "mussel",
    }
    path = EnvironmentsClient.test_case_result_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_test_case_result_path(path)
    assert expected == actual


def test_version_path():
    project = "winkle"
    location = "nautilus"
    agent = "scallop"
    flow = "abalone"
    version = "squid"
    expected = "projects/{project}/locations/{location}/agents/{agent}/flows/{flow}/versions/{version}".format(
        project=project,
        location=location,
        agent=agent,
        flow=flow,
        version=version,
    )
    actual = EnvironmentsClient.version_path(project, location, agent, flow, version)
    assert expected == actual


def test_parse_version_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "agent": "octopus",
        "flow": "oyster",
        "version": "nudibranch",
    }
    path = EnvironmentsClient.version_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_version_path(path)
    assert expected == actual


def test_webhook_path():
    project = "cuttlefish"
    location = "mussel"
    agent = "winkle"
    webhook = "nautilus"
    expected = "projects/{project}/locations/{location}/agents/{agent}/webhooks/{webhook}".format(
        project=project,
        location=location,
        agent=agent,
        webhook=webhook,
    )
    actual = EnvironmentsClient.webhook_path(project, location, agent, webhook)
    assert expected == actual


def test_parse_webhook_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "agent": "squid",
        "webhook": "clam",
    }
    path = EnvironmentsClient.webhook_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_webhook_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = EnvironmentsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = EnvironmentsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = EnvironmentsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = EnvironmentsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = EnvironmentsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = EnvironmentsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = EnvironmentsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = EnvironmentsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = EnvironmentsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = EnvironmentsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = EnvironmentsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.EnvironmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = EnvironmentsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.EnvironmentsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = EnvironmentsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_cancel_operation(transport: str = "grpc"):
    client = EnvironmentsClient(
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
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
async def test_list_locations_async(transport: str = "grpc_asyncio"):
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = EnvironmentsClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = EnvironmentsAsyncClient(credentials=async_anonymous_credentials())

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
    client = EnvironmentsClient(
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
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(),
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


def test_transport_close_grpc():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = EnvironmentsAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = EnvironmentsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
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
        client = EnvironmentsClient(
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
        (EnvironmentsClient, transports.EnvironmentsGrpcTransport),
        (EnvironmentsAsyncClient, transports.EnvironmentsGrpcAsyncIOTransport),
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
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
