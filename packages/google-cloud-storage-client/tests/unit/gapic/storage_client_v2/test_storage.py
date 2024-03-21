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

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.storage_client_v2.services.storage import (
    StorageAsyncClient,
    StorageClient,
    pagers,
    transports,
)
from google.cloud.storage_client_v2.types import storage


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

    assert StorageClient._get_default_mtls_endpoint(None) is None
    assert StorageClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        StorageClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        StorageClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        StorageClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert StorageClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert StorageClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert StorageClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert StorageClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            StorageClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert StorageClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert StorageClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert StorageClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            StorageClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert StorageClient._read_environment_variables() == (False, "auto", "foo.com")


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert StorageClient._get_client_cert_source(None, False) is None
    assert (
        StorageClient._get_client_cert_source(mock_provided_cert_source, False) is None
    )
    assert (
        StorageClient._get_client_cert_source(mock_provided_cert_source, True)
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
                StorageClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                StorageClient._get_client_cert_source(mock_provided_cert_source, "true")
                is mock_provided_cert_source
            )


@mock.patch.object(
    StorageClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageClient),
)
@mock.patch.object(
    StorageAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = StorageClient._DEFAULT_UNIVERSE
    default_endpoint = StorageClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = StorageClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        StorageClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        StorageClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == StorageClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        StorageClient._get_api_endpoint(None, None, default_universe, "always")
        == StorageClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == StorageClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        StorageClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        StorageClient._get_api_endpoint(
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
        StorageClient._get_universe_domain(client_universe_domain, universe_domain_env)
        == client_universe_domain
    )
    assert (
        StorageClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        StorageClient._get_universe_domain(None, None)
        == StorageClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        StorageClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (StorageClient, transports.StorageGrpcTransport, "grpc"),
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
        (StorageClient, "grpc"),
        (StorageAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("storage.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.StorageGrpcTransport, "grpc"),
        (transports.StorageGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_storage_client_service_account_always_use_jwt(transport_class, transport_name):
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
        (StorageClient, "grpc"),
        (StorageAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("storage.googleapis.com:443")


def test_storage_client_get_transport_class():
    transport = StorageClient.get_transport_class()
    available_transports = [
        transports.StorageGrpcTransport,
    ]
    assert transport in available_transports

    transport = StorageClient.get_transport_class("grpc")
    assert transport == transports.StorageGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (StorageClient, transports.StorageGrpcTransport, "grpc"),
        (StorageAsyncClient, transports.StorageGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    StorageClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageClient),
)
@mock.patch.object(
    StorageAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageAsyncClient),
)
def test_storage_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(StorageClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(StorageClient, "get_transport_class") as gtc:
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
        (StorageClient, transports.StorageGrpcTransport, "grpc", "true"),
        (
            StorageAsyncClient,
            transports.StorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (StorageClient, transports.StorageGrpcTransport, "grpc", "false"),
        (
            StorageAsyncClient,
            transports.StorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    StorageClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageClient),
)
@mock.patch.object(
    StorageAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_storage_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [StorageClient, StorageAsyncClient])
@mock.patch.object(
    StorageClient, "DEFAULT_ENDPOINT", modify_default_endpoint(StorageClient)
)
@mock.patch.object(
    StorageAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(StorageAsyncClient)
)
def test_storage_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize("client_class", [StorageClient, StorageAsyncClient])
@mock.patch.object(
    StorageClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageClient),
)
@mock.patch.object(
    StorageAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageAsyncClient),
)
def test_storage_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = StorageClient._DEFAULT_UNIVERSE
    default_endpoint = StorageClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = StorageClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (StorageClient, transports.StorageGrpcTransport, "grpc"),
        (StorageAsyncClient, transports.StorageGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_storage_client_client_options_scopes(
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
        (StorageClient, transports.StorageGrpcTransport, "grpc", grpc_helpers),
        (
            StorageAsyncClient,
            transports.StorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_client_client_options_credentials_file(
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


def test_storage_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.storage_client_v2.services.storage.transports.StorageGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = StorageClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (StorageClient, transports.StorageGrpcTransport, "grpc", grpc_helpers),
        (
            StorageAsyncClient,
            transports.StorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_client_create_channel_credentials_file(
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
            "storage.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            scopes=None,
            default_host="storage.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.DeleteBucketRequest,
        dict,
    ],
)
def test_delete_bucket(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        client.delete_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteBucketRequest()


@pytest.mark.asyncio
async def test_delete_bucket_async(
    transport: str = "grpc_asyncio", request_type=storage.DeleteBucketRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteBucketRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_bucket_async_from_dict():
    await test_delete_bucket_async(request_type=dict)


def test_delete_bucket_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.DeleteBucketRequest(**{"name": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        call.return_value = None
        client.delete_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_bucket_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_bucket(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_bucket_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_bucket(
            storage.DeleteBucketRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_bucket_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_bucket(
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
async def test_delete_bucket_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_bucket(
            storage.DeleteBucketRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.GetBucketRequest,
        dict,
    ],
)
def test_get_bucket(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket(
            name="name_value",
            bucket_id="bucket_id_value",
            etag="etag_value",
            project="project_value",
            metageneration=1491,
            location="location_value",
            location_type="location_type_value",
            storage_class="storage_class_value",
            rpo="rpo_value",
            default_event_based_hold=True,
            satisfies_pzs=True,
        )
        response = client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


def test_get_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        client.get_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetBucketRequest()


@pytest.mark.asyncio
async def test_get_bucket_async(
    transport: str = "grpc_asyncio", request_type=storage.GetBucketRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Bucket(
                name="name_value",
                bucket_id="bucket_id_value",
                etag="etag_value",
                project="project_value",
                metageneration=1491,
                location="location_value",
                location_type="location_type_value",
                storage_class="storage_class_value",
                rpo="rpo_value",
                default_event_based_hold=True,
                satisfies_pzs=True,
            )
        )
        response = await client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


@pytest.mark.asyncio
async def test_get_bucket_async_from_dict():
    await test_get_bucket_async(request_type=dict)


def test_get_bucket_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetBucketRequest(**{"name": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        call.return_value = storage.Bucket()
        client.get_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_bucket_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_bucket(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_bucket_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_bucket(
            storage.GetBucketRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_bucket_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Bucket())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_bucket(
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
async def test_get_bucket_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_bucket(
            storage.GetBucketRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.CreateBucketRequest,
        dict,
    ],
)
def test_create_bucket(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket(
            name="name_value",
            bucket_id="bucket_id_value",
            etag="etag_value",
            project="project_value",
            metageneration=1491,
            location="location_value",
            location_type="location_type_value",
            storage_class="storage_class_value",
            rpo="rpo_value",
            default_event_based_hold=True,
            satisfies_pzs=True,
        )
        response = client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


def test_create_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        client.create_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateBucketRequest()


@pytest.mark.asyncio
async def test_create_bucket_async(
    transport: str = "grpc_asyncio", request_type=storage.CreateBucketRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Bucket(
                name="name_value",
                bucket_id="bucket_id_value",
                etag="etag_value",
                project="project_value",
                metageneration=1491,
                location="location_value",
                location_type="location_type_value",
                storage_class="storage_class_value",
                rpo="rpo_value",
                default_event_based_hold=True,
                satisfies_pzs=True,
            )
        )
        response = await client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


@pytest.mark.asyncio
async def test_create_bucket_async_from_dict():
    await test_create_bucket_async(request_type=dict)


def test_create_bucket_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateBucketRequest(**{"parent": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        call.return_value = storage.Bucket()
        client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateBucketRequest(**{"bucket": {"project": "sample1"}})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        call.return_value = storage.Bucket()
        client.create_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_bucket_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_bucket(
            parent="parent_value",
            bucket=storage.Bucket(name="name_value"),
            bucket_id="bucket_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].bucket
        mock_val = storage.Bucket(name="name_value")
        assert arg == mock_val
        arg = args[0].bucket_id
        mock_val = "bucket_id_value"
        assert arg == mock_val


def test_create_bucket_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_bucket(
            storage.CreateBucketRequest(),
            parent="parent_value",
            bucket=storage.Bucket(name="name_value"),
            bucket_id="bucket_id_value",
        )


@pytest.mark.asyncio
async def test_create_bucket_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Bucket())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_bucket(
            parent="parent_value",
            bucket=storage.Bucket(name="name_value"),
            bucket_id="bucket_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].bucket
        mock_val = storage.Bucket(name="name_value")
        assert arg == mock_val
        arg = args[0].bucket_id
        mock_val = "bucket_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_bucket_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_bucket(
            storage.CreateBucketRequest(),
            parent="parent_value",
            bucket=storage.Bucket(name="name_value"),
            bucket_id="bucket_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ListBucketsRequest,
        dict,
    ],
)
def test_list_buckets(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListBucketsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_buckets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListBucketsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBucketsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_buckets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        client.list_buckets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListBucketsRequest()


@pytest.mark.asyncio
async def test_list_buckets_async(
    transport: str = "grpc_asyncio", request_type=storage.ListBucketsRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListBucketsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_buckets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListBucketsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBucketsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_buckets_async_from_dict():
    await test_list_buckets_async(request_type=dict)


def test_list_buckets_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ListBucketsRequest(**{"parent": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        call.return_value = storage.ListBucketsResponse()
        client.list_buckets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_buckets_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListBucketsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_buckets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_buckets_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_buckets(
            storage.ListBucketsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_buckets_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListBucketsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListBucketsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_buckets(
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
async def test_list_buckets_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_buckets(
            storage.ListBucketsRequest(),
            parent="parent_value",
        )


def test_list_buckets_pager(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                    storage.Bucket(),
                ],
                next_page_token="abc",
            ),
            storage.ListBucketsResponse(
                buckets=[],
                next_page_token="def",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                ],
                next_page_token="ghi",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_buckets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage.Bucket) for i in results)


def test_list_buckets_pages(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_buckets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                    storage.Bucket(),
                ],
                next_page_token="abc",
            ),
            storage.ListBucketsResponse(
                buckets=[],
                next_page_token="def",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                ],
                next_page_token="ghi",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_buckets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_buckets_async_pager():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_buckets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                    storage.Bucket(),
                ],
                next_page_token="abc",
            ),
            storage.ListBucketsResponse(
                buckets=[],
                next_page_token="def",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                ],
                next_page_token="ghi",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_buckets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage.Bucket) for i in responses)


@pytest.mark.asyncio
async def test_list_buckets_async_pages():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_buckets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                    storage.Bucket(),
                ],
                next_page_token="abc",
            ),
            storage.ListBucketsResponse(
                buckets=[],
                next_page_token="def",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                ],
                next_page_token="ghi",
            ),
            storage.ListBucketsResponse(
                buckets=[
                    storage.Bucket(),
                    storage.Bucket(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_buckets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage.LockBucketRetentionPolicyRequest,
        dict,
    ],
)
def test_lock_bucket_retention_policy(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket(
            name="name_value",
            bucket_id="bucket_id_value",
            etag="etag_value",
            project="project_value",
            metageneration=1491,
            location="location_value",
            location_type="location_type_value",
            storage_class="storage_class_value",
            rpo="rpo_value",
            default_event_based_hold=True,
            satisfies_pzs=True,
        )
        response = client.lock_bucket_retention_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.LockBucketRetentionPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


def test_lock_bucket_retention_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        client.lock_bucket_retention_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.LockBucketRetentionPolicyRequest()


@pytest.mark.asyncio
async def test_lock_bucket_retention_policy_async(
    transport: str = "grpc_asyncio",
    request_type=storage.LockBucketRetentionPolicyRequest,
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Bucket(
                name="name_value",
                bucket_id="bucket_id_value",
                etag="etag_value",
                project="project_value",
                metageneration=1491,
                location="location_value",
                location_type="location_type_value",
                storage_class="storage_class_value",
                rpo="rpo_value",
                default_event_based_hold=True,
                satisfies_pzs=True,
            )
        )
        response = await client.lock_bucket_retention_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.LockBucketRetentionPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


@pytest.mark.asyncio
async def test_lock_bucket_retention_policy_async_from_dict():
    await test_lock_bucket_retention_policy_async(request_type=dict)


def test_lock_bucket_retention_policy_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.LockBucketRetentionPolicyRequest(**{"bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        call.return_value = storage.Bucket()
        client.lock_bucket_retention_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_lock_bucket_retention_policy_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.lock_bucket_retention_policy(
            bucket="bucket_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val


def test_lock_bucket_retention_policy_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.lock_bucket_retention_policy(
            storage.LockBucketRetentionPolicyRequest(),
            bucket="bucket_value",
        )


@pytest.mark.asyncio
async def test_lock_bucket_retention_policy_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.lock_bucket_retention_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Bucket())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.lock_bucket_retention_policy(
            bucket="bucket_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_lock_bucket_retention_policy_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.lock_bucket_retention_policy(
            storage.LockBucketRetentionPolicyRequest(),
            bucket="bucket_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        client.get_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()


@pytest.mark.asyncio
async def test_get_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.GetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async_from_dict():
    await test_get_iam_policy_async(request_type=dict)


def test_get_iam_policy_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest(**{"resource": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


def test_get_iam_policy_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy_pb2.GetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_iam_policy_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_iam_policy(
            iam_policy_pb2.GetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        client.set_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()


@pytest.mark.asyncio
async def test_set_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.SetIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async_from_dict():
    await test_set_iam_policy_async(request_type=dict)


def test_set_iam_policy_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest(**{"resource": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()
        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
                "update_mask": field_mask_pb2.FieldMask(paths=["paths_value"]),
            }
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


def test_set_iam_policy_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy_pb2.SetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_iam_policy(
            resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_iam_policy_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_iam_policy(
            iam_policy_pb2.SetIamPolicyRequest(),
            resource="resource_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )
        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        client.test_iam_permissions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()


@pytest.mark.asyncio
async def test_test_iam_permissions_async(
    transport: str = "grpc_asyncio",
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )
        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == iam_policy_pb2.TestIamPermissionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async_from_dict():
    await test_test_iam_permissions_async(request_type=dict)


def test_test_iam_permissions_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest(**{"resource": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest(
        **{"resource": "projects/sample1/buckets/sample2/objects/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.test_iam_permissions(
            resource="resource_value",
            permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val
        arg = args[0].permissions
        mock_val = ["permissions_value"]
        assert arg == mock_val


def test_test_iam_permissions_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy_pb2.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.test_iam_permissions(
            resource="resource_value",
            permissions=["permissions_value"],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].resource
        mock_val = "resource_value"
        assert arg == mock_val
        arg = args[0].permissions
        mock_val = ["permissions_value"]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_test_iam_permissions_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.test_iam_permissions(
            iam_policy_pb2.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.UpdateBucketRequest,
        dict,
    ],
)
def test_update_bucket(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket(
            name="name_value",
            bucket_id="bucket_id_value",
            etag="etag_value",
            project="project_value",
            metageneration=1491,
            location="location_value",
            location_type="location_type_value",
            storage_class="storage_class_value",
            rpo="rpo_value",
            default_event_based_hold=True,
            satisfies_pzs=True,
        )
        response = client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


def test_update_bucket_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        client.update_bucket()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateBucketRequest()


@pytest.mark.asyncio
async def test_update_bucket_async(
    transport: str = "grpc_asyncio", request_type=storage.UpdateBucketRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Bucket(
                name="name_value",
                bucket_id="bucket_id_value",
                etag="etag_value",
                project="project_value",
                metageneration=1491,
                location="location_value",
                location_type="location_type_value",
                storage_class="storage_class_value",
                rpo="rpo_value",
                default_event_based_hold=True,
                satisfies_pzs=True,
            )
        )
        response = await client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateBucketRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Bucket)
    assert response.name == "name_value"
    assert response.bucket_id == "bucket_id_value"
    assert response.etag == "etag_value"
    assert response.project == "project_value"
    assert response.metageneration == 1491
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"
    assert response.storage_class == "storage_class_value"
    assert response.rpo == "rpo_value"
    assert response.default_event_based_hold is True
    assert response.satisfies_pzs is True


@pytest.mark.asyncio
async def test_update_bucket_async_from_dict():
    await test_update_bucket_async(request_type=dict)


def test_update_bucket_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.UpdateBucketRequest(**{"bucket": {"name": "sample1"}})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        call.return_value = storage.Bucket()
        client.update_bucket(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_update_bucket_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_bucket(
            bucket=storage.Bucket(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = storage.Bucket(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_bucket_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_bucket(
            storage.UpdateBucketRequest(),
            bucket=storage.Bucket(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_bucket_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_bucket), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Bucket()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Bucket())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_bucket(
            bucket=storage.Bucket(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = storage.Bucket(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_bucket_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_bucket(
            storage.UpdateBucketRequest(),
            bucket=storage.Bucket(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.DeleteNotificationConfigRequest,
        dict,
    ],
)
def test_delete_notification_config(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        client.delete_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteNotificationConfigRequest()


@pytest.mark.asyncio
async def test_delete_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage.DeleteNotificationConfigRequest,
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_notification_config_async_from_dict():
    await test_delete_notification_config_async(request_type=dict)


def test_delete_notification_config_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.DeleteNotificationConfigRequest(
        **{"name": "projects/sample1/buckets/sample2/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        call.return_value = None
        client.delete_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_notification_config_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_notification_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_notification_config_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_notification_config(
            storage.DeleteNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_notification_config_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_notification_config(
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
async def test_delete_notification_config_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_notification_config(
            storage.DeleteNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.GetNotificationConfigRequest,
        dict,
    ],
)
def test_get_notification_config(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig(
            name="name_value",
            topic="topic_value",
            etag="etag_value",
            event_types=["event_types_value"],
            object_name_prefix="object_name_prefix_value",
            payload_format="payload_format_value",
        )
        response = client.get_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.NotificationConfig)
    assert response.name == "name_value"
    assert response.topic == "topic_value"
    assert response.etag == "etag_value"
    assert response.event_types == ["event_types_value"]
    assert response.object_name_prefix == "object_name_prefix_value"
    assert response.payload_format == "payload_format_value"


def test_get_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        client.get_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetNotificationConfigRequest()


@pytest.mark.asyncio
async def test_get_notification_config_async(
    transport: str = "grpc_asyncio", request_type=storage.GetNotificationConfigRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.NotificationConfig(
                name="name_value",
                topic="topic_value",
                etag="etag_value",
                event_types=["event_types_value"],
                object_name_prefix="object_name_prefix_value",
                payload_format="payload_format_value",
            )
        )
        response = await client.get_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.NotificationConfig)
    assert response.name == "name_value"
    assert response.topic == "topic_value"
    assert response.etag == "etag_value"
    assert response.event_types == ["event_types_value"]
    assert response.object_name_prefix == "object_name_prefix_value"
    assert response.payload_format == "payload_format_value"


@pytest.mark.asyncio
async def test_get_notification_config_async_from_dict():
    await test_get_notification_config_async(request_type=dict)


def test_get_notification_config_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetNotificationConfigRequest(
        **{"name": "projects/sample1/buckets/sample2/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        call.return_value = storage.NotificationConfig()
        client.get_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_notification_config_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_notification_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_notification_config_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_notification_config(
            storage.GetNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_notification_config_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.NotificationConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_notification_config(
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
async def test_get_notification_config_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_notification_config(
            storage.GetNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.CreateNotificationConfigRequest,
        dict,
    ],
)
def test_create_notification_config(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig(
            name="name_value",
            topic="topic_value",
            etag="etag_value",
            event_types=["event_types_value"],
            object_name_prefix="object_name_prefix_value",
            payload_format="payload_format_value",
        )
        response = client.create_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.NotificationConfig)
    assert response.name == "name_value"
    assert response.topic == "topic_value"
    assert response.etag == "etag_value"
    assert response.event_types == ["event_types_value"]
    assert response.object_name_prefix == "object_name_prefix_value"
    assert response.payload_format == "payload_format_value"


def test_create_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        client.create_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateNotificationConfigRequest()


@pytest.mark.asyncio
async def test_create_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage.CreateNotificationConfigRequest,
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.NotificationConfig(
                name="name_value",
                topic="topic_value",
                etag="etag_value",
                event_types=["event_types_value"],
                object_name_prefix="object_name_prefix_value",
                payload_format="payload_format_value",
            )
        )
        response = await client.create_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.NotificationConfig)
    assert response.name == "name_value"
    assert response.topic == "topic_value"
    assert response.etag == "etag_value"
    assert response.event_types == ["event_types_value"]
    assert response.object_name_prefix == "object_name_prefix_value"
    assert response.payload_format == "payload_format_value"


@pytest.mark.asyncio
async def test_create_notification_config_async_from_dict():
    await test_create_notification_config_async(request_type=dict)


def test_create_notification_config_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateNotificationConfigRequest(**{"parent": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        call.return_value = storage.NotificationConfig()
        client.create_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_notification_config_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_notification_config(
            parent="parent_value",
            notification_config=storage.NotificationConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].notification_config
        mock_val = storage.NotificationConfig(name="name_value")
        assert arg == mock_val


def test_create_notification_config_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_notification_config(
            storage.CreateNotificationConfigRequest(),
            parent="parent_value",
            notification_config=storage.NotificationConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_notification_config_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.NotificationConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.NotificationConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_notification_config(
            parent="parent_value",
            notification_config=storage.NotificationConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].notification_config
        mock_val = storage.NotificationConfig(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_notification_config_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_notification_config(
            storage.CreateNotificationConfigRequest(),
            parent="parent_value",
            notification_config=storage.NotificationConfig(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ListNotificationConfigsRequest,
        dict,
    ],
)
def test_list_notification_configs(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListNotificationConfigsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_notification_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListNotificationConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_notification_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        client.list_notification_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListNotificationConfigsRequest()


@pytest.mark.asyncio
async def test_list_notification_configs_async(
    transport: str = "grpc_asyncio", request_type=storage.ListNotificationConfigsRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListNotificationConfigsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_notification_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListNotificationConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_notification_configs_async_from_dict():
    await test_list_notification_configs_async(request_type=dict)


def test_list_notification_configs_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ListNotificationConfigsRequest(**{"parent": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        call.return_value = storage.ListNotificationConfigsResponse()
        client.list_notification_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_notification_configs_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListNotificationConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notification_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_notification_configs_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notification_configs(
            storage.ListNotificationConfigsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_notification_configs_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListNotificationConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListNotificationConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notification_configs(
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
async def test_list_notification_configs_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notification_configs(
            storage.ListNotificationConfigsRequest(),
            parent="parent_value",
        )


def test_list_notification_configs_pager(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_notification_configs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage.NotificationConfig) for i in results)


def test_list_notification_configs_pages(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_notification_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notification_configs_async_pager():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_notification_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage.NotificationConfig) for i in responses)


@pytest.mark.asyncio
async def test_list_notification_configs_async_pages():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            storage.ListNotificationConfigsResponse(
                notification_configs=[
                    storage.NotificationConfig(),
                    storage.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_notification_configs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ComposeObjectRequest,
        dict,
    ],
)
def test_compose_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.compose_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object(
            name="name_value",
            bucket="bucket_value",
            etag="etag_value",
            generation=1068,
            metageneration=1491,
            storage_class="storage_class_value",
            size=443,
            content_encoding="content_encoding_value",
            content_disposition="content_disposition_value",
            cache_control="cache_control_value",
            content_language="content_language_value",
            content_type="content_type_value",
            component_count=1627,
            kms_key="kms_key_value",
            temporary_hold=True,
            event_based_hold=True,
        )
        response = client.compose_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ComposeObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


def test_compose_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.compose_object), "__call__") as call:
        client.compose_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ComposeObjectRequest()


@pytest.mark.asyncio
async def test_compose_object_async(
    transport: str = "grpc_asyncio", request_type=storage.ComposeObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.compose_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Object(
                name="name_value",
                bucket="bucket_value",
                etag="etag_value",
                generation=1068,
                metageneration=1491,
                storage_class="storage_class_value",
                size=443,
                content_encoding="content_encoding_value",
                content_disposition="content_disposition_value",
                cache_control="cache_control_value",
                content_language="content_language_value",
                content_type="content_type_value",
                component_count=1627,
                kms_key="kms_key_value",
                temporary_hold=True,
                event_based_hold=True,
            )
        )
        response = await client.compose_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ComposeObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


@pytest.mark.asyncio
async def test_compose_object_async_from_dict():
    await test_compose_object_async(request_type=dict)


def test_compose_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ComposeObjectRequest(**{"destination": {"bucket": "sample1"}})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.compose_object), "__call__") as call:
        call.return_value = storage.Object()
        client.compose_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        storage.DeleteObjectRequest,
        dict,
    ],
)
def test_delete_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteObjectRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        client.delete_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteObjectRequest()


@pytest.mark.asyncio
async def test_delete_object_async(
    transport: str = "grpc_asyncio", request_type=storage.DeleteObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteObjectRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_object_async_from_dict():
    await test_delete_object_async(request_type=dict)


def test_delete_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.DeleteObjectRequest(**{"bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        call.return_value = None
        client.delete_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_object_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


def test_delete_object_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_object(
            storage.DeleteObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.asyncio
async def test_delete_object_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_object_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_object(
            storage.DeleteObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.RestoreObjectRequest,
        dict,
    ],
)
def test_restore_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object(
            name="name_value",
            bucket="bucket_value",
            etag="etag_value",
            generation=1068,
            metageneration=1491,
            storage_class="storage_class_value",
            size=443,
            content_encoding="content_encoding_value",
            content_disposition="content_disposition_value",
            cache_control="cache_control_value",
            content_language="content_language_value",
            content_type="content_type_value",
            component_count=1627,
            kms_key="kms_key_value",
            temporary_hold=True,
            event_based_hold=True,
        )
        response = client.restore_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RestoreObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


def test_restore_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        client.restore_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RestoreObjectRequest()


@pytest.mark.asyncio
async def test_restore_object_async(
    transport: str = "grpc_asyncio", request_type=storage.RestoreObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Object(
                name="name_value",
                bucket="bucket_value",
                etag="etag_value",
                generation=1068,
                metageneration=1491,
                storage_class="storage_class_value",
                size=443,
                content_encoding="content_encoding_value",
                content_disposition="content_disposition_value",
                cache_control="cache_control_value",
                content_language="content_language_value",
                content_type="content_type_value",
                component_count=1627,
                kms_key="kms_key_value",
                temporary_hold=True,
                event_based_hold=True,
            )
        )
        response = await client.restore_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RestoreObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


@pytest.mark.asyncio
async def test_restore_object_async_from_dict():
    await test_restore_object_async(request_type=dict)


def test_restore_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.RestoreObjectRequest(**{"bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        call.return_value = storage.Object()
        client.restore_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_restore_object_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restore_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


def test_restore_object_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_object(
            storage.RestoreObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.asyncio
async def test_restore_object_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Object())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restore_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


@pytest.mark.asyncio
async def test_restore_object_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restore_object(
            storage.RestoreObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.CancelResumableWriteRequest,
        dict,
    ],
)
def test_cancel_resumable_write(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CancelResumableWriteResponse()
        response = client.cancel_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CancelResumableWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.CancelResumableWriteResponse)


def test_cancel_resumable_write_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        client.cancel_resumable_write()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CancelResumableWriteRequest()


@pytest.mark.asyncio
async def test_cancel_resumable_write_async(
    transport: str = "grpc_asyncio", request_type=storage.CancelResumableWriteRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.CancelResumableWriteResponse()
        )
        response = await client.cancel_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CancelResumableWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.CancelResumableWriteResponse)


@pytest.mark.asyncio
async def test_cancel_resumable_write_async_from_dict():
    await test_cancel_resumable_write_async(request_type=dict)


def test_cancel_resumable_write_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CancelResumableWriteRequest(
        **{"upload_id": "projects/sample1/buckets/sample2/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        call.return_value = storage.CancelResumableWriteResponse()
        client.cancel_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_cancel_resumable_write_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CancelResumableWriteResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_resumable_write(
            upload_id="upload_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].upload_id
        mock_val = "upload_id_value"
        assert arg == mock_val


def test_cancel_resumable_write_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_resumable_write(
            storage.CancelResumableWriteRequest(),
            upload_id="upload_id_value",
        )


@pytest.mark.asyncio
async def test_cancel_resumable_write_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CancelResumableWriteResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.CancelResumableWriteResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_resumable_write(
            upload_id="upload_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].upload_id
        mock_val = "upload_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_resumable_write_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_resumable_write(
            storage.CancelResumableWriteRequest(),
            upload_id="upload_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.GetObjectRequest,
        dict,
    ],
)
def test_get_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object(
            name="name_value",
            bucket="bucket_value",
            etag="etag_value",
            generation=1068,
            metageneration=1491,
            storage_class="storage_class_value",
            size=443,
            content_encoding="content_encoding_value",
            content_disposition="content_disposition_value",
            cache_control="cache_control_value",
            content_language="content_language_value",
            content_type="content_type_value",
            component_count=1627,
            kms_key="kms_key_value",
            temporary_hold=True,
            event_based_hold=True,
        )
        response = client.get_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


def test_get_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        client.get_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetObjectRequest()


@pytest.mark.asyncio
async def test_get_object_async(
    transport: str = "grpc_asyncio", request_type=storage.GetObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Object(
                name="name_value",
                bucket="bucket_value",
                etag="etag_value",
                generation=1068,
                metageneration=1491,
                storage_class="storage_class_value",
                size=443,
                content_encoding="content_encoding_value",
                content_disposition="content_disposition_value",
                cache_control="cache_control_value",
                content_language="content_language_value",
                content_type="content_type_value",
                component_count=1627,
                kms_key="kms_key_value",
                temporary_hold=True,
                event_based_hold=True,
            )
        )
        response = await client.get_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


@pytest.mark.asyncio
async def test_get_object_async_from_dict():
    await test_get_object_async(request_type=dict)


def test_get_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetObjectRequest(**{"bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        call.return_value = storage.Object()
        client.get_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_object_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


def test_get_object_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_object(
            storage.GetObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.asyncio
async def test_get_object_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Object())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_object_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_object(
            storage.GetObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ReadObjectRequest,
        dict,
    ],
)
def test_read_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadObjectResponse()])
        response = client.read_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ReadObjectRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, storage.ReadObjectResponse)


def test_read_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        client.read_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ReadObjectRequest()


@pytest.mark.asyncio
async def test_read_object_async(
    transport: str = "grpc_asyncio", request_type=storage.ReadObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.ReadObjectResponse()]
        )
        response = await client.read_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ReadObjectRequest()

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, storage.ReadObjectResponse)


@pytest.mark.asyncio
async def test_read_object_async_from_dict():
    await test_read_object_async(request_type=dict)


def test_read_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ReadObjectRequest(**{"bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        call.return_value = iter([storage.ReadObjectResponse()])
        client.read_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_read_object_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadObjectResponse()])
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


def test_read_object_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_object(
            storage.ReadObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.asyncio
async def test_read_object_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.read_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadObjectResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_object(
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].bucket
        mock_val = "bucket_value"
        assert arg == mock_val
        arg = args[0].object_
        mock_val = "object__value"
        assert arg == mock_val
        arg = args[0].generation
        mock_val = 1068
        assert arg == mock_val


@pytest.mark.asyncio
async def test_read_object_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_object(
            storage.ReadObjectRequest(),
            bucket="bucket_value",
            object_="object__value",
            generation=1068,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.UpdateObjectRequest,
        dict,
    ],
)
def test_update_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object(
            name="name_value",
            bucket="bucket_value",
            etag="etag_value",
            generation=1068,
            metageneration=1491,
            storage_class="storage_class_value",
            size=443,
            content_encoding="content_encoding_value",
            content_disposition="content_disposition_value",
            cache_control="cache_control_value",
            content_language="content_language_value",
            content_type="content_type_value",
            component_count=1627,
            kms_key="kms_key_value",
            temporary_hold=True,
            event_based_hold=True,
        )
        response = client.update_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


def test_update_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        client.update_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateObjectRequest()


@pytest.mark.asyncio
async def test_update_object_async(
    transport: str = "grpc_asyncio", request_type=storage.UpdateObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.Object(
                name="name_value",
                bucket="bucket_value",
                etag="etag_value",
                generation=1068,
                metageneration=1491,
                storage_class="storage_class_value",
                size=443,
                content_encoding="content_encoding_value",
                content_disposition="content_disposition_value",
                cache_control="cache_control_value",
                content_language="content_language_value",
                content_type="content_type_value",
                component_count=1627,
                kms_key="kms_key_value",
                temporary_hold=True,
                event_based_hold=True,
            )
        )
        response = await client.update_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.Object)
    assert response.name == "name_value"
    assert response.bucket == "bucket_value"
    assert response.etag == "etag_value"
    assert response.generation == 1068
    assert response.metageneration == 1491
    assert response.storage_class == "storage_class_value"
    assert response.size == 443
    assert response.content_encoding == "content_encoding_value"
    assert response.content_disposition == "content_disposition_value"
    assert response.cache_control == "cache_control_value"
    assert response.content_language == "content_language_value"
    assert response.content_type == "content_type_value"
    assert response.component_count == 1627
    assert response.kms_key == "kms_key_value"
    assert response.temporary_hold is True
    assert response.event_based_hold is True


@pytest.mark.asyncio
async def test_update_object_async_from_dict():
    await test_update_object_async(request_type=dict)


def test_update_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.UpdateObjectRequest(**{"object": {"bucket": "sample1"}})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        call.return_value = storage.Object()
        client.update_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_update_object_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_object(
            object_=storage.Object(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].object_
        mock_val = storage.Object(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_object_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_object(
            storage.UpdateObjectRequest(),
            object_=storage.Object(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_object_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.Object()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.Object())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_object(
            object_=storage.Object(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].object_
        mock_val = storage.Object(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_object_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_object(
            storage.UpdateObjectRequest(),
            object_=storage.Object(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.WriteObjectRequest,
        dict,
    ],
)
def test_write_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.WriteObjectResponse(
            persisted_size=1517,
        )
        response = client.write_object(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.WriteObjectResponse)


@pytest.mark.asyncio
async def test_write_object_async(
    transport: str = "grpc_asyncio", request_type=storage.WriteObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.write_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeStreamUnaryCall(
            storage.WriteObjectResponse()
        )
        response = await (await client.write_object(iter(requests)))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.WriteObjectResponse)


@pytest.mark.asyncio
async def test_write_object_async_from_dict():
    await test_write_object_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        storage.BidiWriteObjectRequest,
        dict,
    ],
)
def test_bidi_write_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bidi_write_object), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.BidiWriteObjectResponse()])
        response = client.bidi_write_object(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, storage.BidiWriteObjectResponse)


@pytest.mark.asyncio
async def test_bidi_write_object_async(
    transport: str = "grpc_asyncio", request_type=storage.BidiWriteObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bidi_write_object), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.BidiWriteObjectResponse()]
        )
        response = await client.bidi_write_object(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, storage.BidiWriteObjectResponse)


@pytest.mark.asyncio
async def test_bidi_write_object_async_from_dict():
    await test_bidi_write_object_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ListObjectsRequest,
        dict,
    ],
)
def test_list_objects(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListObjectsResponse(
            prefixes=["prefixes_value"],
            next_page_token="next_page_token_value",
        )
        response = client.list_objects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListObjectsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListObjectsPager)
    assert response.prefixes == ["prefixes_value"]
    assert response.next_page_token == "next_page_token_value"


def test_list_objects_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        client.list_objects()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListObjectsRequest()


@pytest.mark.asyncio
async def test_list_objects_async(
    transport: str = "grpc_asyncio", request_type=storage.ListObjectsRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListObjectsResponse(
                prefixes=["prefixes_value"],
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_objects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListObjectsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListObjectsAsyncPager)
    assert response.prefixes == ["prefixes_value"]
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_objects_async_from_dict():
    await test_list_objects_async(request_type=dict)


def test_list_objects_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ListObjectsRequest(**{"parent": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        call.return_value = storage.ListObjectsResponse()
        client.list_objects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_objects_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListObjectsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_objects(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_objects_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_objects(
            storage.ListObjectsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_objects_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListObjectsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListObjectsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_objects(
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
async def test_list_objects_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_objects(
            storage.ListObjectsRequest(),
            parent="parent_value",
        )


def test_list_objects_pager(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                    storage.Object(),
                ],
                next_page_token="abc",
            ),
            storage.ListObjectsResponse(
                objects=[],
                next_page_token="def",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                ],
                next_page_token="ghi",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_objects(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage.Object) for i in results)


def test_list_objects_pages(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_objects), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                    storage.Object(),
                ],
                next_page_token="abc",
            ),
            storage.ListObjectsResponse(
                objects=[],
                next_page_token="def",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                ],
                next_page_token="ghi",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_objects(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_objects_async_pager():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_objects), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                    storage.Object(),
                ],
                next_page_token="abc",
            ),
            storage.ListObjectsResponse(
                objects=[],
                next_page_token="def",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                ],
                next_page_token="ghi",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_objects(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage.Object) for i in responses)


@pytest.mark.asyncio
async def test_list_objects_async_pages():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_objects), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                    storage.Object(),
                ],
                next_page_token="abc",
            ),
            storage.ListObjectsResponse(
                objects=[],
                next_page_token="def",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                ],
                next_page_token="ghi",
            ),
            storage.ListObjectsResponse(
                objects=[
                    storage.Object(),
                    storage.Object(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_objects(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage.RewriteObjectRequest,
        dict,
    ],
)
def test_rewrite_object(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rewrite_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.RewriteResponse(
            total_bytes_rewritten=2285,
            object_size=1169,
            done=True,
            rewrite_token="rewrite_token_value",
        )
        response = client.rewrite_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RewriteObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.RewriteResponse)
    assert response.total_bytes_rewritten == 2285
    assert response.object_size == 1169
    assert response.done is True
    assert response.rewrite_token == "rewrite_token_value"


def test_rewrite_object_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rewrite_object), "__call__") as call:
        client.rewrite_object()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RewriteObjectRequest()


@pytest.mark.asyncio
async def test_rewrite_object_async(
    transport: str = "grpc_asyncio", request_type=storage.RewriteObjectRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rewrite_object), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.RewriteResponse(
                total_bytes_rewritten=2285,
                object_size=1169,
                done=True,
                rewrite_token="rewrite_token_value",
            )
        )
        response = await client.rewrite_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.RewriteObjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.RewriteResponse)
    assert response.total_bytes_rewritten == 2285
    assert response.object_size == 1169
    assert response.done is True
    assert response.rewrite_token == "rewrite_token_value"


@pytest.mark.asyncio
async def test_rewrite_object_async_from_dict():
    await test_rewrite_object_async(request_type=dict)


def test_rewrite_object_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.RewriteObjectRequest(**{"source_bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rewrite_object), "__call__") as call:
        call.return_value = storage.RewriteResponse()
        client.rewrite_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]
    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.RewriteObjectRequest(**{"destination_bucket": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rewrite_object), "__call__") as call:
        call.return_value = storage.RewriteResponse()
        client.rewrite_object(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        storage.StartResumableWriteRequest,
        dict,
    ],
)
def test_start_resumable_write(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.StartResumableWriteResponse(
            upload_id="upload_id_value",
        )
        response = client.start_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.StartResumableWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.StartResumableWriteResponse)
    assert response.upload_id == "upload_id_value"


def test_start_resumable_write_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_resumable_write), "__call__"
    ) as call:
        client.start_resumable_write()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.StartResumableWriteRequest()


@pytest.mark.asyncio
async def test_start_resumable_write_async(
    transport: str = "grpc_asyncio", request_type=storage.StartResumableWriteRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_resumable_write), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.StartResumableWriteResponse(
                upload_id="upload_id_value",
            )
        )
        response = await client.start_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.StartResumableWriteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.StartResumableWriteResponse)
    assert response.upload_id == "upload_id_value"


@pytest.mark.asyncio
async def test_start_resumable_write_async_from_dict():
    await test_start_resumable_write_async(request_type=dict)


def test_start_resumable_write_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.StartResumableWriteRequest(
        **{"write_object_spec": {"resource": {"bucket": "sample1"}}}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_resumable_write), "__call__"
    ) as call:
        call.return_value = storage.StartResumableWriteResponse()
        client.start_resumable_write(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        storage.QueryWriteStatusRequest,
        dict,
    ],
)
def test_query_write_status(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.QueryWriteStatusResponse(
            persisted_size=1517,
        )
        response = client.query_write_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.QueryWriteStatusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.QueryWriteStatusResponse)


def test_query_write_status_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        client.query_write_status()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.QueryWriteStatusRequest()


@pytest.mark.asyncio
async def test_query_write_status_async(
    transport: str = "grpc_asyncio", request_type=storage.QueryWriteStatusRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.QueryWriteStatusResponse()
        )
        response = await client.query_write_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.QueryWriteStatusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.QueryWriteStatusResponse)


@pytest.mark.asyncio
async def test_query_write_status_async_from_dict():
    await test_query_write_status_async(request_type=dict)


def test_query_write_status_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.QueryWriteStatusRequest(
        **{"upload_id": "projects/sample1/buckets/sample2/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        call.return_value = storage.QueryWriteStatusResponse()
        client.query_write_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_query_write_status_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.QueryWriteStatusResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.query_write_status(
            upload_id="upload_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].upload_id
        mock_val = "upload_id_value"
        assert arg == mock_val


def test_query_write_status_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.query_write_status(
            storage.QueryWriteStatusRequest(),
            upload_id="upload_id_value",
        )


@pytest.mark.asyncio
async def test_query_write_status_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.query_write_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.QueryWriteStatusResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.QueryWriteStatusResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.query_write_status(
            upload_id="upload_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].upload_id
        mock_val = "upload_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_query_write_status_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.query_write_status(
            storage.QueryWriteStatusRequest(),
            upload_id="upload_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.GetServiceAccountRequest,
        dict,
    ],
)
def test_get_service_account(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ServiceAccount(
            email_address="email_address_value",
        )
        response = client.get_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetServiceAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.ServiceAccount)
    assert response.email_address == "email_address_value"


def test_get_service_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        client.get_service_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetServiceAccountRequest()


@pytest.mark.asyncio
async def test_get_service_account_async(
    transport: str = "grpc_asyncio", request_type=storage.GetServiceAccountRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ServiceAccount(
                email_address="email_address_value",
            )
        )
        response = await client.get_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetServiceAccountRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.ServiceAccount)
    assert response.email_address == "email_address_value"


@pytest.mark.asyncio
async def test_get_service_account_async_from_dict():
    await test_get_service_account_async(request_type=dict)


def test_get_service_account_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetServiceAccountRequest(**{"project": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        call.return_value = storage.ServiceAccount()
        client.get_service_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_service_account_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ServiceAccount()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service_account(
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


def test_get_service_account_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service_account(
            storage.GetServiceAccountRequest(),
            project="project_value",
        )


@pytest.mark.asyncio
async def test_get_service_account_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_service_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ServiceAccount()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ServiceAccount()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service_account(
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_service_account_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service_account(
            storage.GetServiceAccountRequest(),
            project="project_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.CreateHmacKeyRequest,
        dict,
    ],
)
def test_create_hmac_key(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CreateHmacKeyResponse(
            secret_key_bytes=b"secret_key_bytes_blob",
        )
        response = client.create_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.CreateHmacKeyResponse)
    assert response.secret_key_bytes == b"secret_key_bytes_blob"


def test_create_hmac_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        client.create_hmac_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateHmacKeyRequest()


@pytest.mark.asyncio
async def test_create_hmac_key_async(
    transport: str = "grpc_asyncio", request_type=storage.CreateHmacKeyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.CreateHmacKeyResponse(
                secret_key_bytes=b"secret_key_bytes_blob",
            )
        )
        response = await client.create_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.CreateHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.CreateHmacKeyResponse)
    assert response.secret_key_bytes == b"secret_key_bytes_blob"


@pytest.mark.asyncio
async def test_create_hmac_key_async_from_dict():
    await test_create_hmac_key_async(request_type=dict)


def test_create_hmac_key_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateHmacKeyRequest(**{"project": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        call.return_value = storage.CreateHmacKeyResponse()
        client.create_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_hmac_key_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CreateHmacKeyResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_hmac_key(
            project="project_value",
            service_account_email="service_account_email_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val
        arg = args[0].service_account_email
        mock_val = "service_account_email_value"
        assert arg == mock_val


def test_create_hmac_key_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_hmac_key(
            storage.CreateHmacKeyRequest(),
            project="project_value",
            service_account_email="service_account_email_value",
        )


@pytest.mark.asyncio
async def test_create_hmac_key_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.CreateHmacKeyResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.CreateHmacKeyResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_hmac_key(
            project="project_value",
            service_account_email="service_account_email_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val
        arg = args[0].service_account_email
        mock_val = "service_account_email_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_hmac_key_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_hmac_key(
            storage.CreateHmacKeyRequest(),
            project="project_value",
            service_account_email="service_account_email_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.DeleteHmacKeyRequest,
        dict,
    ],
)
def test_delete_hmac_key(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_hmac_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        client.delete_hmac_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteHmacKeyRequest()


@pytest.mark.asyncio
async def test_delete_hmac_key_async(
    transport: str = "grpc_asyncio", request_type=storage.DeleteHmacKeyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.DeleteHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_hmac_key_async_from_dict():
    await test_delete_hmac_key_async(request_type=dict)


def test_delete_hmac_key_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.DeleteHmacKeyRequest(**{"project": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        call.return_value = None
        client.delete_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_hmac_key_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_hmac_key(
            access_id="access_id_value",
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].access_id
        mock_val = "access_id_value"
        assert arg == mock_val
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


def test_delete_hmac_key_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_hmac_key(
            storage.DeleteHmacKeyRequest(),
            access_id="access_id_value",
            project="project_value",
        )


@pytest.mark.asyncio
async def test_delete_hmac_key_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_hmac_key(
            access_id="access_id_value",
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].access_id
        mock_val = "access_id_value"
        assert arg == mock_val
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_hmac_key_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_hmac_key(
            storage.DeleteHmacKeyRequest(),
            access_id="access_id_value",
            project="project_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.GetHmacKeyRequest,
        dict,
    ],
)
def test_get_hmac_key(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata(
            id="id_value",
            access_id="access_id_value",
            project="project_value",
            service_account_email="service_account_email_value",
            state="state_value",
            etag="etag_value",
        )
        response = client.get_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.HmacKeyMetadata)
    assert response.id == "id_value"
    assert response.access_id == "access_id_value"
    assert response.project == "project_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.state == "state_value"
    assert response.etag == "etag_value"


def test_get_hmac_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        client.get_hmac_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetHmacKeyRequest()


@pytest.mark.asyncio
async def test_get_hmac_key_async(
    transport: str = "grpc_asyncio", request_type=storage.GetHmacKeyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.HmacKeyMetadata(
                id="id_value",
                access_id="access_id_value",
                project="project_value",
                service_account_email="service_account_email_value",
                state="state_value",
                etag="etag_value",
            )
        )
        response = await client.get_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.GetHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.HmacKeyMetadata)
    assert response.id == "id_value"
    assert response.access_id == "access_id_value"
    assert response.project == "project_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.state == "state_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_hmac_key_async_from_dict():
    await test_get_hmac_key_async(request_type=dict)


def test_get_hmac_key_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.GetHmacKeyRequest(**{"project": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        call.return_value = storage.HmacKeyMetadata()
        client.get_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_hmac_key_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_hmac_key(
            access_id="access_id_value",
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].access_id
        mock_val = "access_id_value"
        assert arg == mock_val
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


def test_get_hmac_key_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_hmac_key(
            storage.GetHmacKeyRequest(),
            access_id="access_id_value",
            project="project_value",
        )


@pytest.mark.asyncio
async def test_get_hmac_key_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.HmacKeyMetadata()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_hmac_key(
            access_id="access_id_value",
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].access_id
        mock_val = "access_id_value"
        assert arg == mock_val
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_hmac_key_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_hmac_key(
            storage.GetHmacKeyRequest(),
            access_id="access_id_value",
            project="project_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage.ListHmacKeysRequest,
        dict,
    ],
)
def test_list_hmac_keys(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListHmacKeysResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_hmac_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListHmacKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHmacKeysPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_hmac_keys_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        client.list_hmac_keys()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListHmacKeysRequest()


@pytest.mark.asyncio
async def test_list_hmac_keys_async(
    transport: str = "grpc_asyncio", request_type=storage.ListHmacKeysRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListHmacKeysResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_hmac_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.ListHmacKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHmacKeysAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_hmac_keys_async_from_dict():
    await test_list_hmac_keys_async(request_type=dict)


def test_list_hmac_keys_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ListHmacKeysRequest(**{"project": "sample1"})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        call.return_value = storage.ListHmacKeysResponse()
        client.list_hmac_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_hmac_keys_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListHmacKeysResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_hmac_keys(
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


def test_list_hmac_keys_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_hmac_keys(
            storage.ListHmacKeysRequest(),
            project="project_value",
        )


@pytest.mark.asyncio
async def test_list_hmac_keys_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ListHmacKeysResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ListHmacKeysResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_hmac_keys(
            project="project_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project
        mock_val = "project_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_hmac_keys_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_hmac_keys(
            storage.ListHmacKeysRequest(),
            project="project_value",
        )


def test_list_hmac_keys_pager(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="abc",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[],
                next_page_token="def",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="ghi",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_hmac_keys(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage.HmacKeyMetadata) for i in results)


def test_list_hmac_keys_pages(transport_name: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_hmac_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="abc",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[],
                next_page_token="def",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="ghi",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_hmac_keys(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_hmac_keys_async_pager():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hmac_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="abc",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[],
                next_page_token="def",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="ghi",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_hmac_keys(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage.HmacKeyMetadata) for i in responses)


@pytest.mark.asyncio
async def test_list_hmac_keys_async_pages():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hmac_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="abc",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[],
                next_page_token="def",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                ],
                next_page_token="ghi",
            ),
            storage.ListHmacKeysResponse(
                hmac_keys=[
                    storage.HmacKeyMetadata(),
                    storage.HmacKeyMetadata(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_hmac_keys(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage.UpdateHmacKeyRequest,
        dict,
    ],
)
def test_update_hmac_key(request_type, transport: str = "grpc"):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata(
            id="id_value",
            access_id="access_id_value",
            project="project_value",
            service_account_email="service_account_email_value",
            state="state_value",
            etag="etag_value",
        )
        response = client.update_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.HmacKeyMetadata)
    assert response.id == "id_value"
    assert response.access_id == "access_id_value"
    assert response.project == "project_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.state == "state_value"
    assert response.etag == "etag_value"


def test_update_hmac_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        client.update_hmac_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateHmacKeyRequest()


@pytest.mark.asyncio
async def test_update_hmac_key_async(
    transport: str = "grpc_asyncio", request_type=storage.UpdateHmacKeyRequest
):
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.HmacKeyMetadata(
                id="id_value",
                access_id="access_id_value",
                project="project_value",
                service_account_email="service_account_email_value",
                state="state_value",
                etag="etag_value",
            )
        )
        response = await client.update_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage.UpdateHmacKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.HmacKeyMetadata)
    assert response.id == "id_value"
    assert response.access_id == "access_id_value"
    assert response.project == "project_value"
    assert response.service_account_email == "service_account_email_value"
    assert response.state == "state_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_hmac_key_async_from_dict():
    await test_update_hmac_key_async(request_type=dict)


def test_update_hmac_key_routing_parameters():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.UpdateHmacKeyRequest(**{"hmac_key": {"project": "sample1"}})

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        call.return_value = storage.HmacKeyMetadata()
        client.update_hmac_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_update_hmac_key_flattened():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_hmac_key(
            hmac_key=storage.HmacKeyMetadata(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].hmac_key
        mock_val = storage.HmacKeyMetadata(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_hmac_key_flattened_error():
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_hmac_key(
            storage.UpdateHmacKeyRequest(),
            hmac_key=storage.HmacKeyMetadata(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_hmac_key_flattened_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_hmac_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.HmacKeyMetadata()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.HmacKeyMetadata()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_hmac_key(
            hmac_key=storage.HmacKeyMetadata(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].hmac_key
        mock_val = storage.HmacKeyMetadata(id="id_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_hmac_key_flattened_error_async():
    client = StorageAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_hmac_key(
            storage.UpdateHmacKeyRequest(),
            hmac_key=storage.HmacKeyMetadata(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = StorageClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.StorageGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageGrpcTransport,
        transports.StorageGrpcAsyncIOTransport,
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
    transport = StorageClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.StorageGrpcTransport,
    )


def test_storage_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.StorageTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_storage_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.storage_client_v2.services.storage.transports.StorageTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.StorageTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "delete_bucket",
        "get_bucket",
        "create_bucket",
        "list_buckets",
        "lock_bucket_retention_policy",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
        "update_bucket",
        "delete_notification_config",
        "get_notification_config",
        "create_notification_config",
        "list_notification_configs",
        "compose_object",
        "delete_object",
        "restore_object",
        "cancel_resumable_write",
        "get_object",
        "read_object",
        "update_object",
        "write_object",
        "bidi_write_object",
        "list_objects",
        "rewrite_object",
        "start_resumable_write",
        "query_write_status",
        "get_service_account",
        "create_hmac_key",
        "delete_hmac_key",
        "get_hmac_key",
        "list_hmac_keys",
        "update_hmac_key",
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


def test_storage_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.storage_client_v2.services.storage.transports.StorageTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            quota_project_id="octopus",
        )


def test_storage_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.storage_client_v2.services.storage.transports.StorageTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageTransport()
        adc.assert_called_once()


def test_storage_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        StorageClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageGrpcTransport,
        transports.StorageGrpcAsyncIOTransport,
    ],
)
def test_storage_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageGrpcTransport,
        transports.StorageGrpcAsyncIOTransport,
    ],
)
def test_storage_transport_auth_gdch_credentials(transport_class):
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
        (transports.StorageGrpcTransport, grpc_helpers),
        (transports.StorageGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_storage_transport_create_channel(transport_class, grpc_helpers):
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
            "storage.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/devstorage.full_control",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write",
            ),
            scopes=["1", "2"],
            default_host="storage.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.StorageGrpcTransport, transports.StorageGrpcAsyncIOTransport],
)
def test_storage_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_storage_host_no_port(transport_name):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="storage.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("storage.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_storage_host_with_port(transport_name):
    client = StorageClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="storage.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("storage.googleapis.com:8000")


def test_storage_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_storage_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageGrpcAsyncIOTransport(
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
    [transports.StorageGrpcTransport, transports.StorageGrpcAsyncIOTransport],
)
def test_storage_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.StorageGrpcTransport, transports.StorageGrpcAsyncIOTransport],
)
def test_storage_transport_channel_mtls_with_adc(transport_class):
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


def test_bucket_path():
    project = "squid"
    bucket = "clam"
    expected = "projects/{project}/buckets/{bucket}".format(
        project=project,
        bucket=bucket,
    )
    actual = StorageClient.bucket_path(project, bucket)
    assert expected == actual


def test_parse_bucket_path():
    expected = {
        "project": "whelk",
        "bucket": "octopus",
    }
    path = StorageClient.bucket_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_bucket_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "oyster"
    location = "nudibranch"
    key_ring = "cuttlefish"
    crypto_key = "mussel"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
    )
    actual = StorageClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "key_ring": "scallop",
        "crypto_key": "abalone",
    }
    path = StorageClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_crypto_key_path(path)
    assert expected == actual


def test_notification_config_path():
    project = "squid"
    bucket = "clam"
    notification_config = "whelk"
    expected = "projects/{project}/buckets/{bucket}/notificationConfigs/{notification_config}".format(
        project=project,
        bucket=bucket,
        notification_config=notification_config,
    )
    actual = StorageClient.notification_config_path(
        project, bucket, notification_config
    )
    assert expected == actual


def test_parse_notification_config_path():
    expected = {
        "project": "octopus",
        "bucket": "oyster",
        "notification_config": "nudibranch",
    }
    path = StorageClient.notification_config_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_notification_config_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = StorageClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = StorageClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = StorageClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = StorageClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = StorageClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = StorageClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = StorageClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = StorageClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = StorageClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = StorageClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.StorageTransport, "_prep_wrapped_messages"
    ) as prep:
        client = StorageClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.StorageTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = StorageClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = StorageAsyncClient(
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
        client = StorageClient(
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
        client = StorageClient(
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
        (StorageClient, transports.StorageGrpcTransport),
        (StorageAsyncClient, transports.StorageGrpcAsyncIOTransport),
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
