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

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.apps.script.type.calendar.types import calendar_addon_manifest
from google.apps.script.type.docs.types import docs_addon_manifest
from google.apps.script.type.drive.types import drive_addon_manifest
from google.apps.script.type.gmail.types import gmail_addon_manifest
from google.apps.script.type.sheets.types import sheets_addon_manifest
from google.apps.script.type.slides.types import slides_addon_manifest
from google.apps.script.type.types import (
    addon_widget_set,
    extension_point,
    script_manifest,
)
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.cloud.gsuiteaddons_v1.services.g_suite_add_ons import (
    GSuiteAddOnsAsyncClient,
    GSuiteAddOnsClient,
    pagers,
    transports,
)
from google.cloud.gsuiteaddons_v1.types import gsuiteaddons


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

    assert GSuiteAddOnsClient._get_default_mtls_endpoint(None) is None
    assert (
        GSuiteAddOnsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        GSuiteAddOnsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        GSuiteAddOnsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        GSuiteAddOnsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert GSuiteAddOnsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert GSuiteAddOnsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            GSuiteAddOnsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            GSuiteAddOnsClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert GSuiteAddOnsClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert GSuiteAddOnsClient._get_client_cert_source(None, False) is None
    assert (
        GSuiteAddOnsClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        GSuiteAddOnsClient._get_client_cert_source(mock_provided_cert_source, True)
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
                GSuiteAddOnsClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                GSuiteAddOnsClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    GSuiteAddOnsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsClient),
)
@mock.patch.object(
    GSuiteAddOnsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = GSuiteAddOnsClient._DEFAULT_UNIVERSE
    default_endpoint = GSuiteAddOnsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = GSuiteAddOnsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        GSuiteAddOnsClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == GSuiteAddOnsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(None, None, default_universe, "always")
        == GSuiteAddOnsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == GSuiteAddOnsClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        GSuiteAddOnsClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        GSuiteAddOnsClient._get_api_endpoint(
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
        GSuiteAddOnsClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        GSuiteAddOnsClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        GSuiteAddOnsClient._get_universe_domain(None, None)
        == GSuiteAddOnsClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        GSuiteAddOnsClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport, "grpc"),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest"),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (GSuiteAddOnsClient, "grpc"),
        (GSuiteAddOnsAsyncClient, "grpc_asyncio"),
        (GSuiteAddOnsClient, "rest"),
    ],
)
def test_g_suite_add_ons_client_from_service_account_info(client_class, transport_name):
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
            "gsuiteaddons.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://gsuiteaddons.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.GSuiteAddOnsGrpcTransport, "grpc"),
        (transports.GSuiteAddOnsGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.GSuiteAddOnsRestTransport, "rest"),
    ],
)
def test_g_suite_add_ons_client_service_account_always_use_jwt(
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
        (GSuiteAddOnsClient, "grpc"),
        (GSuiteAddOnsAsyncClient, "grpc_asyncio"),
        (GSuiteAddOnsClient, "rest"),
    ],
)
def test_g_suite_add_ons_client_from_service_account_file(client_class, transport_name):
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
            "gsuiteaddons.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://gsuiteaddons.googleapis.com"
        )


def test_g_suite_add_ons_client_get_transport_class():
    transport = GSuiteAddOnsClient.get_transport_class()
    available_transports = [
        transports.GSuiteAddOnsGrpcTransport,
        transports.GSuiteAddOnsRestTransport,
    ]
    assert transport in available_transports

    transport = GSuiteAddOnsClient.get_transport_class("grpc")
    assert transport == transports.GSuiteAddOnsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport, "grpc"),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest"),
    ],
)
@mock.patch.object(
    GSuiteAddOnsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsClient),
)
@mock.patch.object(
    GSuiteAddOnsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsAsyncClient),
)
def test_g_suite_add_ons_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(GSuiteAddOnsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(GSuiteAddOnsClient, "get_transport_class") as gtc:
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
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport, "grpc", "true"),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport, "grpc", "false"),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest", "true"),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    GSuiteAddOnsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsClient),
)
@mock.patch.object(
    GSuiteAddOnsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_g_suite_add_ons_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [GSuiteAddOnsClient, GSuiteAddOnsAsyncClient])
@mock.patch.object(
    GSuiteAddOnsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(GSuiteAddOnsClient)
)
@mock.patch.object(
    GSuiteAddOnsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(GSuiteAddOnsAsyncClient),
)
def test_g_suite_add_ons_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize("client_class", [GSuiteAddOnsClient, GSuiteAddOnsAsyncClient])
@mock.patch.object(
    GSuiteAddOnsClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsClient),
)
@mock.patch.object(
    GSuiteAddOnsAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(GSuiteAddOnsAsyncClient),
)
def test_g_suite_add_ons_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = GSuiteAddOnsClient._DEFAULT_UNIVERSE
    default_endpoint = GSuiteAddOnsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = GSuiteAddOnsClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport, "grpc"),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest"),
    ],
)
def test_g_suite_add_ons_client_client_options_scopes(
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
            GSuiteAddOnsClient,
            transports.GSuiteAddOnsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (GSuiteAddOnsClient, transports.GSuiteAddOnsRestTransport, "rest", None),
    ],
)
def test_g_suite_add_ons_client_client_options_credentials_file(
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


def test_g_suite_add_ons_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.gsuiteaddons_v1.services.g_suite_add_ons.transports.GSuiteAddOnsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = GSuiteAddOnsClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
            GSuiteAddOnsClient,
            transports.GSuiteAddOnsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            GSuiteAddOnsAsyncClient,
            transports.GSuiteAddOnsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_g_suite_add_ons_client_create_channel_credentials_file(
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
            "gsuiteaddons.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="gsuiteaddons.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetAuthorizationRequest,
        dict,
    ],
)
def test_get_authorization(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Authorization(
            name="name_value",
            service_account_email="service_account_email_value",
            oauth_client_id="oauth_client_id_value",
        )
        response = client.get_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetAuthorizationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Authorization)
    assert response.name == "name_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.oauth_client_id == "oauth_client_id_value"


