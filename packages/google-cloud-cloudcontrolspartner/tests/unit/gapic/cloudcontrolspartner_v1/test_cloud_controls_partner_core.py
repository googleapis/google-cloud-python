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

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.cloudcontrolspartner_v1.services.cloud_controls_partner_core import (
    CloudControlsPartnerCoreAsyncClient,
    CloudControlsPartnerCoreClient,
    pagers,
    transports,
)
from google.cloud.cloudcontrolspartner_v1.types import (
    access_approval_requests,
    customer_workloads,
    customers,
    ekm_connections,
    partner_permissions,
    partners,
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

    assert CloudControlsPartnerCoreClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudControlsPartnerCoreClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert CloudControlsPartnerCoreClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            CloudControlsPartnerCoreClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            CloudControlsPartnerCoreClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert CloudControlsPartnerCoreClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert CloudControlsPartnerCoreClient._get_client_cert_source(None, False) is None
    assert (
        CloudControlsPartnerCoreClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        CloudControlsPartnerCoreClient._get_client_cert_source(
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
                CloudControlsPartnerCoreClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                CloudControlsPartnerCoreClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    CloudControlsPartnerCoreClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreClient),
)
@mock.patch.object(
    CloudControlsPartnerCoreAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = CloudControlsPartnerCoreClient._DEFAULT_UNIVERSE
    default_endpoint = CloudControlsPartnerCoreClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CloudControlsPartnerCoreClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == CloudControlsPartnerCoreClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == CloudControlsPartnerCoreClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == CloudControlsPartnerCoreClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        CloudControlsPartnerCoreClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        CloudControlsPartnerCoreClient._get_api_endpoint(
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
        CloudControlsPartnerCoreClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        CloudControlsPartnerCoreClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        CloudControlsPartnerCoreClient._get_universe_domain(None, None)
        == CloudControlsPartnerCoreClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        CloudControlsPartnerCoreClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
        ),
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
        (CloudControlsPartnerCoreClient, "grpc"),
        (CloudControlsPartnerCoreAsyncClient, "grpc_asyncio"),
        (CloudControlsPartnerCoreClient, "rest"),
    ],
)
def test_cloud_controls_partner_core_client_from_service_account_info(
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
            "cloudcontrolspartner.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudcontrolspartner.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudControlsPartnerCoreGrpcTransport, "grpc"),
        (transports.CloudControlsPartnerCoreGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CloudControlsPartnerCoreRestTransport, "rest"),
    ],
)
def test_cloud_controls_partner_core_client_service_account_always_use_jwt(
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
        (CloudControlsPartnerCoreClient, "grpc"),
        (CloudControlsPartnerCoreAsyncClient, "grpc_asyncio"),
        (CloudControlsPartnerCoreClient, "rest"),
    ],
)
def test_cloud_controls_partner_core_client_from_service_account_file(
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
            "cloudcontrolspartner.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudcontrolspartner.googleapis.com"
        )


