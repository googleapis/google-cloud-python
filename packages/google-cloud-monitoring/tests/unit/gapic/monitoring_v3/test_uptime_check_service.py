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

import math

from google.api import monitored_resource_pb2  # type: ignore
from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.monitoring_v3.services.uptime_check_service import (
    UptimeCheckServiceAsyncClient,
    UptimeCheckServiceClient,
    pagers,
    transports,
)
from google.cloud.monitoring_v3.types import uptime, uptime_service


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

    assert UptimeCheckServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert UptimeCheckServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            UptimeCheckServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            UptimeCheckServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert UptimeCheckServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert UptimeCheckServiceClient._get_client_cert_source(None, False) is None
    assert (
        UptimeCheckServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        UptimeCheckServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
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
                UptimeCheckServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                UptimeCheckServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    UptimeCheckServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = UptimeCheckServiceClient._DEFAULT_UNIVERSE
    default_endpoint = UptimeCheckServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = UptimeCheckServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        UptimeCheckServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == UptimeCheckServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == UptimeCheckServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == UptimeCheckServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        UptimeCheckServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        UptimeCheckServiceClient._get_api_endpoint(
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
        UptimeCheckServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        UptimeCheckServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        UptimeCheckServiceClient._get_universe_domain(None, None)
        == UptimeCheckServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        UptimeCheckServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
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
        (UptimeCheckServiceClient, "grpc"),
        (UptimeCheckServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_uptime_check_service_client_from_service_account_info(
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

        assert client.transport._host == ("monitoring.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (transports.UptimeCheckServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_uptime_check_service_client_service_account_always_use_jwt(
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
        (UptimeCheckServiceClient, "grpc"),
        (UptimeCheckServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_uptime_check_service_client_from_service_account_file(
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

        assert client.transport._host == ("monitoring.googleapis.com:443")


def test_uptime_check_service_client_get_transport_class():
    transport = UptimeCheckServiceClient.get_transport_class()
    available_transports = [
        transports.UptimeCheckServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = UptimeCheckServiceClient.get_transport_class("grpc")
    assert transport == transports.UptimeCheckServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceAsyncClient),
)
def test_uptime_check_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(UptimeCheckServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(UptimeCheckServiceClient, "get_transport_class") as gtc:
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
        (
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_uptime_check_service_client_mtls_env_auto(
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


@pytest.mark.parametrize(
    "client_class", [UptimeCheckServiceClient, UptimeCheckServiceAsyncClient]
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(UptimeCheckServiceAsyncClient),
)
def test_uptime_check_service_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize(
    "client_class", [UptimeCheckServiceClient, UptimeCheckServiceAsyncClient]
)
@mock.patch.object(
    UptimeCheckServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceClient),
)
@mock.patch.object(
    UptimeCheckServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(UptimeCheckServiceAsyncClient),
)
def test_uptime_check_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = UptimeCheckServiceClient._DEFAULT_UNIVERSE
    default_endpoint = UptimeCheckServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = UptimeCheckServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport, "grpc"),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_uptime_check_service_client_client_options_scopes(
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
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_uptime_check_service_client_client_options_credentials_file(
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


def test_uptime_check_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = UptimeCheckServiceClient(
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
            UptimeCheckServiceClient,
            transports.UptimeCheckServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_uptime_check_service_client_create_channel_credentials_file(
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
            "monitoring.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            scopes=None,
            default_host="monitoring.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.ListUptimeCheckConfigsRequest,
        dict,
    ],
)
def test_list_uptime_check_configs(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.ListUptimeCheckConfigsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckConfigsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_uptime_check_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_uptime_check_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckConfigsRequest()


def test_list_uptime_check_configs_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.ListUptimeCheckConfigsRequest(
        parent="parent_value",
        filter="filter_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_uptime_check_configs(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckConfigsRequest(
            parent="parent_value",
            filter="filter_value",
            page_token="page_token_value",
        )


def test_list_uptime_check_configs_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_uptime_check_configs
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_uptime_check_configs
        ] = mock_rpc
        request = {}
        client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_uptime_check_configs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_uptime_check_configs_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_uptime_check_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckConfigsRequest()


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_uptime_check_configs
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_uptime_check_configs
        ] = mock_object

        request = {}
        await client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_uptime_check_configs(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.ListUptimeCheckConfigsRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_uptime_check_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.ListUptimeCheckConfigsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_from_dict():
    await test_list_uptime_check_configs_async(request_type=dict)


def test_list_uptime_check_configs_field_headers():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.ListUptimeCheckConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()
        client.list_uptime_check_configs(request)

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
async def test_list_uptime_check_configs_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.ListUptimeCheckConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse()
        )
        await client.list_uptime_check_configs(request)

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


def test_list_uptime_check_configs_flattened():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_uptime_check_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_uptime_check_configs_flattened_error():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_uptime_check_configs(
            uptime_service.ListUptimeCheckConfigsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_uptime_check_configs_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_uptime_check_configs(
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
async def test_list_uptime_check_configs_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_uptime_check_configs(
            uptime_service.ListUptimeCheckConfigsRequest(),
            parent="parent_value",
        )


def test_list_uptime_check_configs_pager(transport_name: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
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
        pager = client.list_uptime_check_configs(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, uptime.UptimeCheckConfig) for i in results)


def test_list_uptime_check_configs_pages(transport_name: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_uptime_check_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_pager():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_uptime_check_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, uptime.UptimeCheckConfig) for i in responses)


@pytest.mark.asyncio
async def test_list_uptime_check_configs_async_pages():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckConfigsResponse(
                uptime_check_configs=[
                    uptime.UptimeCheckConfig(),
                    uptime.UptimeCheckConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_uptime_check_configs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.GetUptimeCheckConfigRequest,
        dict,
    ],
)
def test_get_uptime_check_config(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
        )
        response = client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.GetUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


def test_get_uptime_check_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.GetUptimeCheckConfigRequest()


def test_get_uptime_check_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.GetUptimeCheckConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_uptime_check_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.GetUptimeCheckConfigRequest(
            name="name_value",
        )


def test_get_uptime_check_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_uptime_check_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_uptime_check_config
        ] = mock_rpc
        request = {}
        client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_uptime_check_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.get_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.GetUptimeCheckConfigRequest()


@pytest.mark.asyncio
async def test_get_uptime_check_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_uptime_check_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_uptime_check_config
        ] = mock_object

        request = {}
        await client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_uptime_check_config_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.GetUptimeCheckConfigRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.get_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.GetUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


@pytest.mark.asyncio
async def test_get_uptime_check_config_async_from_dict():
    await test_get_uptime_check_config_async(request_type=dict)


def test_get_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.GetUptimeCheckConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()
        client.get_uptime_check_config(request)

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
async def test_get_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.GetUptimeCheckConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        await client.get_uptime_check_config(request)

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


def test_get_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_uptime_check_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_uptime_check_config(
            uptime_service.GetUptimeCheckConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_uptime_check_config(
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
async def test_get_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_uptime_check_config(
            uptime_service.GetUptimeCheckConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.CreateUptimeCheckConfigRequest,
        dict,
    ],
)
def test_create_uptime_check_config(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
        )
        response = client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.CreateUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


def test_create_uptime_check_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.CreateUptimeCheckConfigRequest()


def test_create_uptime_check_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.CreateUptimeCheckConfigRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_uptime_check_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.CreateUptimeCheckConfigRequest(
            parent="parent_value",
        )


def test_create_uptime_check_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_uptime_check_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_uptime_check_config
        ] = mock_rpc
        request = {}
        client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_uptime_check_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.create_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.CreateUptimeCheckConfigRequest()


@pytest.mark.asyncio
async def test_create_uptime_check_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_uptime_check_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_uptime_check_config
        ] = mock_object

        request = {}
        await client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_uptime_check_config_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.CreateUptimeCheckConfigRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.create_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.CreateUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


@pytest.mark.asyncio
async def test_create_uptime_check_config_async_from_dict():
    await test_create_uptime_check_config_async(request_type=dict)


def test_create_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.CreateUptimeCheckConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()
        client.create_uptime_check_config(request)

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
async def test_create_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.CreateUptimeCheckConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        await client.create_uptime_check_config(request)

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


def test_create_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_uptime_check_config(
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].uptime_check_config
        mock_val = uptime.UptimeCheckConfig(name="name_value")
        assert arg == mock_val


def test_create_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_uptime_check_config(
            uptime_service.CreateUptimeCheckConfigRequest(),
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_uptime_check_config(
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].uptime_check_config
        mock_val = uptime.UptimeCheckConfig(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_uptime_check_config(
            uptime_service.CreateUptimeCheckConfigRequest(),
            parent="parent_value",
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.UpdateUptimeCheckConfigRequest,
        dict,
    ],
)
def test_update_uptime_check_config(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig(
            name="name_value",
            display_name="display_name_value",
            checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
            selected_regions=[uptime.UptimeCheckRegion.USA],
            is_internal=True,
        )
        response = client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.UpdateUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


def test_update_uptime_check_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.UpdateUptimeCheckConfigRequest()


def test_update_uptime_check_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.UpdateUptimeCheckConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_uptime_check_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.UpdateUptimeCheckConfigRequest()


def test_update_uptime_check_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_uptime_check_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_uptime_check_config
        ] = mock_rpc
        request = {}
        client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_uptime_check_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.update_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.UpdateUptimeCheckConfigRequest()


@pytest.mark.asyncio
async def test_update_uptime_check_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_uptime_check_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_uptime_check_config
        ] = mock_object

        request = {}
        await client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_uptime_check_config_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.UpdateUptimeCheckConfigRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig(
                name="name_value",
                display_name="display_name_value",
                checker_type=uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS,
                selected_regions=[uptime.UptimeCheckRegion.USA],
                is_internal=True,
            )
        )
        response = await client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.UpdateUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, uptime.UptimeCheckConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert (
        response.checker_type == uptime.UptimeCheckConfig.CheckerType.STATIC_IP_CHECKERS
    )
    assert response.selected_regions == [uptime.UptimeCheckRegion.USA]
    assert response.is_internal is True


@pytest.mark.asyncio
async def test_update_uptime_check_config_async_from_dict():
    await test_update_uptime_check_config_async(request_type=dict)


def test_update_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.UpdateUptimeCheckConfigRequest()

    request.uptime_check_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value = uptime.UptimeCheckConfig()
        client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "uptime_check_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.UpdateUptimeCheckConfigRequest()

    request.uptime_check_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        await client.update_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "uptime_check_config.name=name_value",
    ) in kw["metadata"]


def test_update_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_uptime_check_config(
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].uptime_check_config
        mock_val = uptime.UptimeCheckConfig(name="name_value")
        assert arg == mock_val


def test_update_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_uptime_check_config(
            uptime_service.UpdateUptimeCheckConfigRequest(),
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime.UptimeCheckConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime.UptimeCheckConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_uptime_check_config(
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].uptime_check_config
        mock_val = uptime.UptimeCheckConfig(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_uptime_check_config(
            uptime_service.UpdateUptimeCheckConfigRequest(),
            uptime_check_config=uptime.UptimeCheckConfig(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.DeleteUptimeCheckConfigRequest,
        dict,
    ],
)
def test_delete_uptime_check_config(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.DeleteUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_uptime_check_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.DeleteUptimeCheckConfigRequest()


def test_delete_uptime_check_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.DeleteUptimeCheckConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_uptime_check_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.DeleteUptimeCheckConfigRequest(
            name="name_value",
        )


def test_delete_uptime_check_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_uptime_check_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_uptime_check_config
        ] = mock_rpc
        request = {}
        client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_uptime_check_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_uptime_check_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.DeleteUptimeCheckConfigRequest()


@pytest.mark.asyncio
async def test_delete_uptime_check_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_uptime_check_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_uptime_check_config
        ] = mock_object

        request = {}
        await client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_uptime_check_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_uptime_check_config_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.DeleteUptimeCheckConfigRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_uptime_check_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.DeleteUptimeCheckConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_uptime_check_config_async_from_dict():
    await test_delete_uptime_check_config_async(request_type=dict)


def test_delete_uptime_check_config_field_headers():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.DeleteUptimeCheckConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value = None
        client.delete_uptime_check_config(request)

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
async def test_delete_uptime_check_config_field_headers_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = uptime_service.DeleteUptimeCheckConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_uptime_check_config(request)

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


def test_delete_uptime_check_config_flattened():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_uptime_check_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_uptime_check_config_flattened_error():
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_uptime_check_config(
            uptime_service.DeleteUptimeCheckConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_uptime_check_config_flattened_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_uptime_check_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_uptime_check_config(
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
async def test_delete_uptime_check_config_flattened_error_async():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_uptime_check_config(
            uptime_service.DeleteUptimeCheckConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        uptime_service.ListUptimeCheckIpsRequest,
        dict,
    ],
)
def test_list_uptime_check_ips(request_type, transport: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = uptime_service.ListUptimeCheckIpsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = uptime_service.ListUptimeCheckIpsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckIpsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_uptime_check_ips_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_uptime_check_ips()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckIpsRequest()


def test_list_uptime_check_ips_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = uptime_service.ListUptimeCheckIpsRequest(
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_uptime_check_ips(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckIpsRequest(
            page_token="page_token_value",
        )


def test_list_uptime_check_ips_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_uptime_check_ips
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_uptime_check_ips
        ] = mock_rpc
        request = {}
        client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_uptime_check_ips(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_uptime_check_ips_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckIpsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_uptime_check_ips()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == uptime_service.ListUptimeCheckIpsRequest()


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = UptimeCheckServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_uptime_check_ips
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_uptime_check_ips
        ] = mock_object

        request = {}
        await client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_uptime_check_ips(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async(
    transport: str = "grpc_asyncio",
    request_type=uptime_service.ListUptimeCheckIpsRequest,
):
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            uptime_service.ListUptimeCheckIpsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_uptime_check_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = uptime_service.ListUptimeCheckIpsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUptimeCheckIpsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_from_dict():
    await test_list_uptime_check_ips_async(request_type=dict)


def test_list_uptime_check_ips_pager(transport_name: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_uptime_check_ips(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, uptime.UptimeCheckIp) for i in results)


def test_list_uptime_check_ips_pages(transport_name: str = "grpc"):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_uptime_check_ips(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_pager():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_uptime_check_ips(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, uptime.UptimeCheckIp) for i in responses)


@pytest.mark.asyncio
async def test_list_uptime_check_ips_async_pages():
    client = UptimeCheckServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_uptime_check_ips),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="abc",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[],
                next_page_token="def",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                ],
                next_page_token="ghi",
            ),
            uptime_service.ListUptimeCheckIpsResponse(
                uptime_check_ips=[
                    uptime.UptimeCheckIp(),
                    uptime.UptimeCheckIp(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_uptime_check_ips(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = UptimeCheckServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = UptimeCheckServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.UptimeCheckServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.UptimeCheckServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
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
    ],
)
def test_transport_kind(transport_name):
    transport = UptimeCheckServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.UptimeCheckServiceGrpcTransport,
    )


def test_uptime_check_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.UptimeCheckServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_uptime_check_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.UptimeCheckServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_uptime_check_configs",
        "get_uptime_check_config",
        "create_uptime_check_config",
        "update_uptime_check_config",
        "delete_uptime_check_config",
        "list_uptime_check_ips",
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


def test_uptime_check_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.UptimeCheckServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_uptime_check_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.monitoring_v3.services.uptime_check_service.transports.UptimeCheckServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.UptimeCheckServiceTransport()
        adc.assert_called_once()


def test_uptime_check_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        UptimeCheckServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.UptimeCheckServiceGrpcTransport, grpc_helpers),
        (transports.UptimeCheckServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_uptime_check_service_transport_create_channel(transport_class, grpc_helpers):
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
            "monitoring.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            scopes=["1", "2"],
            default_host="monitoring.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_grpc_transport_client_cert_source_for_mtls(
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


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_uptime_check_service_host_no_port(transport_name):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("monitoring.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_uptime_check_service_host_with_port(transport_name):
    client = UptimeCheckServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("monitoring.googleapis.com:8000")


def test_uptime_check_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.UptimeCheckServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_uptime_check_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.UptimeCheckServiceGrpcAsyncIOTransport(
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
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_channel_mtls_with_client_cert_source(
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
        transports.UptimeCheckServiceGrpcTransport,
        transports.UptimeCheckServiceGrpcAsyncIOTransport,
    ],
)
def test_uptime_check_service_transport_channel_mtls_with_adc(transport_class):
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


def test_function_path():
    project = "squid"
    location = "clam"
    function = "whelk"
    expected = "projects/{project}/locations/{location}/functions/{function}".format(
        project=project,
        location=location,
        function=function,
    )
    actual = UptimeCheckServiceClient.function_path(project, location, function)
    assert expected == actual


def test_parse_function_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "function": "nudibranch",
    }
    path = UptimeCheckServiceClient.function_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_function_path(path)
    assert expected == actual


def test_uptime_check_config_path():
    project = "cuttlefish"
    uptime_check_config = "mussel"
    expected = "projects/{project}/uptimeCheckConfigs/{uptime_check_config}".format(
        project=project,
        uptime_check_config=uptime_check_config,
    )
    actual = UptimeCheckServiceClient.uptime_check_config_path(
        project, uptime_check_config
    )
    assert expected == actual


def test_parse_uptime_check_config_path():
    expected = {
        "project": "winkle",
        "uptime_check_config": "nautilus",
    }
    path = UptimeCheckServiceClient.uptime_check_config_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_uptime_check_config_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = UptimeCheckServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = UptimeCheckServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = UptimeCheckServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = UptimeCheckServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = UptimeCheckServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = UptimeCheckServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = UptimeCheckServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = UptimeCheckServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = UptimeCheckServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = UptimeCheckServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = UptimeCheckServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.UptimeCheckServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = UptimeCheckServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.UptimeCheckServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = UptimeCheckServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = UptimeCheckServiceAsyncClient(
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
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = UptimeCheckServiceClient(
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
        "grpc",
    ]
    for transport in transports:
        client = UptimeCheckServiceClient(
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
        (UptimeCheckServiceClient, transports.UptimeCheckServiceGrpcTransport),
        (
            UptimeCheckServiceAsyncClient,
            transports.UptimeCheckServiceGrpcAsyncIOTransport,
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