def test_get_authorization_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.GetAuthorizationRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_authorization(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.GetAuthorizationRequest(
            name="name_value",
        )


def test_get_authorization_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_authorization in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_authorization
        ] = mock_rpc
        request = {}
        client.get_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_authorization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_authorization_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_authorization
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_authorization
        ] = mock_rpc

        request = {}
        await client.get_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_authorization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_authorization_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.GetAuthorizationRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Authorization(
                name="name_value",
                service_account_email="service_account_email_value",
                oauth_client_id="oauth_client_id_value",
            )
        )
        response = await client.get_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetAuthorizationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Authorization)
    assert response.name == "name_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.oauth_client_id == "oauth_client_id_value"


@pytest.mark.asyncio
async def test_get_authorization_async_from_dict():
    await test_get_authorization_async(request_type=dict)


def test_get_authorization_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Authorization()
        client.get_authorization(request)

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
async def test_get_authorization_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Authorization()
        )
        await client.get_authorization(request)

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


def test_get_authorization_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Authorization()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_authorization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_authorization_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_authorization(
            gsuiteaddons.GetAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_authorization_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Authorization()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Authorization()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_authorization(
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
async def test_get_authorization_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_authorization(
            gsuiteaddons.GetAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.CreateDeploymentRequest,
        dict,
    ],
)
def test_create_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
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
        call.return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )
        response = client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.CreateDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


def test_create_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.CreateDeploymentRequest(
        parent="parent_value",
        deployment_id="deployment_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.CreateDeploymentRequest(
            parent="parent_value",
            deployment_id="deployment_id_value",
        )


def test_create_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_deployment
        ] = mock_rpc
        request = {}
        client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_deployment
        ] = mock_rpc

        request = {}
        await client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_deployment_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.CreateDeploymentRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
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
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        response = await client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.CreateDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_create_deployment_async_from_dict():
    await test_create_deployment_async(request_type=dict)


def test_create_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.CreateDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.CreateDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_deployment(
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
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
        mock_val = gsuiteaddons.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].deployment_id
        mock_val = "deployment_id_value"
        assert arg == mock_val


def test_create_deployment_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_deployment(
            gsuiteaddons.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


@pytest.mark.asyncio
async def test_create_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_deployment(
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
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
        mock_val = gsuiteaddons.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].deployment_id
        mock_val = "deployment_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_deployment_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_deployment(
            gsuiteaddons.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.ReplaceDeploymentRequest,
        dict,
    ],
)
def test_replace_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )
        response = client.replace_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.ReplaceDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


def test_replace_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.ReplaceDeploymentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.replace_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.ReplaceDeploymentRequest()


def test_replace_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.replace_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.replace_deployment
        ] = mock_rpc
        request = {}
        client.replace_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.replace_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_replace_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.replace_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.replace_deployment
        ] = mock_rpc

        request = {}
        await client.replace_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.replace_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_replace_deployment_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.ReplaceDeploymentRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        response = await client.replace_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.ReplaceDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_replace_deployment_async_from_dict():
    await test_replace_deployment_async(request_type=dict)


def test_replace_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.ReplaceDeploymentRequest()

    request.deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Deployment()
        client.replace_deployment(request)

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
async def test_replace_deployment_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.ReplaceDeploymentRequest()

    request.deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
        )
        await client.replace_deployment(request)

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


def test_replace_deployment_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.replace_deployment(
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].deployment
        mock_val = gsuiteaddons.Deployment(name="name_value")
        assert arg == mock_val


def test_replace_deployment_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.replace_deployment(
            gsuiteaddons.ReplaceDeploymentRequest(),
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )


@pytest.mark.asyncio
async def test_replace_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.replace_deployment(
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].deployment
        mock_val = gsuiteaddons.Deployment(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_replace_deployment_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.replace_deployment(
            gsuiteaddons.ReplaceDeploymentRequest(),
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetDeploymentRequest,
        dict,
    ],
)
def test_get_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )
        response = client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


def test_get_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.GetDeploymentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.GetDeploymentRequest(
            name="name_value",
        )


def test_get_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_deployment] = mock_rpc
        request = {}
        client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_deployment
        ] = mock_rpc

        request = {}
        await client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_deployment_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.GetDeploymentRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        response = await client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_deployment_async_from_dict():
    await test_get_deployment_async(request_type=dict)


def test_get_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value = gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_deployment(
            gsuiteaddons.GetDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment()
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_deployment(
            gsuiteaddons.GetDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.ListDeploymentsRequest,
        dict,
    ],
)
def test_list_deployments(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.ListDeploymentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.ListDeploymentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deployments_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.ListDeploymentsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_deployments(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.ListDeploymentsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_deployments_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_deployments in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_deployments
        ] = mock_rpc
        request = {}
        client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_deployments_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_deployments
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_deployments
        ] = mock_rpc

        request = {}
        await client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_deployments_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.ListDeploymentsRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.ListDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.ListDeploymentsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_deployments_async_from_dict():
    await test_list_deployments_async(request_type=dict)