def test_cloud_controls_partner_core_client_get_transport_class():
    transport = CloudControlsPartnerCoreClient.get_transport_class()
    available_transports = [
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreRestTransport,
    ]
    assert transport in available_transports

    transport = CloudControlsPartnerCoreClient.get_transport_class("grpc")
    assert transport == transports.CloudControlsPartnerCoreGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    CloudControlsPartnerCoreClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreClient),
)
@mock.patch.object(
    CloudControlsPartnerCoreAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreAsyncClient),
)
def test_cloud_controls_partner_core_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        CloudControlsPartnerCoreClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        CloudControlsPartnerCoreClient, "get_transport_class"
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
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
            "true",
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
            "false",
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
            "true",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudControlsPartnerCoreClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreClient),
)
@mock.patch.object(
    CloudControlsPartnerCoreAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_controls_partner_core_client_mtls_env_auto(
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
    "client_class",
    [CloudControlsPartnerCoreClient, CloudControlsPartnerCoreAsyncClient],
)
@mock.patch.object(
    CloudControlsPartnerCoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudControlsPartnerCoreClient),
)
@mock.patch.object(
    CloudControlsPartnerCoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudControlsPartnerCoreAsyncClient),
)
def test_cloud_controls_partner_core_client_get_mtls_endpoint_and_cert_source(
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
    "client_class",
    [CloudControlsPartnerCoreClient, CloudControlsPartnerCoreAsyncClient],
)
@mock.patch.object(
    CloudControlsPartnerCoreClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreClient),
)
@mock.patch.object(
    CloudControlsPartnerCoreAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudControlsPartnerCoreAsyncClient),
)
def test_cloud_controls_partner_core_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = CloudControlsPartnerCoreClient._DEFAULT_UNIVERSE
    default_endpoint = CloudControlsPartnerCoreClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CloudControlsPartnerCoreClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
        ),
    ],
)
def test_cloud_controls_partner_core_client_client_options_scopes(
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
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_cloud_controls_partner_core_client_client_options_credentials_file(
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


def test_cloud_controls_partner_core_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.cloudcontrolspartner_v1.services.cloud_controls_partner_core.transports.CloudControlsPartnerCoreGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudControlsPartnerCoreClient(
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
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_controls_partner_core_client_create_channel_credentials_file(
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
            "cloudcontrolspartner.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="cloudcontrolspartner.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        customer_workloads.GetWorkloadRequest,
        dict,
    ],
)
def test_get_workload(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.Workload(
            name="name_value",
            folder_id=936,
            folder="folder_value",
            is_onboarded=True,
            key_management_project_id="key_management_project_id_value",
            location="location_value",
            partner=customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS,
        )
        response = client.get_workload(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = customer_workloads.GetWorkloadRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, customer_workloads.Workload)
    assert response.name == "name_value"
    assert response.folder_id == 936
    assert response.folder == "folder_value"
    assert response.is_onboarded is True
    assert response.key_management_project_id == "key_management_project_id_value"
    assert response.location == "location_value"
    assert (
        response.partner
        == customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS
    )


def test_get_workload_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_workload()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.GetWorkloadRequest()


def test_get_workload_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = customer_workloads.GetWorkloadRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_workload(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.GetWorkloadRequest(
            name="name_value",
        )


def test_get_workload_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_workload in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_workload] = mock_rpc
        request = {}
        client.get_workload(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_workload(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_workload_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.Workload(
                name="name_value",
                folder_id=936,
                folder="folder_value",
                is_onboarded=True,
                key_management_project_id="key_management_project_id_value",
                location="location_value",
                partner=customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS,
            )
        )
        response = await client.get_workload()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.GetWorkloadRequest()


@pytest.mark.asyncio
async def test_get_workload_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_workload
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_workload
        ] = mock_object

        request = {}
        await client.get_workload(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_workload(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_workload_async(
    transport: str = "grpc_asyncio", request_type=customer_workloads.GetWorkloadRequest
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.Workload(
                name="name_value",
                folder_id=936,
                folder="folder_value",
                is_onboarded=True,
                key_management_project_id="key_management_project_id_value",
                location="location_value",
                partner=customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS,
            )
        )
        response = await client.get_workload(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = customer_workloads.GetWorkloadRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, customer_workloads.Workload)
    assert response.name == "name_value"
    assert response.folder_id == 936
    assert response.folder == "folder_value"
    assert response.is_onboarded is True
    assert response.key_management_project_id == "key_management_project_id_value"
    assert response.location == "location_value"
    assert (
        response.partner
        == customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS
    )


@pytest.mark.asyncio
async def test_get_workload_async_from_dict():
    await test_get_workload_async(request_type=dict)


def test_get_workload_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customer_workloads.GetWorkloadRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        call.return_value = customer_workloads.Workload()
        client.get_workload(request)

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
async def test_get_workload_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customer_workloads.GetWorkloadRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.Workload()
        )
        await client.get_workload(request)

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


def test_get_workload_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.Workload()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_workload(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_workload_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workload(
            customer_workloads.GetWorkloadRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_workload_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_workload), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.Workload()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.Workload()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_workload(
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
async def test_get_workload_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_workload(
            customer_workloads.GetWorkloadRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        customer_workloads.ListWorkloadsRequest,
        dict,
    ],
)
def test_list_workloads(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.ListWorkloadsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_workloads(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = customer_workloads.ListWorkloadsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkloadsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workloads_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_workloads()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.ListWorkloadsRequest()


def test_list_workloads_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = customer_workloads.ListWorkloadsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_workloads(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.ListWorkloadsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_workloads_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_workloads in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_workloads] = mock_rpc
        request = {}
        client.list_workloads(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_workloads(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_workloads_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.ListWorkloadsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_workloads()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customer_workloads.ListWorkloadsRequest()


@pytest.mark.asyncio
async def test_list_workloads_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_workloads
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_workloads
        ] = mock_object

        request = {}
        await client.list_workloads(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_workloads(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_workloads_async(
    transport: str = "grpc_asyncio",
    request_type=customer_workloads.ListWorkloadsRequest,
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.ListWorkloadsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_workloads(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = customer_workloads.ListWorkloadsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkloadsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_workloads_async_from_dict():
    await test_list_workloads_async(request_type=dict)


def test_list_workloads_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customer_workloads.ListWorkloadsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        call.return_value = customer_workloads.ListWorkloadsResponse()
        client.list_workloads(request)

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
async def test_list_workloads_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customer_workloads.ListWorkloadsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.ListWorkloadsResponse()
        )
        await client.list_workloads(request)

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


def test_list_workloads_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.ListWorkloadsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_workloads(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_workloads_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workloads(
            customer_workloads.ListWorkloadsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_workloads_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customer_workloads.ListWorkloadsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customer_workloads.ListWorkloadsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_workloads(
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
async def test_list_workloads_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_workloads(
            customer_workloads.ListWorkloadsRequest(),
            parent="parent_value",
        )


def test_list_workloads_pager(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
                next_page_token="abc",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[],
                next_page_token="def",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                ],
                next_page_token="ghi",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
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
        pager = client.list_workloads(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, customer_workloads.Workload) for i in results)


def test_list_workloads_pages(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_workloads), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
                next_page_token="abc",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[],
                next_page_token="def",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                ],
                next_page_token="ghi",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_workloads(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_workloads_async_pager():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workloads), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
                next_page_token="abc",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[],
                next_page_token="def",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                ],
                next_page_token="ghi",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_workloads(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, customer_workloads.Workload) for i in responses)


@pytest.mark.asyncio
async def test_list_workloads_async_pages():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workloads), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
                next_page_token="abc",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[],
                next_page_token="def",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                ],
                next_page_token="ghi",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_workloads(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        customers.GetCustomerRequest,
        dict,
    ],
)
def test_get_customer(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer(
            name="name_value",
            display_name="display_name_value",
            is_onboarded=True,
        )
        response = client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = customers.GetCustomerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_onboarded is True


def test_get_customer_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.GetCustomerRequest()


def test_get_customer_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = customers.GetCustomerRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_customer(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.GetCustomerRequest(
            name="name_value",
        )


def test_get_customer_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_customer in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_customer] = mock_rpc
        request = {}
        client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_customer(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_customer_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.Customer(
                name="name_value",
                display_name="display_name_value",
                is_onboarded=True,
            )
        )
        response = await client.get_customer()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.GetCustomerRequest()


@pytest.mark.asyncio
async def test_get_customer_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_customer
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_customer
        ] = mock_object

        request = {}
        await client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_customer(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_customer_async(
    transport: str = "grpc_asyncio", request_type=customers.GetCustomerRequest
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.Customer(
                name="name_value",
                display_name="display_name_value",
                is_onboarded=True,
            )
        )
        response = await client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = customers.GetCustomerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_onboarded is True


@pytest.mark.asyncio
async def test_get_customer_async_from_dict():
    await test_get_customer_async(request_type=dict)


def test_get_customer_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customers.GetCustomerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value = customers.Customer()
        client.get_customer(request)

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
async def test_get_customer_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customers.GetCustomerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        await client.get_customer(request)

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


def test_get_customer_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_customer(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_customer_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_customer(
            customers.GetCustomerRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_customer_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_customer), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.Customer()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(customers.Customer())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_customer(
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
async def test_get_customer_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_customer(
            customers.GetCustomerRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        customers.ListCustomersRequest,
        dict,
    ],
)
def test_list_customers(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.ListCustomersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = customers.ListCustomersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_customers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_customers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.ListCustomersRequest()


def test_list_customers_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = customers.ListCustomersRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_customers(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.ListCustomersRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_customers_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_customers in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_customers] = mock_rpc
        request = {}
        client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_customers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_customers_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.ListCustomersResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_customers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == customers.ListCustomersRequest()


@pytest.mark.asyncio
async def test_list_customers_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_customers
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_customers
        ] = mock_object

        request = {}
        await client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_customers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_customers_async(
    transport: str = "grpc_asyncio", request_type=customers.ListCustomersRequest
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.ListCustomersResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = customers.ListCustomersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomersAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_customers_async_from_dict():
    await test_list_customers_async(request_type=dict)


def test_list_customers_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customers.ListCustomersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value = customers.ListCustomersResponse()
        client.list_customers(request)

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
async def test_list_customers_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = customers.ListCustomersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.ListCustomersResponse()
        )
        await client.list_customers(request)

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


def test_list_customers_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.ListCustomersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_customers(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_customers_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_customers(
            customers.ListCustomersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_customers_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = customers.ListCustomersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            customers.ListCustomersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_customers(
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
async def test_list_customers_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_customers(
            customers.ListCustomersRequest(),
            parent="parent_value",
        )


def test_list_customers_pager(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            customers.ListCustomersResponse(
                customers=[],
                next_page_token="def",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                ],
                next_page_token="ghi",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
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
        pager = client.list_customers(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, customers.Customer) for i in results)


def test_list_customers_pages(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_customers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            customers.ListCustomersResponse(
                customers=[],
                next_page_token="def",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                ],
                next_page_token="ghi",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_customers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_customers_async_pager():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_customers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            customers.ListCustomersResponse(
                customers=[],
                next_page_token="def",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                ],
                next_page_token="ghi",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_customers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, customers.Customer) for i in responses)


@pytest.mark.asyncio
async def test_list_customers_async_pages():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_customers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            customers.ListCustomersResponse(
                customers=[],
                next_page_token="def",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                ],
                next_page_token="ghi",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_customers(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        ekm_connections.GetEkmConnectionsRequest,
        dict,
    ],
)
def test_get_ekm_connections(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ekm_connections.EkmConnections(
            name="name_value",
        )
        response = client.get_ekm_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = ekm_connections.GetEkmConnectionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, ekm_connections.EkmConnections)
    assert response.name == "name_value"


def test_get_ekm_connections_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_ekm_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ekm_connections.GetEkmConnectionsRequest()


def test_get_ekm_connections_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = ekm_connections.GetEkmConnectionsRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_ekm_connections(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ekm_connections.GetEkmConnectionsRequest(
            name="name_value",
        )


def test_get_ekm_connections_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_ekm_connections in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_ekm_connections
        ] = mock_rpc
        request = {}
        client.get_ekm_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_ekm_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_ekm_connections_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ekm_connections.EkmConnections(
                name="name_value",
            )
        )
        response = await client.get_ekm_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ekm_connections.GetEkmConnectionsRequest()


@pytest.mark.asyncio
async def test_get_ekm_connections_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_ekm_connections
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_ekm_connections
        ] = mock_object

        request = {}
        await client.get_ekm_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_ekm_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_ekm_connections_async(
    transport: str = "grpc_asyncio",
    request_type=ekm_connections.GetEkmConnectionsRequest,
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ekm_connections.EkmConnections(
                name="name_value",
            )
        )
        response = await client.get_ekm_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = ekm_connections.GetEkmConnectionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, ekm_connections.EkmConnections)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_ekm_connections_async_from_dict():
    await test_get_ekm_connections_async(request_type=dict)


def test_get_ekm_connections_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ekm_connections.GetEkmConnectionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        call.return_value = ekm_connections.EkmConnections()
        client.get_ekm_connections(request)

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
async def test_get_ekm_connections_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ekm_connections.GetEkmConnectionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ekm_connections.EkmConnections()
        )
        await client.get_ekm_connections(request)

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


def test_get_ekm_connections_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ekm_connections.EkmConnections()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_ekm_connections(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_ekm_connections_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ekm_connections(
            ekm_connections.GetEkmConnectionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_ekm_connections_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ekm_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ekm_connections.EkmConnections()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ekm_connections.EkmConnections()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_ekm_connections(
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
async def test_get_ekm_connections_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_ekm_connections(
            ekm_connections.GetEkmConnectionsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        partner_permissions.GetPartnerPermissionsRequest,
        dict,
    ],
)
def test_get_partner_permissions(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = partner_permissions.PartnerPermissions(
            name="name_value",
            partner_permissions=[
                partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
            ],
        )
        response = client.get_partner_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = partner_permissions.GetPartnerPermissionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, partner_permissions.PartnerPermissions)
    assert response.name == "name_value"
    assert response.partner_permissions == [
        partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
    ]


def test_get_partner_permissions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_partner_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partner_permissions.GetPartnerPermissionsRequest()


def test_get_partner_permissions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = partner_permissions.GetPartnerPermissionsRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_partner_permissions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partner_permissions.GetPartnerPermissionsRequest(
            name="name_value",
        )


def test_get_partner_permissions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_partner_permissions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_partner_permissions
        ] = mock_rpc
        request = {}
        client.get_partner_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_partner_permissions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_partner_permissions_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partner_permissions.PartnerPermissions(
                name="name_value",
                partner_permissions=[
                    partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
                ],
            )
        )
        response = await client.get_partner_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partner_permissions.GetPartnerPermissionsRequest()


@pytest.mark.asyncio
async def test_get_partner_permissions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_partner_permissions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_partner_permissions
        ] = mock_object

        request = {}
        await client.get_partner_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_partner_permissions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_partner_permissions_async(
    transport: str = "grpc_asyncio",
    request_type=partner_permissions.GetPartnerPermissionsRequest,
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partner_permissions.PartnerPermissions(
                name="name_value",
                partner_permissions=[
                    partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
                ],
            )
        )
        response = await client.get_partner_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = partner_permissions.GetPartnerPermissionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, partner_permissions.PartnerPermissions)
    assert response.name == "name_value"
    assert response.partner_permissions == [
        partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
    ]


@pytest.mark.asyncio
async def test_get_partner_permissions_async_from_dict():
    await test_get_partner_permissions_async(request_type=dict)


def test_get_partner_permissions_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = partner_permissions.GetPartnerPermissionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        call.return_value = partner_permissions.PartnerPermissions()
        client.get_partner_permissions(request)

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
async def test_get_partner_permissions_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = partner_permissions.GetPartnerPermissionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partner_permissions.PartnerPermissions()
        )
        await client.get_partner_permissions(request)

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


def test_get_partner_permissions_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = partner_permissions.PartnerPermissions()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_partner_permissions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_partner_permissions_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_partner_permissions(
            partner_permissions.GetPartnerPermissionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_partner_permissions_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_partner_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = partner_permissions.PartnerPermissions()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partner_permissions.PartnerPermissions()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_partner_permissions(
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
async def test_get_partner_permissions_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_partner_permissions(
            partner_permissions.GetPartnerPermissionsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        access_approval_requests.ListAccessApprovalRequestsRequest,
        dict,
    ],
)
def test_list_access_approval_requests(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = access_approval_requests.ListAccessApprovalRequestsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_access_approval_requests(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = access_approval_requests.ListAccessApprovalRequestsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccessApprovalRequestsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_access_approval_requests_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_access_approval_requests()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == access_approval_requests.ListAccessApprovalRequestsRequest()


def test_list_access_approval_requests_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = access_approval_requests.ListAccessApprovalRequestsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_access_approval_requests(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == access_approval_requests.ListAccessApprovalRequestsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_access_approval_requests_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_access_approval_requests
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_access_approval_requests
        ] = mock_rpc
        request = {}
        client.list_access_approval_requests(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_access_approval_requests(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_access_approval_requests_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            access_approval_requests.ListAccessApprovalRequestsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_access_approval_requests()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == access_approval_requests.ListAccessApprovalRequestsRequest()


@pytest.mark.asyncio
async def test_list_access_approval_requests_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_access_approval_requests
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_access_approval_requests
        ] = mock_object

        request = {}
        await client.list_access_approval_requests(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_access_approval_requests(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_access_approval_requests_async(
    transport: str = "grpc_asyncio",
    request_type=access_approval_requests.ListAccessApprovalRequestsRequest,
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            access_approval_requests.ListAccessApprovalRequestsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_access_approval_requests(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = access_approval_requests.ListAccessApprovalRequestsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccessApprovalRequestsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_access_approval_requests_async_from_dict():
    await test_list_access_approval_requests_async(request_type=dict)


def test_list_access_approval_requests_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = access_approval_requests.ListAccessApprovalRequestsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        call.return_value = (
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )
        client.list_access_approval_requests(request)

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
async def test_list_access_approval_requests_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = access_approval_requests.ListAccessApprovalRequestsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )
        await client.list_access_approval_requests(request)

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


def test_list_access_approval_requests_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_access_approval_requests(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_access_approval_requests_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_access_approval_requests(
            access_approval_requests.ListAccessApprovalRequestsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_access_approval_requests_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_access_approval_requests(
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
async def test_list_access_approval_requests_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_access_approval_requests(
            access_approval_requests.ListAccessApprovalRequestsRequest(),
            parent="parent_value",
        )


def test_list_access_approval_requests_pager(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="abc",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[],
                next_page_token="def",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="ghi",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
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
        pager = client.list_access_approval_requests(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, access_approval_requests.AccessApprovalRequest)
            for i in results
        )


def test_list_access_approval_requests_pages(transport_name: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="abc",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[],
                next_page_token="def",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="ghi",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_access_approval_requests(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_access_approval_requests_async_pager():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="abc",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[],
                next_page_token="def",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="ghi",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_access_approval_requests(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, access_approval_requests.AccessApprovalRequest)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_access_approval_requests_async_pages():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_access_approval_requests),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="abc",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[],
                next_page_token="def",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="ghi",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_access_approval_requests(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        partners.GetPartnerRequest,
        dict,
    ],
)
def test_get_partner(request_type, transport: str = "grpc"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = partners.Partner(
            name="name_value",
            operated_cloud_regions=["operated_cloud_regions_value"],
            partner_project_id="partner_project_id_value",
        )
        response = client.get_partner(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = partners.GetPartnerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, partners.Partner)
    assert response.name == "name_value"
    assert response.operated_cloud_regions == ["operated_cloud_regions_value"]
    assert response.partner_project_id == "partner_project_id_value"


def test_get_partner_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_partner()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partners.GetPartnerRequest()


def test_get_partner_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = partners.GetPartnerRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_partner(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partners.GetPartnerRequest(
            name="name_value",
        )


def test_get_partner_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_partner in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_partner] = mock_rpc
        request = {}
        client.get_partner(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_partner(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_partner_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partners.Partner(
                name="name_value",
                operated_cloud_regions=["operated_cloud_regions_value"],
                partner_project_id="partner_project_id_value",
            )
        )
        response = await client.get_partner()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == partners.GetPartnerRequest()


@pytest.mark.asyncio
async def test_get_partner_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_partner
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_partner
        ] = mock_object

        request = {}
        await client.get_partner(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_partner(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_partner_async(
    transport: str = "grpc_asyncio", request_type=partners.GetPartnerRequest
):
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            partners.Partner(
                name="name_value",
                operated_cloud_regions=["operated_cloud_regions_value"],
                partner_project_id="partner_project_id_value",
            )
        )
        response = await client.get_partner(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = partners.GetPartnerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, partners.Partner)
    assert response.name == "name_value"
    assert response.operated_cloud_regions == ["operated_cloud_regions_value"]
    assert response.partner_project_id == "partner_project_id_value"


@pytest.mark.asyncio
async def test_get_partner_async_from_dict():
    await test_get_partner_async(request_type=dict)


def test_get_partner_field_headers():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = partners.GetPartnerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        call.return_value = partners.Partner()
        client.get_partner(request)

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
async def test_get_partner_field_headers_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = partners.GetPartnerRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(partners.Partner())
        await client.get_partner(request)

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


def test_get_partner_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = partners.Partner()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_partner(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_partner_flattened_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_partner(
            partners.GetPartnerRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_partner_flattened_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_partner), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = partners.Partner()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(partners.Partner())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_partner(
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
async def test_get_partner_flattened_error_async():
    client = CloudControlsPartnerCoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_partner(
            partners.GetPartnerRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        customer_workloads.GetWorkloadRequest,
        dict,
    ],
)
def test_get_workload_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customer_workloads.Workload(
            name="name_value",
            folder_id=936,
            folder="folder_value",
            is_onboarded=True,
            key_management_project_id="key_management_project_id_value",
            location="location_value",
            partner=customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = customer_workloads.Workload.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_workload(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, customer_workloads.Workload)
    assert response.name == "name_value"
    assert response.folder_id == 936
    assert response.folder == "folder_value"
    assert response.is_onboarded is True
    assert response.key_management_project_id == "key_management_project_id_value"
    assert response.location == "location_value"
    assert (
        response.partner
        == customer_workloads.Workload.Partner.PARTNER_LOCAL_CONTROLS_BY_S3NS
    )


def test_get_workload_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_workload in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_workload] = mock_rpc

        request = {}
        client.get_workload(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_workload(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_workload_rest_required_fields(
    request_type=customer_workloads.GetWorkloadRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).get_workload._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_workload._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = customer_workloads.Workload()
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
            return_value = customer_workloads.Workload.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_workload(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_workload_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_workload._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_workload_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_get_workload"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_get_workload"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = customer_workloads.GetWorkloadRequest.pb(
            customer_workloads.GetWorkloadRequest()
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
        req.return_value._content = customer_workloads.Workload.to_json(
            customer_workloads.Workload()
        )

        request = customer_workloads.GetWorkloadRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = customer_workloads.Workload()

        client.get_workload(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_workload_rest_bad_request(
    transport: str = "rest", request_type=customer_workloads.GetWorkloadRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
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
        client.get_workload(request)


def test_get_workload_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customer_workloads.Workload()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
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
        return_value = customer_workloads.Workload.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_workload(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/customers/*/workloads/*}"
            % client.transport._host,
            args[1],
        )


def test_get_workload_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workload(
            customer_workloads.GetWorkloadRequest(),
            name="name_value",
        )


def test_get_workload_rest_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        customer_workloads.ListWorkloadsRequest,
        dict,
    ],
)
def test_list_workloads_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/customers/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customer_workloads.ListWorkloadsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = customer_workloads.ListWorkloadsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_workloads(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkloadsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_workloads_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_workloads in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_workloads] = mock_rpc

        request = {}
        client.list_workloads(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_workloads(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_workloads_rest_required_fields(
    request_type=customer_workloads.ListWorkloadsRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).list_workloads._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_workloads._get_unset_required_fields(jsonified_request)
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

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = customer_workloads.ListWorkloadsResponse()
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
            return_value = customer_workloads.ListWorkloadsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_workloads(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_workloads_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_workloads._get_unset_required_fields({})
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
def test_list_workloads_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_list_workloads"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_list_workloads"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = customer_workloads.ListWorkloadsRequest.pb(
            customer_workloads.ListWorkloadsRequest()
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
        req.return_value._content = customer_workloads.ListWorkloadsResponse.to_json(
            customer_workloads.ListWorkloadsResponse()
        )

        request = customer_workloads.ListWorkloadsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = customer_workloads.ListWorkloadsResponse()

        client.list_workloads(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_workloads_rest_bad_request(
    transport: str = "rest", request_type=customer_workloads.ListWorkloadsRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/customers/sample3"
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
        client.list_workloads(request)


def test_list_workloads_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customer_workloads.ListWorkloadsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "organizations/sample1/locations/sample2/customers/sample3"
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
        return_value = customer_workloads.ListWorkloadsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_workloads(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*/customers/*}/workloads"
            % client.transport._host,
            args[1],
        )


def test_list_workloads_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workloads(
            customer_workloads.ListWorkloadsRequest(),
            parent="parent_value",
        )


def test_list_workloads_rest_pager(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
                next_page_token="abc",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[],
                next_page_token="def",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                ],
                next_page_token="ghi",
            ),
            customer_workloads.ListWorkloadsResponse(
                workloads=[
                    customer_workloads.Workload(),
                    customer_workloads.Workload(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            customer_workloads.ListWorkloadsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "organizations/sample1/locations/sample2/customers/sample3"
        }

        pager = client.list_workloads(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, customer_workloads.Workload) for i in results)

        pages = list(client.list_workloads(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        customers.GetCustomerRequest,
        dict,
    ],
)
def test_get_customer_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/locations/sample2/customers/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customers.Customer(
            name="name_value",
            display_name="display_name_value",
            is_onboarded=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = customers.Customer.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_customer(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, customers.Customer)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_onboarded is True


def test_get_customer_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_customer in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_customer] = mock_rpc

        request = {}
        client.get_customer(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_customer(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_customer_rest_required_fields(request_type=customers.GetCustomerRequest):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).get_customer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_customer._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = customers.Customer()
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
            return_value = customers.Customer.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_customer(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_customer_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_customer._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_customer_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_get_customer"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_get_customer"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = customers.GetCustomerRequest.pb(customers.GetCustomerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = customers.Customer.to_json(customers.Customer())

        request = customers.GetCustomerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = customers.Customer()

        client.get_customer(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_customer_rest_bad_request(
    transport: str = "rest", request_type=customers.GetCustomerRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/locations/sample2/customers/sample3"}
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
        client.get_customer(request)


def test_get_customer_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customers.Customer()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "organizations/sample1/locations/sample2/customers/sample3"
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
        return_value = customers.Customer.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_customer(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/customers/*}"
            % client.transport._host,
            args[1],
        )


def test_get_customer_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_customer(
            customers.GetCustomerRequest(),
            name="name_value",
        )


def test_get_customer_rest_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        customers.ListCustomersRequest,
        dict,
    ],
)
def test_list_customers_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customers.ListCustomersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = customers.ListCustomersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_customers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_customers_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_customers in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_customers] = mock_rpc

        request = {}
        client.list_customers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_customers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_customers_rest_required_fields(
    request_type=customers.ListCustomersRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).list_customers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_customers._get_unset_required_fields(jsonified_request)
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

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = customers.ListCustomersResponse()
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
            return_value = customers.ListCustomersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_customers(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_customers_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_customers._get_unset_required_fields({})
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
def test_list_customers_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_list_customers"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_list_customers"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = customers.ListCustomersRequest.pb(customers.ListCustomersRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = customers.ListCustomersResponse.to_json(
            customers.ListCustomersResponse()
        )

        request = customers.ListCustomersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = customers.ListCustomersResponse()

        client.list_customers(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_customers_rest_bad_request(
    transport: str = "rest", request_type=customers.ListCustomersRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "organizations/sample1/locations/sample2"}
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
        client.list_customers(request)


def test_list_customers_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = customers.ListCustomersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "organizations/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = customers.ListCustomersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_customers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*}/customers"
            % client.transport._host,
            args[1],
        )


def test_list_customers_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_customers(
            customers.ListCustomersRequest(),
            parent="parent_value",
        )


def test_list_customers_rest_pager(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                    customers.Customer(),
                ],
                next_page_token="abc",
            ),
            customers.ListCustomersResponse(
                customers=[],
                next_page_token="def",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                ],
                next_page_token="ghi",
            ),
            customers.ListCustomersResponse(
                customers=[
                    customers.Customer(),
                    customers.Customer(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(customers.ListCustomersResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "organizations/sample1/locations/sample2"}

        pager = client.list_customers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, customers.Customer) for i in results)

        pages = list(client.list_customers(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        ekm_connections.GetEkmConnectionsRequest,
        dict,
    ],
)
def test_get_ekm_connections_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/ekmConnections"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ekm_connections.EkmConnections(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = ekm_connections.EkmConnections.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_ekm_connections(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, ekm_connections.EkmConnections)
    assert response.name == "name_value"


def test_get_ekm_connections_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_ekm_connections in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_ekm_connections
        ] = mock_rpc

        request = {}
        client.get_ekm_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_ekm_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_ekm_connections_rest_required_fields(
    request_type=ekm_connections.GetEkmConnectionsRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).get_ekm_connections._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_ekm_connections._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = ekm_connections.EkmConnections()
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
            return_value = ekm_connections.EkmConnections.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_ekm_connections(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_ekm_connections_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_ekm_connections._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_ekm_connections_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_get_ekm_connections"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_get_ekm_connections"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = ekm_connections.GetEkmConnectionsRequest.pb(
            ekm_connections.GetEkmConnectionsRequest()
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
        req.return_value._content = ekm_connections.EkmConnections.to_json(
            ekm_connections.EkmConnections()
        )

        request = ekm_connections.GetEkmConnectionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = ekm_connections.EkmConnections()

        client.get_ekm_connections(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_ekm_connections_rest_bad_request(
    transport: str = "rest", request_type=ekm_connections.GetEkmConnectionsRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/ekmConnections"
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
        client.get_ekm_connections(request)


def test_get_ekm_connections_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ekm_connections.EkmConnections()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/ekmConnections"
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
        return_value = ekm_connections.EkmConnections.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_ekm_connections(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/customers/*/workloads/*/ekmConnections}"
            % client.transport._host,
            args[1],
        )


def test_get_ekm_connections_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ekm_connections(
            ekm_connections.GetEkmConnectionsRequest(),
            name="name_value",
        )


def test_get_ekm_connections_rest_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        partner_permissions.GetPartnerPermissionsRequest,
        dict,
    ],
)
def test_get_partner_permissions_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/partnerPermissions"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = partner_permissions.PartnerPermissions(
            name="name_value",
            partner_permissions=[
                partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
            ],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = partner_permissions.PartnerPermissions.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_partner_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, partner_permissions.PartnerPermissions)
    assert response.name == "name_value"
    assert response.partner_permissions == [
        partner_permissions.PartnerPermissions.Permission.ACCESS_TRANSPARENCY_AND_EMERGENCY_ACCESS_LOGS
    ]


def test_get_partner_permissions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_partner_permissions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_partner_permissions
        ] = mock_rpc

        request = {}
        client.get_partner_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_partner_permissions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_partner_permissions_rest_required_fields(
    request_type=partner_permissions.GetPartnerPermissionsRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).get_partner_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_partner_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = partner_permissions.PartnerPermissions()
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
            return_value = partner_permissions.PartnerPermissions.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_partner_permissions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_partner_permissions_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_partner_permissions._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_partner_permissions_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor,
        "post_get_partner_permissions",
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor,
        "pre_get_partner_permissions",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = partner_permissions.GetPartnerPermissionsRequest.pb(
            partner_permissions.GetPartnerPermissionsRequest()
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
        req.return_value._content = partner_permissions.PartnerPermissions.to_json(
            partner_permissions.PartnerPermissions()
        )

        request = partner_permissions.GetPartnerPermissionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = partner_permissions.PartnerPermissions()

        client.get_partner_permissions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_partner_permissions_rest_bad_request(
    transport: str = "rest",
    request_type=partner_permissions.GetPartnerPermissionsRequest,
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/partnerPermissions"
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
        client.get_partner_permissions(request)


def test_get_partner_permissions_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = partner_permissions.PartnerPermissions()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4/partnerPermissions"
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
        return_value = partner_permissions.PartnerPermissions.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_partner_permissions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/customers/*/workloads/*/partnerPermissions}"
            % client.transport._host,
            args[1],
        )


def test_get_partner_permissions_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_partner_permissions(
            partner_permissions.GetPartnerPermissionsRequest(),
            name="name_value",
        )


def test_get_partner_permissions_rest_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        access_approval_requests.ListAccessApprovalRequestsRequest,
        dict,
    ],
)
def test_list_access_approval_requests_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = access_approval_requests.ListAccessApprovalRequestsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = access_approval_requests.ListAccessApprovalRequestsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_access_approval_requests(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAccessApprovalRequestsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_access_approval_requests_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_access_approval_requests
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_access_approval_requests
        ] = mock_rpc

        request = {}
        client.list_access_approval_requests(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_access_approval_requests(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_access_approval_requests_rest_required_fields(
    request_type=access_approval_requests.ListAccessApprovalRequestsRequest,
):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).list_access_approval_requests._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_access_approval_requests._get_unset_required_fields(jsonified_request)
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

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = access_approval_requests.ListAccessApprovalRequestsResponse()
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
            return_value = (
                access_approval_requests.ListAccessApprovalRequestsResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_access_approval_requests(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_access_approval_requests_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_access_approval_requests._get_unset_required_fields(
        {}
    )
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
def test_list_access_approval_requests_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor,
        "post_list_access_approval_requests",
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor,
        "pre_list_access_approval_requests",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = access_approval_requests.ListAccessApprovalRequestsRequest.pb(
            access_approval_requests.ListAccessApprovalRequestsRequest()
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
            access_approval_requests.ListAccessApprovalRequestsResponse.to_json(
                access_approval_requests.ListAccessApprovalRequestsResponse()
            )
        )

        request = access_approval_requests.ListAccessApprovalRequestsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            access_approval_requests.ListAccessApprovalRequestsResponse()
        )

        client.list_access_approval_requests(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_access_approval_requests_rest_bad_request(
    transport: str = "rest",
    request_type=access_approval_requests.ListAccessApprovalRequestsRequest,
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
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
        client.list_access_approval_requests(request)


def test_list_access_approval_requests_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = access_approval_requests.ListAccessApprovalRequestsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
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
        return_value = access_approval_requests.ListAccessApprovalRequestsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_access_approval_requests(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=organizations/*/locations/*/customers/*/workloads/*}/accessApprovalRequests"
            % client.transport._host,
            args[1],
        )


def test_list_access_approval_requests_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_access_approval_requests(
            access_approval_requests.ListAccessApprovalRequestsRequest(),
            parent="parent_value",
        )


def test_list_access_approval_requests_rest_pager(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="abc",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[],
                next_page_token="def",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                ],
                next_page_token="ghi",
            ),
            access_approval_requests.ListAccessApprovalRequestsResponse(
                access_approval_requests=[
                    access_approval_requests.AccessApprovalRequest(),
                    access_approval_requests.AccessApprovalRequest(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            access_approval_requests.ListAccessApprovalRequestsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "organizations/sample1/locations/sample2/customers/sample3/workloads/sample4"
        }

        pager = client.list_access_approval_requests(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, access_approval_requests.AccessApprovalRequest)
            for i in results
        )

        pages = list(client.list_access_approval_requests(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        partners.GetPartnerRequest,
        dict,
    ],
)
def test_get_partner_rest(request_type):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/locations/sample2/partner"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = partners.Partner(
            name="name_value",
            operated_cloud_regions=["operated_cloud_regions_value"],
            partner_project_id="partner_project_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = partners.Partner.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_partner(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, partners.Partner)
    assert response.name == "name_value"
    assert response.operated_cloud_regions == ["operated_cloud_regions_value"]
    assert response.partner_project_id == "partner_project_id_value"


def test_get_partner_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_partner in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_partner] = mock_rpc

        request = {}
        client.get_partner(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_partner(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_partner_rest_required_fields(request_type=partners.GetPartnerRequest):
    transport_class = transports.CloudControlsPartnerCoreRestTransport

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
    ).get_partner._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_partner._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = partners.Partner()
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
            return_value = partners.Partner.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_partner(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_partner_rest_unset_required_fields():
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_partner._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_partner_rest_interceptors(null_interceptor):
    transport = transports.CloudControlsPartnerCoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudControlsPartnerCoreRestInterceptor(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "post_get_partner"
    ) as post, mock.patch.object(
        transports.CloudControlsPartnerCoreRestInterceptor, "pre_get_partner"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = partners.GetPartnerRequest.pb(partners.GetPartnerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = partners.Partner.to_json(partners.Partner())

        request = partners.GetPartnerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = partners.Partner()

        client.get_partner(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_partner_rest_bad_request(
    transport: str = "rest", request_type=partners.GetPartnerRequest
):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "organizations/sample1/locations/sample2/partner"}
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
        client.get_partner(request)


def test_get_partner_rest_flattened():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = partners.Partner()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "organizations/sample1/locations/sample2/partner"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = partners.Partner.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_partner(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=organizations/*/locations/*/partner}" % client.transport._host,
            args[1],
        )


def test_get_partner_rest_flattened_error(transport: str = "rest"):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_partner(
            partners.GetPartnerRequest(),
            name="name_value",
        )


def test_get_partner_rest_error():
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudControlsPartnerCoreClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudControlsPartnerCoreClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudControlsPartnerCoreClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudControlsPartnerCoreClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudControlsPartnerCoreClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudControlsPartnerCoreGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
        transports.CloudControlsPartnerCoreRestTransport,
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
    transport = CloudControlsPartnerCoreClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudControlsPartnerCoreGrpcTransport,
    )


def test_cloud_controls_partner_core_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudControlsPartnerCoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_controls_partner_core_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.cloudcontrolspartner_v1.services.cloud_controls_partner_core.transports.CloudControlsPartnerCoreTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudControlsPartnerCoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_workload",
        "list_workloads",
        "get_customer",
        "list_customers",
        "get_ekm_connections",
        "get_partner_permissions",
        "list_access_approval_requests",
        "get_partner",
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


def test_cloud_controls_partner_core_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.cloudcontrolspartner_v1.services.cloud_controls_partner_core.transports.CloudControlsPartnerCoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudControlsPartnerCoreTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_controls_partner_core_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.cloudcontrolspartner_v1.services.cloud_controls_partner_core.transports.CloudControlsPartnerCoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudControlsPartnerCoreTransport()
        adc.assert_called_once()


def test_cloud_controls_partner_core_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudControlsPartnerCoreClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
    ],
)
def test_cloud_controls_partner_core_transport_auth_adc(transport_class):
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
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
        transports.CloudControlsPartnerCoreRestTransport,
    ],
)
def test_cloud_controls_partner_core_transport_auth_gdch_credentials(transport_class):
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
        (transports.CloudControlsPartnerCoreGrpcTransport, grpc_helpers),
        (transports.CloudControlsPartnerCoreGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_controls_partner_core_transport_create_channel(
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
            "cloudcontrolspartner.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="cloudcontrolspartner.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
    ],
)
def test_cloud_controls_partner_core_grpc_transport_client_cert_source_for_mtls(
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


def test_cloud_controls_partner_core_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CloudControlsPartnerCoreRestTransport(
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
def test_cloud_controls_partner_core_host_no_port(transport_name):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudcontrolspartner.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudcontrolspartner.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudcontrolspartner.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_controls_partner_core_host_with_port(transport_name):
    client = CloudControlsPartnerCoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudcontrolspartner.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudcontrolspartner.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudcontrolspartner.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_cloud_controls_partner_core_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = CloudControlsPartnerCoreClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CloudControlsPartnerCoreClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_workload._session
    session2 = client2.transport.get_workload._session
    assert session1 != session2
    session1 = client1.transport.list_workloads._session
    session2 = client2.transport.list_workloads._session
    assert session1 != session2
    session1 = client1.transport.get_customer._session
    session2 = client2.transport.get_customer._session
    assert session1 != session2
    session1 = client1.transport.list_customers._session
    session2 = client2.transport.list_customers._session
    assert session1 != session2
    session1 = client1.transport.get_ekm_connections._session
    session2 = client2.transport.get_ekm_connections._session
    assert session1 != session2
    session1 = client1.transport.get_partner_permissions._session
    session2 = client2.transport.get_partner_permissions._session
    assert session1 != session2
    session1 = client1.transport.list_access_approval_requests._session
    session2 = client2.transport.list_access_approval_requests._session
    assert session1 != session2
    session1 = client1.transport.get_partner._session
    session2 = client2.transport.get_partner._session
    assert session1 != session2


def test_cloud_controls_partner_core_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudControlsPartnerCoreGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_controls_partner_core_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudControlsPartnerCoreGrpcAsyncIOTransport(
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
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
    ],
)
def test_cloud_controls_partner_core_transport_channel_mtls_with_client_cert_source(
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
        transports.CloudControlsPartnerCoreGrpcTransport,
        transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
    ],
)
def test_cloud_controls_partner_core_transport_channel_mtls_with_adc(transport_class):
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


def test_access_approval_request_path():
    organization = "squid"
    location = "clam"
    customer = "whelk"
    workload = "octopus"
    access_approval_request = "oyster"
    expected = "organizations/{organization}/locations/{location}/customers/{customer}/workloads/{workload}/accessApprovalRequests/{access_approval_request}".format(
        organization=organization,
        location=location,
        customer=customer,
        workload=workload,
        access_approval_request=access_approval_request,
    )
    actual = CloudControlsPartnerCoreClient.access_approval_request_path(
        organization, location, customer, workload, access_approval_request
    )
    assert expected == actual


def test_parse_access_approval_request_path():
    expected = {
        "organization": "nudibranch",
        "location": "cuttlefish",
        "customer": "mussel",
        "workload": "winkle",
        "access_approval_request": "nautilus",
    }
    path = CloudControlsPartnerCoreClient.access_approval_request_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_access_approval_request_path(path)
    assert expected == actual


def test_customer_path():
    organization = "scallop"
    location = "abalone"
    customer = "squid"
    expected = (
        "organizations/{organization}/locations/{location}/customers/{customer}".format(
            organization=organization,
            location=location,
            customer=customer,
        )
    )
    actual = CloudControlsPartnerCoreClient.customer_path(
        organization, location, customer
    )
    assert expected == actual


def test_parse_customer_path():
    expected = {
        "organization": "clam",
        "location": "whelk",
        "customer": "octopus",
    }
    path = CloudControlsPartnerCoreClient.customer_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_customer_path(path)
    assert expected == actual


def test_ekm_connections_path():
    organization = "oyster"
    location = "nudibranch"
    customer = "cuttlefish"
    workload = "mussel"
    expected = "organizations/{organization}/locations/{location}/customers/{customer}/workloads/{workload}/ekmConnections".format(
        organization=organization,
        location=location,
        customer=customer,
        workload=workload,
    )
    actual = CloudControlsPartnerCoreClient.ekm_connections_path(
        organization, location, customer, workload
    )
    assert expected == actual


def test_parse_ekm_connections_path():
    expected = {
        "organization": "winkle",
        "location": "nautilus",
        "customer": "scallop",
        "workload": "abalone",
    }
    path = CloudControlsPartnerCoreClient.ekm_connections_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_ekm_connections_path(path)
    assert expected == actual


def test_partner_path():
    organization = "squid"
    location = "clam"
    expected = "organizations/{organization}/locations/{location}/partner".format(
        organization=organization,
        location=location,
    )
    actual = CloudControlsPartnerCoreClient.partner_path(organization, location)
    assert expected == actual


def test_parse_partner_path():
    expected = {
        "organization": "whelk",
        "location": "octopus",
    }
    path = CloudControlsPartnerCoreClient.partner_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_partner_path(path)
    assert expected == actual


def test_partner_permissions_path():
    organization = "oyster"
    location = "nudibranch"
    customer = "cuttlefish"
    workload = "mussel"
    expected = "organizations/{organization}/locations/{location}/customers/{customer}/workloads/{workload}/partnerPermissions".format(
        organization=organization,
        location=location,
        customer=customer,
        workload=workload,
    )
    actual = CloudControlsPartnerCoreClient.partner_permissions_path(
        organization, location, customer, workload
    )
    assert expected == actual


def test_parse_partner_permissions_path():
    expected = {
        "organization": "winkle",
        "location": "nautilus",
        "customer": "scallop",
        "workload": "abalone",
    }
    path = CloudControlsPartnerCoreClient.partner_permissions_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_partner_permissions_path(path)
    assert expected == actual


def test_workload_path():
    organization = "squid"
    location = "clam"
    customer = "whelk"
    workload = "octopus"
    expected = "organizations/{organization}/locations/{location}/customers/{customer}/workloads/{workload}".format(
        organization=organization,
        location=location,
        customer=customer,
        workload=workload,
    )
    actual = CloudControlsPartnerCoreClient.workload_path(
        organization, location, customer, workload
    )
    assert expected == actual


def test_parse_workload_path():
    expected = {
        "organization": "oyster",
        "location": "nudibranch",
        "customer": "cuttlefish",
        "workload": "mussel",
    }
    path = CloudControlsPartnerCoreClient.workload_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_workload_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudControlsPartnerCoreClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = CloudControlsPartnerCoreClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudControlsPartnerCoreClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = CloudControlsPartnerCoreClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudControlsPartnerCoreClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = CloudControlsPartnerCoreClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudControlsPartnerCoreClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = CloudControlsPartnerCoreClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudControlsPartnerCoreClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = CloudControlsPartnerCoreClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudControlsPartnerCoreClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudControlsPartnerCoreTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudControlsPartnerCoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudControlsPartnerCoreTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudControlsPartnerCoreClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudControlsPartnerCoreAsyncClient(
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
        client = CloudControlsPartnerCoreClient(
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
        client = CloudControlsPartnerCoreClient(
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
            CloudControlsPartnerCoreClient,
            transports.CloudControlsPartnerCoreGrpcTransport,
        ),
        (
            CloudControlsPartnerCoreAsyncClient,
            transports.CloudControlsPartnerCoreGrpcAsyncIOTransport,
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