def test_list_deployments_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.ListDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value = gsuiteaddons.ListDeploymentsResponse()
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.ListDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.ListDeploymentsResponse()
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
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.ListDeploymentsResponse()
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
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployments(
            gsuiteaddons.ListDeploymentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_deployments_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.ListDeploymentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.ListDeploymentsResponse()
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_deployments(
            gsuiteaddons.ListDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_deployments_pager(transport_name: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="abc",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="ghi",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
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
        pager = client.list_deployments(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gsuiteaddons.Deployment) for i in results)


def test_list_deployments_pages(transport_name: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="abc",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="ghi",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_deployments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_deployments_async_pager():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployments), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="abc",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="ghi",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
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
        assert all(isinstance(i, gsuiteaddons.Deployment) for i in responses)


@pytest.mark.asyncio
async def test_list_deployments_async_pages():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployments), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="abc",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="ghi",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
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
        gsuiteaddons.DeleteDeploymentRequest,
        dict,
    ],
)
def test_delete_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.DeleteDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.DeleteDeploymentRequest(
        name="name_value",
        etag="etag_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.DeleteDeploymentRequest(
            name="name_value",
            etag="etag_value",
        )


def test_delete_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_deployment
        ] = mock_rpc
        request = {}
        client.delete_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_deployment
        ] = mock_rpc

        request = {}
        await client.delete_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_deployment_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.DeleteDeploymentRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.DeleteDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_deployment_async_from_dict():
    await test_delete_deployment_async(request_type=dict)


def test_delete_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.DeleteDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.delete_deployment(request)

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
async def test_delete_deployment_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.DeleteDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_deployment(request)

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


def test_delete_deployment_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_deployment_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_deployment(
            gsuiteaddons.DeleteDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_deployment(
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
async def test_delete_deployment_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_deployment(
            gsuiteaddons.DeleteDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.InstallDeploymentRequest,
        dict,
    ],
)
def test_install_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.install_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.InstallDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_install_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.InstallDeploymentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.install_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.InstallDeploymentRequest(
            name="name_value",
        )


def test_install_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.install_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.install_deployment
        ] = mock_rpc
        request = {}
        client.install_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.install_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_install_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.install_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.install_deployment
        ] = mock_rpc

        request = {}
        await client.install_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.install_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_install_deployment_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.InstallDeploymentRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.install_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.InstallDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_install_deployment_async_from_dict():
    await test_install_deployment_async(request_type=dict)


def test_install_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.InstallDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.install_deployment(request)

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
async def test_install_deployment_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.InstallDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.install_deployment(request)

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


def test_install_deployment_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.install_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_install_deployment_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.install_deployment(
            gsuiteaddons.InstallDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_install_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.install_deployment(
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
async def test_install_deployment_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.install_deployment(
            gsuiteaddons.InstallDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.UninstallDeploymentRequest,
        dict,
    ],
)
def test_uninstall_deployment(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.uninstall_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.UninstallDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_uninstall_deployment_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.UninstallDeploymentRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.uninstall_deployment(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.UninstallDeploymentRequest(
            name="name_value",
        )


def test_uninstall_deployment_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.uninstall_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.uninstall_deployment
        ] = mock_rpc
        request = {}
        client.uninstall_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.uninstall_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_uninstall_deployment_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.uninstall_deployment
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.uninstall_deployment
        ] = mock_rpc

        request = {}
        await client.uninstall_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.uninstall_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_uninstall_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=gsuiteaddons.UninstallDeploymentRequest,
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.uninstall_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.UninstallDeploymentRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_uninstall_deployment_async_from_dict():
    await test_uninstall_deployment_async(request_type=dict)


def test_uninstall_deployment_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.UninstallDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.uninstall_deployment(request)

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
async def test_uninstall_deployment_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.UninstallDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.uninstall_deployment(request)

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


def test_uninstall_deployment_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.uninstall_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_uninstall_deployment_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.uninstall_deployment(
            gsuiteaddons.UninstallDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_uninstall_deployment_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.uninstall_deployment(
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
async def test_uninstall_deployment_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.uninstall_deployment(
            gsuiteaddons.UninstallDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetInstallStatusRequest,
        dict,
    ],
)
def test_get_install_status(request_type, transport: str = "grpc"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.InstallStatus(
            name="name_value",
        )
        response = client.get_install_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetInstallStatusRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.InstallStatus)
    assert response.name == "name_value"


def test_get_install_status_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = gsuiteaddons.GetInstallStatusRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_install_status(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gsuiteaddons.GetInstallStatusRequest(
            name="name_value",
        )


def test_get_install_status_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_install_status in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_install_status
        ] = mock_rpc
        request = {}
        client.get_install_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_install_status(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_install_status_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_install_status
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_install_status
        ] = mock_rpc

        request = {}
        await client.get_install_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_install_status(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_install_status_async(
    transport: str = "grpc_asyncio", request_type=gsuiteaddons.GetInstallStatusRequest
):
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.InstallStatus(
                name="name_value",
            )
        )
        response = await client.get_install_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = gsuiteaddons.GetInstallStatusRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.InstallStatus)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_install_status_async_from_dict():
    await test_get_install_status_async(request_type=dict)


def test_get_install_status_field_headers():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetInstallStatusRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.InstallStatus()
        client.get_install_status(request)

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
async def test_get_install_status_field_headers_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gsuiteaddons.GetInstallStatusRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.InstallStatus()
        )
        await client.get_install_status(request)

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


def test_get_install_status_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.InstallStatus()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_install_status(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_install_status_flattened_error():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_install_status(
            gsuiteaddons.GetInstallStatusRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_install_status_flattened_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gsuiteaddons.InstallStatus()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.InstallStatus()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_install_status(
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
async def test_get_install_status_flattened_error_async():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_install_status(
            gsuiteaddons.GetInstallStatusRequest(),
            name="name_value",
        )


def test_get_authorization_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_authorization in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_authorization
        ] = mock_rpc

        request = {}
        client.get_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_authorization(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_authorization_rest_required_fields(
    request_type=gsuiteaddons.GetAuthorizationRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).get_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.Authorization()
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
            return_value = gsuiteaddons.Authorization.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_authorization(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_authorization_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_authorization._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_authorization_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Authorization()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/authorization"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gsuiteaddons.Authorization.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_authorization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/authorization}" % client.transport._host, args[1]
        )


def test_get_authorization_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_authorization(
            gsuiteaddons.GetAuthorizationRequest(),
            name="name_value",
        )


def test_create_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_deployment
        ] = mock_rpc

        request = {}
        client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_deployment_rest_required_fields(
    request_type=gsuiteaddons.CreateDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["deployment_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "deploymentId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "deploymentId" in jsonified_request
    assert jsonified_request["deploymentId"] == request_init["deployment_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["deploymentId"] = "deployment_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("deployment_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "deploymentId" in jsonified_request
    assert jsonified_request["deploymentId"] == "deployment_id_value"

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.Deployment()
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
            return_value = gsuiteaddons.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_deployment(request)

            expected_params = [
                (
                    "deploymentId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("deploymentId",))
        & set(
            (
                "parent",
                "deploymentId",
                "deployment",
            )
        )
    )


def test_create_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*}/deployments" % client.transport._host, args[1]
        )


def test_create_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_deployment(
            gsuiteaddons.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=gsuiteaddons.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


def test_replace_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.replace_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.replace_deployment
        ] = mock_rpc

        request = {}
        client.replace_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.replace_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_replace_deployment_rest_required_fields(
    request_type=gsuiteaddons.ReplaceDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).replace_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).replace_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.Deployment()
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
                "method": "put",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gsuiteaddons.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.replace_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_replace_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.replace_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("deployment",)))


def test_replace_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "deployment": {"name": "projects/sample1/deployments/sample2"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.replace_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{deployment.name=projects/*/deployments/*}" % client.transport._host,
            args[1],
        )


def test_replace_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.replace_deployment(
            gsuiteaddons.ReplaceDeploymentRequest(),
            deployment=gsuiteaddons.Deployment(name="name_value"),
        )


def test_get_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_deployment] = mock_rpc

        request = {}
        client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_deployment_rest_required_fields(
    request_type=gsuiteaddons.GetDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).get_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.Deployment()
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
            return_value = gsuiteaddons.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/deployments/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/deployments/*}" % client.transport._host, args[1]
        )


def test_get_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_deployment(
            gsuiteaddons.GetDeploymentRequest(),
            name="name_value",
        )


def test_list_deployments_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_deployments in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_deployments
        ] = mock_rpc

        request = {}
        client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_deployments(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_deployments_rest_required_fields(
    request_type=gsuiteaddons.ListDeploymentsRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.ListDeploymentsResponse()
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
            return_value = gsuiteaddons.ListDeploymentsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_deployments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_deployments_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_deployments._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_deployments_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.ListDeploymentsResponse()

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
        # Convert return value to protobuf type
        return_value = gsuiteaddons.ListDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_deployments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*}/deployments" % client.transport._host, args[1]
        )


def test_list_deployments_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployments(
            gsuiteaddons.ListDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_deployments_rest_pager(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="abc",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                ],
                next_page_token="ghi",
            ),
            gsuiteaddons.ListDeploymentsResponse(
                deployments=[
                    gsuiteaddons.Deployment(),
                    gsuiteaddons.Deployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            gsuiteaddons.ListDeploymentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_deployments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gsuiteaddons.Deployment) for i in results)

        pages = list(client.list_deployments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_deployment in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_deployment
        ] = mock_rpc

        request = {}
        client.delete_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_deployment_rest_required_fields(
    request_type=gsuiteaddons.DeleteDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).delete_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
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

            response = client.delete_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag",)) & set(("name",)))


def test_delete_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/deployments/sample2"}

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

        client.delete_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/deployments/*}" % client.transport._host, args[1]
        )


def test_delete_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_deployment(
            gsuiteaddons.DeleteDeploymentRequest(),
            name="name_value",
        )


def test_install_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.install_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.install_deployment
        ] = mock_rpc

        request = {}
        client.install_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.install_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_install_deployment_rest_required_fields(
    request_type=gsuiteaddons.InstallDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).install_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).install_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
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

            response = client.install_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_install_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.install_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_install_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/deployments/sample2"}

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

        client.install_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/deployments/*}:install" % client.transport._host,
            args[1],
        )


def test_install_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.install_deployment(
            gsuiteaddons.InstallDeploymentRequest(),
            name="name_value",
        )


def test_uninstall_deployment_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.uninstall_deployment in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.uninstall_deployment
        ] = mock_rpc

        request = {}
        client.uninstall_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.uninstall_deployment(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_uninstall_deployment_rest_required_fields(
    request_type=gsuiteaddons.UninstallDeploymentRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).uninstall_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).uninstall_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
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

            response = client.uninstall_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_uninstall_deployment_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.uninstall_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_uninstall_deployment_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/deployments/sample2"}

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

        client.uninstall_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/deployments/*}:uninstall" % client.transport._host,
            args[1],
        )


def test_uninstall_deployment_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.uninstall_deployment(
            gsuiteaddons.UninstallDeploymentRequest(),
            name="name_value",
        )


def test_get_install_status_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_install_status in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_install_status
        ] = mock_rpc

        request = {}
        client.get_install_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_install_status(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_install_status_rest_required_fields(
    request_type=gsuiteaddons.GetInstallStatusRequest,
):
    transport_class = transports.GSuiteAddOnsRestTransport

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
    ).get_install_status._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_install_status._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gsuiteaddons.InstallStatus()
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
            return_value = gsuiteaddons.InstallStatus.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_install_status(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_install_status_rest_unset_required_fields():
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_install_status._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_install_status_rest_flattened():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.InstallStatus()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/deployments/sample2/installStatus"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gsuiteaddons.InstallStatus.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_install_status(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/deployments/*/installStatus}"
            % client.transport._host,
            args[1],
        )


def test_get_install_status_rest_flattened_error(transport: str = "rest"):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_install_status(
            gsuiteaddons.GetInstallStatusRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GSuiteAddOnsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = GSuiteAddOnsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = GSuiteAddOnsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = GSuiteAddOnsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = GSuiteAddOnsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GSuiteAddOnsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.GSuiteAddOnsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.GSuiteAddOnsGrpcTransport,
        transports.GSuiteAddOnsGrpcAsyncIOTransport,
        transports.GSuiteAddOnsRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = GSuiteAddOnsClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_authorization_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Authorization()
        client.get_authorization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetAuthorizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Deployment()
        client.create_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.CreateDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_replace_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.Deployment()
        client.replace_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ReplaceDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value = gsuiteaddons.Deployment()
        client.get_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_deployments_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value = gsuiteaddons.ListDeploymentsResponse()
        client.list_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ListDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.delete_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.DeleteDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_install_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.install_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.InstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_uninstall_deployment_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.uninstall_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.UninstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_install_status_empty_call_grpc():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        call.return_value = gsuiteaddons.InstallStatus()
        client.get_install_status(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetInstallStatusRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = GSuiteAddOnsAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_authorization_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Authorization(
                name="name_value",
                service_account_email="service_account_email_value",
                oauth_client_id="oauth_client_id_value",
            )
        )
        await client.get_authorization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetAuthorizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        await client.create_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.CreateDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_replace_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        await client.replace_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ReplaceDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.Deployment(
                name="name_value",
                oauth_scopes=["oauth_scopes_value"],
                etag="etag_value",
            )
        )
        await client.get_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_deployments_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.ListDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ListDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.DeleteDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_install_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.install_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.InstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_uninstall_deployment_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.uninstall_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.UninstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_install_status_empty_call_grpc_asyncio():
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gsuiteaddons.InstallStatus(
                name="name_value",
            )
        )
        await client.get_install_status(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetInstallStatusRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = GSuiteAddOnsClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_get_authorization_rest_bad_request(
    request_type=gsuiteaddons.GetAuthorizationRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/authorization"}
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
        client.get_authorization(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetAuthorizationRequest,
        dict,
    ],
)
def test_get_authorization_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/authorization"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Authorization(
            name="name_value",
            service_account_email="service_account_email_value",
            oauth_client_id="oauth_client_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.Authorization.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_authorization(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Authorization)
    assert response.name == "name_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.oauth_client_id == "oauth_client_id_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_authorization_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_get_authorization"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_get_authorization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.GetAuthorizationRequest.pb(
            gsuiteaddons.GetAuthorizationRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.Authorization.to_json(gsuiteaddons.Authorization())
        req.return_value.content = return_value

        request = gsuiteaddons.GetAuthorizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.Authorization()

        client.get_authorization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_deployment_rest_bad_request(
    request_type=gsuiteaddons.CreateDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
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
        client.create_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.CreateDeploymentRequest,
        dict,
    ],
)
def test_create_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["deployment"] = {
        "name": "name_value",
        "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
        "add_ons": {
            "common": {
                "name": "name_value",
                "logo_url": "logo_url_value",
                "layout_properties": {
                    "primary_color": "primary_color_value",
                    "secondary_color": "secondary_color_value",
                },
                "add_on_widget_set": {"used_widgets": [1]},
                "use_locale_from_app": True,
                "homepage_trigger": {
                    "run_function": "run_function_value",
                    "enabled": {"value": True},
                },
                "universal_actions": [
                    {
                        "label": "label_value",
                        "open_link": "open_link_value",
                        "run_function": "run_function_value",
                    }
                ],
                "open_link_url_prefixes": {
                    "values": [
                        {
                            "null_value": 0,
                            "number_value": 0.1285,
                            "string_value": "string_value_value",
                            "bool_value": True,
                            "struct_value": {"fields": {}},
                            "list_value": {},
                        }
                    ]
                },
            },
            "gmail": {
                "homepage_trigger": {},
                "contextual_triggers": [
                    {
                        "unconditional": {},
                        "on_trigger_function": "on_trigger_function_value",
                    }
                ],
                "universal_actions": [
                    {
                        "text": "text_value",
                        "open_link": "open_link_value",
                        "run_function": "run_function_value",
                    }
                ],
                "compose_trigger": {
                    "actions": [
                        {
                            "run_function": "run_function_value",
                            "label": "label_value",
                            "logo_url": "logo_url_value",
                        }
                    ],
                    "draft_access": 1,
                },
                "authorization_check_function": "authorization_check_function_value",
            },
            "drive": {
                "homepage_trigger": {},
                "on_items_selected_trigger": {"run_function": "run_function_value"},
            },
            "calendar": {
                "homepage_trigger": {},
                "conference_solution": [
                    {
                        "on_create_function": "on_create_function_value",
                        "id": "id_value",
                        "name": "name_value",
                        "logo_url": "logo_url_value",
                    }
                ],
                "create_settings_url_function": "create_settings_url_function_value",
                "event_open_trigger": {"run_function": "run_function_value"},
                "event_update_trigger": {},
                "current_event_access": 1,
            },
            "docs": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "sheets": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "slides": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "http_options": {"authorization_header": 1},
        },
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gsuiteaddons.CreateDeploymentRequest.meta.fields["deployment"]

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
        return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_create_deployment"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_create_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.CreateDeploymentRequest.pb(
            gsuiteaddons.CreateDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.Deployment.to_json(gsuiteaddons.Deployment())
        req.return_value.content = return_value

        request = gsuiteaddons.CreateDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.Deployment()

        client.create_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_replace_deployment_rest_bad_request(
    request_type=gsuiteaddons.ReplaceDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"deployment": {"name": "projects/sample1/deployments/sample2"}}
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
        client.replace_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.ReplaceDeploymentRequest,
        dict,
    ],
)
def test_replace_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"deployment": {"name": "projects/sample1/deployments/sample2"}}
    request_init["deployment"] = {
        "name": "projects/sample1/deployments/sample2",
        "oauth_scopes": ["oauth_scopes_value1", "oauth_scopes_value2"],
        "add_ons": {
            "common": {
                "name": "name_value",
                "logo_url": "logo_url_value",
                "layout_properties": {
                    "primary_color": "primary_color_value",
                    "secondary_color": "secondary_color_value",
                },
                "add_on_widget_set": {"used_widgets": [1]},
                "use_locale_from_app": True,
                "homepage_trigger": {
                    "run_function": "run_function_value",
                    "enabled": {"value": True},
                },
                "universal_actions": [
                    {
                        "label": "label_value",
                        "open_link": "open_link_value",
                        "run_function": "run_function_value",
                    }
                ],
                "open_link_url_prefixes": {
                    "values": [
                        {
                            "null_value": 0,
                            "number_value": 0.1285,
                            "string_value": "string_value_value",
                            "bool_value": True,
                            "struct_value": {"fields": {}},
                            "list_value": {},
                        }
                    ]
                },
            },
            "gmail": {
                "homepage_trigger": {},
                "contextual_triggers": [
                    {
                        "unconditional": {},
                        "on_trigger_function": "on_trigger_function_value",
                    }
                ],
                "universal_actions": [
                    {
                        "text": "text_value",
                        "open_link": "open_link_value",
                        "run_function": "run_function_value",
                    }
                ],
                "compose_trigger": {
                    "actions": [
                        {
                            "run_function": "run_function_value",
                            "label": "label_value",
                            "logo_url": "logo_url_value",
                        }
                    ],
                    "draft_access": 1,
                },
                "authorization_check_function": "authorization_check_function_value",
            },
            "drive": {
                "homepage_trigger": {},
                "on_items_selected_trigger": {"run_function": "run_function_value"},
            },
            "calendar": {
                "homepage_trigger": {},
                "conference_solution": [
                    {
                        "on_create_function": "on_create_function_value",
                        "id": "id_value",
                        "name": "name_value",
                        "logo_url": "logo_url_value",
                    }
                ],
                "create_settings_url_function": "create_settings_url_function_value",
                "event_open_trigger": {"run_function": "run_function_value"},
                "event_update_trigger": {},
                "current_event_access": 1,
            },
            "docs": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "sheets": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "slides": {
                "homepage_trigger": {},
                "on_file_scope_granted_trigger": {"run_function": "run_function_value"},
            },
            "http_options": {"authorization_header": 1},
        },
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = gsuiteaddons.ReplaceDeploymentRequest.meta.fields["deployment"]

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
        return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.replace_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_replace_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_replace_deployment"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_replace_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.ReplaceDeploymentRequest.pb(
            gsuiteaddons.ReplaceDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.Deployment.to_json(gsuiteaddons.Deployment())
        req.return_value.content = return_value

        request = gsuiteaddons.ReplaceDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.Deployment()

        client.replace_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_deployment_rest_bad_request(
    request_type=gsuiteaddons.GetDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        client.get_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetDeploymentRequest,
        dict,
    ],
)
def test_get_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.Deployment(
            name="name_value",
            oauth_scopes=["oauth_scopes_value"],
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.Deployment)
    assert response.name == "name_value"
    assert response.oauth_scopes == ["oauth_scopes_value"]
    assert response.etag == "etag_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_get_deployment"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_get_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.GetDeploymentRequest.pb(
            gsuiteaddons.GetDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.Deployment.to_json(gsuiteaddons.Deployment())
        req.return_value.content = return_value

        request = gsuiteaddons.GetDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.Deployment()

        client.get_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_deployments_rest_bad_request(
    request_type=gsuiteaddons.ListDeploymentsRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
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
        client.list_deployments(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.ListDeploymentsRequest,
        dict,
    ],
)
def test_list_deployments_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.ListDeploymentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.ListDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_deployments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_deployments_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_list_deployments"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_list_deployments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.ListDeploymentsRequest.pb(
            gsuiteaddons.ListDeploymentsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.ListDeploymentsResponse.to_json(
            gsuiteaddons.ListDeploymentsResponse()
        )
        req.return_value.content = return_value

        request = gsuiteaddons.ListDeploymentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.ListDeploymentsResponse()

        client.list_deployments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_deployment_rest_bad_request(
    request_type=gsuiteaddons.DeleteDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        client.delete_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.DeleteDeploymentRequest,
        dict,
    ],
)
def test_delete_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        response = client.delete_deployment(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_delete_deployment"
    ) as pre:
        pre.assert_not_called()
        pb_message = gsuiteaddons.DeleteDeploymentRequest.pb(
            gsuiteaddons.DeleteDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200

        request = gsuiteaddons.DeleteDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_install_deployment_rest_bad_request(
    request_type=gsuiteaddons.InstallDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        client.install_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.InstallDeploymentRequest,
        dict,
    ],
)
def test_install_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        response = client.install_deployment(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_install_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_install_deployment"
    ) as pre:
        pre.assert_not_called()
        pb_message = gsuiteaddons.InstallDeploymentRequest.pb(
            gsuiteaddons.InstallDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200

        request = gsuiteaddons.InstallDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.install_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_uninstall_deployment_rest_bad_request(
    request_type=gsuiteaddons.UninstallDeploymentRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        client.uninstall_deployment(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.UninstallDeploymentRequest,
        dict,
    ],
)
def test_uninstall_deployment_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2"}
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
        response = client.uninstall_deployment(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_uninstall_deployment_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_uninstall_deployment"
    ) as pre:
        pre.assert_not_called()
        pb_message = gsuiteaddons.UninstallDeploymentRequest.pb(
            gsuiteaddons.UninstallDeploymentRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200

        request = gsuiteaddons.UninstallDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.uninstall_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_get_install_status_rest_bad_request(
    request_type=gsuiteaddons.GetInstallStatusRequest,
):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2/installStatus"}
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
        client.get_install_status(request)


@pytest.mark.parametrize(
    "request_type",
    [
        gsuiteaddons.GetInstallStatusRequest,
        dict,
    ],
)
def test_get_install_status_rest_call_success(request_type):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/deployments/sample2/installStatus"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gsuiteaddons.InstallStatus(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = gsuiteaddons.InstallStatus.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_install_status(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gsuiteaddons.InstallStatus)
    assert response.name == "name_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_install_status_rest_interceptors(null_interceptor):
    transport = transports.GSuiteAddOnsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.GSuiteAddOnsRestInterceptor(),
    )
    client = GSuiteAddOnsClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "post_get_install_status"
    ) as post, mock.patch.object(
        transports.GSuiteAddOnsRestInterceptor, "pre_get_install_status"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gsuiteaddons.GetInstallStatusRequest.pb(
            gsuiteaddons.GetInstallStatusRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        return_value = gsuiteaddons.InstallStatus.to_json(gsuiteaddons.InstallStatus())
        req.return_value.content = return_value

        request = gsuiteaddons.GetInstallStatusRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gsuiteaddons.InstallStatus()

        client.get_install_status(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_initialize_client_w_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_authorization_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_authorization), "__call__"
    ) as call:
        client.get_authorization(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetAuthorizationRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        client.create_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.CreateDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_replace_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.replace_deployment), "__call__"
    ) as call:
        client.replace_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ReplaceDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        client.get_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_deployments_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        client.list_deployments(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.ListDeploymentsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_deployment), "__call__"
    ) as call:
        client.delete_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.DeleteDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_install_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.install_deployment), "__call__"
    ) as call:
        client.install_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.InstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_uninstall_deployment_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.uninstall_deployment), "__call__"
    ) as call:
        client.uninstall_deployment(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.UninstallDeploymentRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_install_status_empty_call_rest():
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_install_status), "__call__"
    ) as call:
        client.get_install_status(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = gsuiteaddons.GetInstallStatusRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.GSuiteAddOnsGrpcTransport,
    )


def test_g_suite_add_ons_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.GSuiteAddOnsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_g_suite_add_ons_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.gsuiteaddons_v1.services.g_suite_add_ons.transports.GSuiteAddOnsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.GSuiteAddOnsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_authorization",
        "create_deployment",
        "replace_deployment",
        "get_deployment",
        "list_deployments",
        "delete_deployment",
        "install_deployment",
        "uninstall_deployment",
        "get_install_status",
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


def test_g_suite_add_ons_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.gsuiteaddons_v1.services.g_suite_add_ons.transports.GSuiteAddOnsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GSuiteAddOnsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_g_suite_add_ons_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.gsuiteaddons_v1.services.g_suite_add_ons.transports.GSuiteAddOnsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GSuiteAddOnsTransport()
        adc.assert_called_once()


def test_g_suite_add_ons_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        GSuiteAddOnsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.GSuiteAddOnsGrpcTransport,
        transports.GSuiteAddOnsGrpcAsyncIOTransport,
    ],
)
def test_g_suite_add_ons_transport_auth_adc(transport_class):
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
        transports.GSuiteAddOnsGrpcTransport,
        transports.GSuiteAddOnsGrpcAsyncIOTransport,
        transports.GSuiteAddOnsRestTransport,
    ],
)
def test_g_suite_add_ons_transport_auth_gdch_credentials(transport_class):
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
        (transports.GSuiteAddOnsGrpcTransport, grpc_helpers),
        (transports.GSuiteAddOnsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_g_suite_add_ons_transport_create_channel(transport_class, grpc_helpers):
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
            "gsuiteaddons.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="gsuiteaddons.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.GSuiteAddOnsGrpcTransport, transports.GSuiteAddOnsGrpcAsyncIOTransport],
)
def test_g_suite_add_ons_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_g_suite_add_ons_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.GSuiteAddOnsRestTransport(
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
def test_g_suite_add_ons_host_no_port(transport_name):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gsuiteaddons.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "gsuiteaddons.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://gsuiteaddons.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_g_suite_add_ons_host_with_port(transport_name):
    client = GSuiteAddOnsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gsuiteaddons.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "gsuiteaddons.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://gsuiteaddons.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_g_suite_add_ons_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = GSuiteAddOnsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = GSuiteAddOnsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_authorization._session
    session2 = client2.transport.get_authorization._session
    assert session1 != session2
    session1 = client1.transport.create_deployment._session
    session2 = client2.transport.create_deployment._session
    assert session1 != session2
    session1 = client1.transport.replace_deployment._session
    session2 = client2.transport.replace_deployment._session
    assert session1 != session2
    session1 = client1.transport.get_deployment._session
    session2 = client2.transport.get_deployment._session
    assert session1 != session2
    session1 = client1.transport.list_deployments._session
    session2 = client2.transport.list_deployments._session
    assert session1 != session2
    session1 = client1.transport.delete_deployment._session
    session2 = client2.transport.delete_deployment._session
    assert session1 != session2
    session1 = client1.transport.install_deployment._session
    session2 = client2.transport.install_deployment._session
    assert session1 != session2
    session1 = client1.transport.uninstall_deployment._session
    session2 = client2.transport.uninstall_deployment._session
    assert session1 != session2
    session1 = client1.transport.get_install_status._session
    session2 = client2.transport.get_install_status._session
    assert session1 != session2


def test_g_suite_add_ons_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GSuiteAddOnsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_g_suite_add_ons_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GSuiteAddOnsGrpcAsyncIOTransport(
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
    [transports.GSuiteAddOnsGrpcTransport, transports.GSuiteAddOnsGrpcAsyncIOTransport],
)
def test_g_suite_add_ons_transport_channel_mtls_with_client_cert_source(
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
    [transports.GSuiteAddOnsGrpcTransport, transports.GSuiteAddOnsGrpcAsyncIOTransport],
)
def test_g_suite_add_ons_transport_channel_mtls_with_adc(transport_class):
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


def test_authorization_path():
    project = "squid"
    expected = "projects/{project}/authorization".format(
        project=project,
    )
    actual = GSuiteAddOnsClient.authorization_path(project)
    assert expected == actual


def test_parse_authorization_path():
    expected = {
        "project": "clam",
    }
    path = GSuiteAddOnsClient.authorization_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_authorization_path(path)
    assert expected == actual


def test_deployment_path():
    project = "whelk"
    deployment = "octopus"
    expected = "projects/{project}/deployments/{deployment}".format(
        project=project,
        deployment=deployment,
    )
    actual = GSuiteAddOnsClient.deployment_path(project, deployment)
    assert expected == actual


def test_parse_deployment_path():
    expected = {
        "project": "oyster",
        "deployment": "nudibranch",
    }
    path = GSuiteAddOnsClient.deployment_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_deployment_path(path)
    assert expected == actual


def test_install_status_path():
    project = "cuttlefish"
    deployment = "mussel"
    expected = "projects/{project}/deployments/{deployment}/installStatus".format(
        project=project,
        deployment=deployment,
    )
    actual = GSuiteAddOnsClient.install_status_path(project, deployment)
    assert expected == actual


def test_parse_install_status_path():
    expected = {
        "project": "winkle",
        "deployment": "nautilus",
    }
    path = GSuiteAddOnsClient.install_status_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_install_status_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = GSuiteAddOnsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = GSuiteAddOnsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = GSuiteAddOnsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = GSuiteAddOnsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = GSuiteAddOnsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = GSuiteAddOnsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = GSuiteAddOnsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = GSuiteAddOnsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = GSuiteAddOnsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = GSuiteAddOnsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = GSuiteAddOnsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.GSuiteAddOnsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = GSuiteAddOnsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.GSuiteAddOnsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = GSuiteAddOnsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = GSuiteAddOnsClient(
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
    client = GSuiteAddOnsAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = GSuiteAddOnsClient(
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
        client = GSuiteAddOnsClient(
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
        (GSuiteAddOnsClient, transports.GSuiteAddOnsGrpcTransport),
        (GSuiteAddOnsAsyncClient, transports.GSuiteAddOnsGrpcAsyncIOTransport),
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
