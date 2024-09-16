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

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import empty_pb2  # type: ignore
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

from google.cloud.gke_multicloud_v1.services.attached_clusters import (
    AttachedClustersAsyncClient,
    AttachedClustersClient,
    pagers,
    transports,
)
from google.cloud.gke_multicloud_v1.types import (
    attached_resources,
    attached_service,
    common_resources,
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

    assert AttachedClustersClient._get_default_mtls_endpoint(None) is None
    assert (
        AttachedClustersClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AttachedClustersClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AttachedClustersClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AttachedClustersClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AttachedClustersClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert AttachedClustersClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert AttachedClustersClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert AttachedClustersClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            AttachedClustersClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert AttachedClustersClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert AttachedClustersClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert AttachedClustersClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            AttachedClustersClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert AttachedClustersClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert AttachedClustersClient._get_client_cert_source(None, False) is None
    assert (
        AttachedClustersClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        AttachedClustersClient._get_client_cert_source(mock_provided_cert_source, True)
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
                AttachedClustersClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                AttachedClustersClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    AttachedClustersClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersClient),
)
@mock.patch.object(
    AttachedClustersAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = AttachedClustersClient._DEFAULT_UNIVERSE
    default_endpoint = AttachedClustersClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = AttachedClustersClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        AttachedClustersClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        AttachedClustersClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == AttachedClustersClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        AttachedClustersClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        AttachedClustersClient._get_api_endpoint(None, None, default_universe, "always")
        == AttachedClustersClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        AttachedClustersClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == AttachedClustersClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        AttachedClustersClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        AttachedClustersClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        AttachedClustersClient._get_api_endpoint(
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
        AttachedClustersClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        AttachedClustersClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        AttachedClustersClient._get_universe_domain(None, None)
        == AttachedClustersClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        AttachedClustersClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AttachedClustersClient, transports.AttachedClustersGrpcTransport, "grpc"),
        (AttachedClustersClient, transports.AttachedClustersRestTransport, "rest"),
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
        (AttachedClustersClient, "grpc"),
        (AttachedClustersAsyncClient, "grpc_asyncio"),
        (AttachedClustersClient, "rest"),
    ],
)
def test_attached_clusters_client_from_service_account_info(
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
            "gkemulticloud.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://gkemulticloud.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AttachedClustersGrpcTransport, "grpc"),
        (transports.AttachedClustersGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.AttachedClustersRestTransport, "rest"),
    ],
)
def test_attached_clusters_client_service_account_always_use_jwt(
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
        (AttachedClustersClient, "grpc"),
        (AttachedClustersAsyncClient, "grpc_asyncio"),
        (AttachedClustersClient, "rest"),
    ],
)
def test_attached_clusters_client_from_service_account_file(
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
            "gkemulticloud.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://gkemulticloud.googleapis.com"
        )


def test_attached_clusters_client_get_transport_class():
    transport = AttachedClustersClient.get_transport_class()
    available_transports = [
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersRestTransport,
    ]
    assert transport in available_transports

    transport = AttachedClustersClient.get_transport_class("grpc")
    assert transport == transports.AttachedClustersGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AttachedClustersClient, transports.AttachedClustersGrpcTransport, "grpc"),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (AttachedClustersClient, transports.AttachedClustersRestTransport, "rest"),
    ],
)
@mock.patch.object(
    AttachedClustersClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersClient),
)
@mock.patch.object(
    AttachedClustersAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersAsyncClient),
)
def test_attached_clusters_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AttachedClustersClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AttachedClustersClient, "get_transport_class") as gtc:
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
            AttachedClustersClient,
            transports.AttachedClustersGrpcTransport,
            "grpc",
            "true",
        ),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            AttachedClustersClient,
            transports.AttachedClustersGrpcTransport,
            "grpc",
            "false",
        ),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            AttachedClustersClient,
            transports.AttachedClustersRestTransport,
            "rest",
            "true",
        ),
        (
            AttachedClustersClient,
            transports.AttachedClustersRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    AttachedClustersClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersClient),
)
@mock.patch.object(
    AttachedClustersAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_attached_clusters_client_mtls_env_auto(
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
    "client_class", [AttachedClustersClient, AttachedClustersAsyncClient]
)
@mock.patch.object(
    AttachedClustersClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AttachedClustersClient),
)
@mock.patch.object(
    AttachedClustersAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AttachedClustersAsyncClient),
)
def test_attached_clusters_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [AttachedClustersClient, AttachedClustersAsyncClient]
)
@mock.patch.object(
    AttachedClustersClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersClient),
)
@mock.patch.object(
    AttachedClustersAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(AttachedClustersAsyncClient),
)
def test_attached_clusters_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = AttachedClustersClient._DEFAULT_UNIVERSE
    default_endpoint = AttachedClustersClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = AttachedClustersClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (AttachedClustersClient, transports.AttachedClustersGrpcTransport, "grpc"),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (AttachedClustersClient, transports.AttachedClustersRestTransport, "rest"),
    ],
)
def test_attached_clusters_client_client_options_scopes(
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
            AttachedClustersClient,
            transports.AttachedClustersGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            AttachedClustersClient,
            transports.AttachedClustersRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_attached_clusters_client_client_options_credentials_file(
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


def test_attached_clusters_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.gke_multicloud_v1.services.attached_clusters.transports.AttachedClustersGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AttachedClustersClient(
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
            AttachedClustersClient,
            transports.AttachedClustersGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            AttachedClustersAsyncClient,
            transports.AttachedClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_attached_clusters_client_create_channel_credentials_file(
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
            "gkemulticloud.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="gkemulticloud.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.CreateAttachedClusterRequest,
        dict,
    ],
)
def test_create_attached_cluster(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.CreateAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_attached_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.CreateAttachedClusterRequest()


def test_create_attached_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.CreateAttachedClusterRequest(
        parent="parent_value",
        attached_cluster_id="attached_cluster_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_attached_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.CreateAttachedClusterRequest(
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )


def test_create_attached_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_attached_cluster
        ] = mock_rpc
        request = {}
        client.create_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_attached_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.CreateAttachedClusterRequest()


@pytest.mark.asyncio
async def test_create_attached_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_attached_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_attached_cluster
        ] = mock_rpc

        request = {}
        await client.create_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_attached_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.CreateAttachedClusterRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.CreateAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_attached_cluster_async_from_dict():
    await test_create_attached_cluster_async(request_type=dict)


def test_create_attached_cluster_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.CreateAttachedClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_attached_cluster(request)

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
async def test_create_attached_cluster_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.CreateAttachedClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_attached_cluster(request)

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


def test_create_attached_cluster_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_attached_cluster(
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].attached_cluster
        mock_val = attached_resources.AttachedCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].attached_cluster_id
        mock_val = "attached_cluster_id_value"
        assert arg == mock_val


def test_create_attached_cluster_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_attached_cluster(
            attached_service.CreateAttachedClusterRequest(),
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )


@pytest.mark.asyncio
async def test_create_attached_cluster_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_attached_cluster(
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].attached_cluster
        mock_val = attached_resources.AttachedCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].attached_cluster_id
        mock_val = "attached_cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_attached_cluster_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_attached_cluster(
            attached_service.CreateAttachedClusterRequest(),
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.UpdateAttachedClusterRequest,
        dict,
    ],
)
def test_update_attached_cluster(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.UpdateAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_attached_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.UpdateAttachedClusterRequest()


def test_update_attached_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.UpdateAttachedClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_attached_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.UpdateAttachedClusterRequest()


def test_update_attached_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_attached_cluster
        ] = mock_rpc
        request = {}
        client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_attached_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.UpdateAttachedClusterRequest()


@pytest.mark.asyncio
async def test_update_attached_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_attached_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_attached_cluster
        ] = mock_rpc

        request = {}
        await client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_attached_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.UpdateAttachedClusterRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.UpdateAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_attached_cluster_async_from_dict():
    await test_update_attached_cluster_async(request_type=dict)


def test_update_attached_cluster_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.UpdateAttachedClusterRequest()

    request.attached_cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attached_cluster.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_attached_cluster_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.UpdateAttachedClusterRequest()

    request.attached_cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attached_cluster.name=name_value",
    ) in kw["metadata"]


def test_update_attached_cluster_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_attached_cluster(
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].attached_cluster
        mock_val = attached_resources.AttachedCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_attached_cluster_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_attached_cluster(
            attached_service.UpdateAttachedClusterRequest(),
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_attached_cluster_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_attached_cluster(
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].attached_cluster
        mock_val = attached_resources.AttachedCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_attached_cluster_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_attached_cluster(
            attached_service.UpdateAttachedClusterRequest(),
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.ImportAttachedClusterRequest,
        dict,
    ],
)
def test_import_attached_cluster(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.ImportAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_attached_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.import_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ImportAttachedClusterRequest()


def test_import_attached_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.ImportAttachedClusterRequest(
        parent="parent_value",
        fleet_membership="fleet_membership_value",
        platform_version="platform_version_value",
        distribution="distribution_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.import_attached_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ImportAttachedClusterRequest(
            parent="parent_value",
            fleet_membership="fleet_membership_value",
            platform_version="platform_version_value",
            distribution="distribution_value",
        )


def test_import_attached_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.import_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.import_attached_cluster
        ] = mock_rpc
        request = {}
        client.import_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.import_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_import_attached_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ImportAttachedClusterRequest()


@pytest.mark.asyncio
async def test_import_attached_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.import_attached_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.import_attached_cluster
        ] = mock_rpc

        request = {}
        await client.import_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.import_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_import_attached_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.ImportAttachedClusterRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.ImportAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_attached_cluster_async_from_dict():
    await test_import_attached_cluster_async(request_type=dict)


def test_import_attached_cluster_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.ImportAttachedClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_attached_cluster(request)

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
async def test_import_attached_cluster_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.ImportAttachedClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_attached_cluster(request)

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


def test_import_attached_cluster_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_attached_cluster(
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].fleet_membership
        mock_val = "fleet_membership_value"
        assert arg == mock_val


def test_import_attached_cluster_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_attached_cluster(
            attached_service.ImportAttachedClusterRequest(),
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )


@pytest.mark.asyncio
async def test_import_attached_cluster_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_attached_cluster(
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].fleet_membership
        mock_val = "fleet_membership_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_import_attached_cluster_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_attached_cluster(
            attached_service.ImportAttachedClusterRequest(),
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GetAttachedClusterRequest,
        dict,
    ],
)
def test_get_attached_cluster(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedCluster(
            name="name_value",
            description="description_value",
            platform_version="platform_version_value",
            distribution="distribution_value",
            cluster_region="cluster_region_value",
            state=attached_resources.AttachedCluster.State.PROVISIONING,
            uid="uid_value",
            reconciling=True,
            etag="etag_value",
            kubernetes_version="kubernetes_version_value",
        )
        response = client.get_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.GetAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedCluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.platform_version == "platform_version_value"
    assert response.distribution == "distribution_value"
    assert response.cluster_region == "cluster_region_value"
    assert response.state == attached_resources.AttachedCluster.State.PROVISIONING
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"
    assert response.kubernetes_version == "kubernetes_version_value"


def test_get_attached_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedClusterRequest()


def test_get_attached_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.GetAttachedClusterRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_attached_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedClusterRequest(
            name="name_value",
        )


def test_get_attached_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_attached_cluster in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_attached_cluster
        ] = mock_rpc
        request = {}
        client.get_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_attached_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedCluster(
                name="name_value",
                description="description_value",
                platform_version="platform_version_value",
                distribution="distribution_value",
                cluster_region="cluster_region_value",
                state=attached_resources.AttachedCluster.State.PROVISIONING,
                uid="uid_value",
                reconciling=True,
                etag="etag_value",
                kubernetes_version="kubernetes_version_value",
            )
        )
        response = await client.get_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedClusterRequest()


@pytest.mark.asyncio
async def test_get_attached_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_attached_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_attached_cluster
        ] = mock_rpc

        request = {}
        await client.get_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_attached_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.GetAttachedClusterRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedCluster(
                name="name_value",
                description="description_value",
                platform_version="platform_version_value",
                distribution="distribution_value",
                cluster_region="cluster_region_value",
                state=attached_resources.AttachedCluster.State.PROVISIONING,
                uid="uid_value",
                reconciling=True,
                etag="etag_value",
                kubernetes_version="kubernetes_version_value",
            )
        )
        response = await client.get_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.GetAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedCluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.platform_version == "platform_version_value"
    assert response.distribution == "distribution_value"
    assert response.cluster_region == "cluster_region_value"
    assert response.state == attached_resources.AttachedCluster.State.PROVISIONING
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"
    assert response.kubernetes_version == "kubernetes_version_value"


@pytest.mark.asyncio
async def test_get_attached_cluster_async_from_dict():
    await test_get_attached_cluster_async(request_type=dict)


def test_get_attached_cluster_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GetAttachedClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        call.return_value = attached_resources.AttachedCluster()
        client.get_attached_cluster(request)

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
async def test_get_attached_cluster_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GetAttachedClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedCluster()
        )
        await client.get_attached_cluster(request)

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


def test_get_attached_cluster_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedCluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_attached_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_attached_cluster_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attached_cluster(
            attached_service.GetAttachedClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_attached_cluster_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedCluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedCluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_attached_cluster(
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
async def test_get_attached_cluster_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_attached_cluster(
            attached_service.GetAttachedClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.ListAttachedClustersRequest,
        dict,
    ],
)
def test_list_attached_clusters(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_service.ListAttachedClustersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_attached_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.ListAttachedClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAttachedClustersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_attached_clusters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_attached_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ListAttachedClustersRequest()


def test_list_attached_clusters_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.ListAttachedClustersRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_attached_clusters(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ListAttachedClustersRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_attached_clusters_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_attached_clusters
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_attached_clusters
        ] = mock_rpc
        request = {}
        client.list_attached_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_attached_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_attached_clusters_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.ListAttachedClustersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_attached_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.ListAttachedClustersRequest()


@pytest.mark.asyncio
async def test_list_attached_clusters_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_attached_clusters
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_attached_clusters
        ] = mock_rpc

        request = {}
        await client.list_attached_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_attached_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_attached_clusters_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.ListAttachedClustersRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.ListAttachedClustersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_attached_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.ListAttachedClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAttachedClustersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_attached_clusters_async_from_dict():
    await test_list_attached_clusters_async(request_type=dict)


def test_list_attached_clusters_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.ListAttachedClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        call.return_value = attached_service.ListAttachedClustersResponse()
        client.list_attached_clusters(request)

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
async def test_list_attached_clusters_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.ListAttachedClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.ListAttachedClustersResponse()
        )
        await client.list_attached_clusters(request)

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


def test_list_attached_clusters_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_service.ListAttachedClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_attached_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_attached_clusters_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_attached_clusters(
            attached_service.ListAttachedClustersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_attached_clusters_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_service.ListAttachedClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.ListAttachedClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_attached_clusters(
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
async def test_list_attached_clusters_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_attached_clusters(
            attached_service.ListAttachedClustersRequest(),
            parent="parent_value",
        )


def test_list_attached_clusters_pager(transport_name: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="abc",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[],
                next_page_token="def",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="ghi",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
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
        pager = client.list_attached_clusters(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, attached_resources.AttachedCluster) for i in results)


def test_list_attached_clusters_pages(transport_name: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="abc",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[],
                next_page_token="def",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="ghi",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_attached_clusters(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_attached_clusters_async_pager():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="abc",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[],
                next_page_token="def",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="ghi",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_attached_clusters(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, attached_resources.AttachedCluster) for i in responses)


@pytest.mark.asyncio
async def test_list_attached_clusters_async_pages():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_attached_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="abc",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[],
                next_page_token="def",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="ghi",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_attached_clusters(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.DeleteAttachedClusterRequest,
        dict,
    ],
)
def test_delete_attached_cluster(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.DeleteAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_attached_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.DeleteAttachedClusterRequest()


def test_delete_attached_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.DeleteAttachedClusterRequest(
        name="name_value",
        etag="etag_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_attached_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.DeleteAttachedClusterRequest(
            name="name_value",
            etag="etag_value",
        )


def test_delete_attached_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_attached_cluster
        ] = mock_rpc
        request = {}
        client.delete_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_attached_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_attached_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.DeleteAttachedClusterRequest()


@pytest.mark.asyncio
async def test_delete_attached_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_attached_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_attached_cluster
        ] = mock_rpc

        request = {}
        await client.delete_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_attached_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.DeleteAttachedClusterRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.DeleteAttachedClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_attached_cluster_async_from_dict():
    await test_delete_attached_cluster_async(request_type=dict)


def test_delete_attached_cluster_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.DeleteAttachedClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_attached_cluster(request)

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
async def test_delete_attached_cluster_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.DeleteAttachedClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_attached_cluster(request)

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


def test_delete_attached_cluster_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_attached_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_attached_cluster_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_attached_cluster(
            attached_service.DeleteAttachedClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_attached_cluster_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_attached_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_attached_cluster(
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
async def test_delete_attached_cluster_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_attached_cluster(
            attached_service.DeleteAttachedClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GetAttachedServerConfigRequest,
        dict,
    ],
)
def test_get_attached_server_config(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedServerConfig(
            name="name_value",
        )
        response = client.get_attached_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.GetAttachedServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedServerConfig)
    assert response.name == "name_value"


def test_get_attached_server_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_attached_server_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedServerConfigRequest()


def test_get_attached_server_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.GetAttachedServerConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_attached_server_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedServerConfigRequest(
            name="name_value",
        )


def test_get_attached_server_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_attached_server_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_attached_server_config
        ] = mock_rpc
        request = {}
        client.get_attached_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_attached_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_attached_server_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedServerConfig(
                name="name_value",
            )
        )
        response = await client.get_attached_server_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GetAttachedServerConfigRequest()


@pytest.mark.asyncio
async def test_get_attached_server_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_attached_server_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_attached_server_config
        ] = mock_rpc

        request = {}
        await client.get_attached_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_attached_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_attached_server_config_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.GetAttachedServerConfigRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedServerConfig(
                name="name_value",
            )
        )
        response = await client.get_attached_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.GetAttachedServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedServerConfig)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_attached_server_config_async_from_dict():
    await test_get_attached_server_config_async(request_type=dict)


def test_get_attached_server_config_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GetAttachedServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        call.return_value = attached_resources.AttachedServerConfig()
        client.get_attached_server_config(request)

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
async def test_get_attached_server_config_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GetAttachedServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedServerConfig()
        )
        await client.get_attached_server_config(request)

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


def test_get_attached_server_config_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedServerConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_attached_server_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_attached_server_config_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attached_server_config(
            attached_service.GetAttachedServerConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_attached_server_config_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_attached_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_resources.AttachedServerConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_resources.AttachedServerConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_attached_server_config(
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
async def test_get_attached_server_config_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_attached_server_config(
            attached_service.GetAttachedServerConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GenerateAttachedClusterInstallManifestRequest,
        dict,
    ],
)
def test_generate_attached_cluster_install_manifest(
    request_type, transport: str = "grpc"
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse(
                manifest="manifest_value",
            )
        )
        response = client.generate_attached_cluster_install_manifest(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.GenerateAttachedClusterInstallManifestRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterInstallManifestResponse
    )
    assert response.manifest == "manifest_value"


def test_generate_attached_cluster_install_manifest_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_attached_cluster_install_manifest()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == attached_service.GenerateAttachedClusterInstallManifestRequest()
        )


def test_generate_attached_cluster_install_manifest_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.GenerateAttachedClusterInstallManifestRequest(
        parent="parent_value",
        attached_cluster_id="attached_cluster_id_value",
        platform_version="platform_version_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_attached_cluster_install_manifest(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ] == attached_service.GenerateAttachedClusterInstallManifestRequest(
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
            platform_version="platform_version_value",
        )


def test_generate_attached_cluster_install_manifest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_attached_cluster_install_manifest
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_attached_cluster_install_manifest
        ] = mock_rpc
        request = {}
        client.generate_attached_cluster_install_manifest(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_attached_cluster_install_manifest(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterInstallManifestResponse(
                manifest="manifest_value",
            )
        )
        response = await client.generate_attached_cluster_install_manifest()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == attached_service.GenerateAttachedClusterInstallManifestRequest()
        )


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_attached_cluster_install_manifest
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_attached_cluster_install_manifest
        ] = mock_rpc

        request = {}
        await client.generate_attached_cluster_install_manifest(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.generate_attached_cluster_install_manifest(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.GenerateAttachedClusterInstallManifestRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterInstallManifestResponse(
                manifest="manifest_value",
            )
        )
        response = await client.generate_attached_cluster_install_manifest(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.GenerateAttachedClusterInstallManifestRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterInstallManifestResponse
    )
    assert response.manifest == "manifest_value"


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_async_from_dict():
    await test_generate_attached_cluster_install_manifest_async(request_type=dict)


def test_generate_attached_cluster_install_manifest_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GenerateAttachedClusterInstallManifestRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        call.return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )
        client.generate_attached_cluster_install_manifest(request)

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
async def test_generate_attached_cluster_install_manifest_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GenerateAttachedClusterInstallManifestRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )
        await client.generate_attached_cluster_install_manifest(request)

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


def test_generate_attached_cluster_install_manifest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_attached_cluster_install_manifest(
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].attached_cluster_id
        mock_val = "attached_cluster_id_value"
        assert arg == mock_val


def test_generate_attached_cluster_install_manifest_flattened_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_attached_cluster_install_manifest(
            attached_service.GenerateAttachedClusterInstallManifestRequest(),
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_flattened_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_install_manifest), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_attached_cluster_install_manifest(
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].attached_cluster_id
        mock_val = "attached_cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_generate_attached_cluster_install_manifest_flattened_error_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_attached_cluster_install_manifest(
            attached_service.GenerateAttachedClusterInstallManifestRequest(),
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GenerateAttachedClusterAgentTokenRequest,
        dict,
    ],
)
def test_generate_attached_cluster_agent_token(request_type, transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = attached_service.GenerateAttachedClusterAgentTokenResponse(
            access_token="access_token_value",
            expires_in=1078,
            token_type="token_type_value",
        )
        response = client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = attached_service.GenerateAttachedClusterAgentTokenRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterAgentTokenResponse
    )
    assert response.access_token == "access_token_value"
    assert response.expires_in == 1078
    assert response.token_type == "token_type_value"


def test_generate_attached_cluster_agent_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_attached_cluster_agent_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GenerateAttachedClusterAgentTokenRequest()


def test_generate_attached_cluster_agent_token_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = attached_service.GenerateAttachedClusterAgentTokenRequest(
        attached_cluster="attached_cluster_value",
        subject_token="subject_token_value",
        subject_token_type="subject_token_type_value",
        version="version_value",
        grant_type="grant_type_value",
        audience="audience_value",
        scope="scope_value",
        requested_token_type="requested_token_type_value",
        options="options_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_attached_cluster_agent_token(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GenerateAttachedClusterAgentTokenRequest(
            attached_cluster="attached_cluster_value",
            subject_token="subject_token_value",
            subject_token_type="subject_token_type_value",
            version="version_value",
            grant_type="grant_type_value",
            audience="audience_value",
            scope="scope_value",
            requested_token_type="requested_token_type_value",
            options="options_value",
        )


def test_generate_attached_cluster_agent_token_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_attached_cluster_agent_token
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_attached_cluster_agent_token
        ] = mock_rpc
        request = {}
        client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_attached_cluster_agent_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_attached_cluster_agent_token_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterAgentTokenResponse(
                access_token="access_token_value",
                expires_in=1078,
                token_type="token_type_value",
            )
        )
        response = await client.generate_attached_cluster_agent_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == attached_service.GenerateAttachedClusterAgentTokenRequest()


@pytest.mark.asyncio
async def test_generate_attached_cluster_agent_token_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = AttachedClustersAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_attached_cluster_agent_token
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_attached_cluster_agent_token
        ] = mock_rpc

        request = {}
        await client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.generate_attached_cluster_agent_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_attached_cluster_agent_token_async(
    transport: str = "grpc_asyncio",
    request_type=attached_service.GenerateAttachedClusterAgentTokenRequest,
):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterAgentTokenResponse(
                access_token="access_token_value",
                expires_in=1078,
                token_type="token_type_value",
            )
        )
        response = await client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = attached_service.GenerateAttachedClusterAgentTokenRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterAgentTokenResponse
    )
    assert response.access_token == "access_token_value"
    assert response.expires_in == 1078
    assert response.token_type == "token_type_value"


@pytest.mark.asyncio
async def test_generate_attached_cluster_agent_token_async_from_dict():
    await test_generate_attached_cluster_agent_token_async(request_type=dict)


def test_generate_attached_cluster_agent_token_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GenerateAttachedClusterAgentTokenRequest()

    request.attached_cluster = "attached_cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        call.return_value = attached_service.GenerateAttachedClusterAgentTokenResponse()
        client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attached_cluster=attached_cluster_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_attached_cluster_agent_token_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = attached_service.GenerateAttachedClusterAgentTokenRequest()

    request.attached_cluster = "attached_cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_attached_cluster_agent_token), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            attached_service.GenerateAttachedClusterAgentTokenResponse()
        )
        await client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "attached_cluster=attached_cluster_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.CreateAttachedClusterRequest,
        dict,
    ],
)
def test_create_attached_cluster_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["attached_cluster"] = {
        "name": "name_value",
        "description": "description_value",
        "oidc_config": {"issuer_url": "issuer_url_value", "jwks": b"jwks_blob"},
        "platform_version": "platform_version_value",
        "distribution": "distribution_value",
        "cluster_region": "cluster_region_value",
        "fleet": {"project": "project_value", "membership": "membership_value"},
        "state": 1,
        "uid": "uid_value",
        "reconciling": True,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "etag": "etag_value",
        "kubernetes_version": "kubernetes_version_value",
        "annotations": {},
        "workload_identity_config": {
            "issuer_uri": "issuer_uri_value",
            "workload_pool": "workload_pool_value",
            "identity_provider": "identity_provider_value",
        },
        "logging_config": {"component_config": {"enable_components": [1]}},
        "errors": [{"message": "message_value"}],
        "authorization": {
            "admin_users": [{"username": "username_value"}],
            "admin_groups": [{"group": "group_value"}],
        },
        "monitoring_config": {"managed_prometheus_config": {"enabled": True}},
        "proxy_config": {
            "kubernetes_secret": {"name": "name_value", "namespace": "namespace_value"}
        },
        "binary_authorization": {"evaluation_mode": 1},
        "security_posture_config": {"vulnerability_mode": 1},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = attached_service.CreateAttachedClusterRequest.meta.fields[
        "attached_cluster"
    ]

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
    for field, value in request_init["attached_cluster"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["attached_cluster"][field])):
                    del request_init["attached_cluster"][field][i][subfield]
            else:
                del request_init["attached_cluster"][field][subfield]
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
        response = client.create_attached_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_attached_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_attached_cluster
        ] = mock_rpc

        request = {}
        client.create_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_attached_cluster_rest_required_fields(
    request_type=attached_service.CreateAttachedClusterRequest,
):
    transport_class = transports.AttachedClustersRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["attached_cluster_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "attachedClusterId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "attachedClusterId" in jsonified_request
    assert jsonified_request["attachedClusterId"] == request_init["attached_cluster_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["attachedClusterId"] = "attached_cluster_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_attached_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "attached_cluster_id",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "attachedClusterId" in jsonified_request
    assert jsonified_request["attachedClusterId"] == "attached_cluster_id_value"

    client = AttachedClustersClient(
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

            response = client.create_attached_cluster(request)

            expected_params = [
                (
                    "attachedClusterId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_attached_cluster_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_attached_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "attachedClusterId",
                "validateOnly",
            )
        )
        & set(
            (
                "parent",
                "attachedCluster",
                "attachedClusterId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_attached_cluster_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_create_attached_cluster"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_create_attached_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.CreateAttachedClusterRequest.pb(
            attached_service.CreateAttachedClusterRequest()
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

        request = attached_service.CreateAttachedClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_attached_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_attached_cluster_rest_bad_request(
    transport: str = "rest", request_type=attached_service.CreateAttachedClusterRequest
):
    client = AttachedClustersClient(
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
        client.create_attached_cluster(request)


def test_create_attached_cluster_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_attached_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/attachedClusters"
            % client.transport._host,
            args[1],
        )


def test_create_attached_cluster_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_attached_cluster(
            attached_service.CreateAttachedClusterRequest(),
            parent="parent_value",
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            attached_cluster_id="attached_cluster_id_value",
        )


def test_create_attached_cluster_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.UpdateAttachedClusterRequest,
        dict,
    ],
)
def test_update_attached_cluster_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attached_cluster": {
            "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
        }
    }
    request_init["attached_cluster"] = {
        "name": "projects/sample1/locations/sample2/attachedClusters/sample3",
        "description": "description_value",
        "oidc_config": {"issuer_url": "issuer_url_value", "jwks": b"jwks_blob"},
        "platform_version": "platform_version_value",
        "distribution": "distribution_value",
        "cluster_region": "cluster_region_value",
        "fleet": {"project": "project_value", "membership": "membership_value"},
        "state": 1,
        "uid": "uid_value",
        "reconciling": True,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "etag": "etag_value",
        "kubernetes_version": "kubernetes_version_value",
        "annotations": {},
        "workload_identity_config": {
            "issuer_uri": "issuer_uri_value",
            "workload_pool": "workload_pool_value",
            "identity_provider": "identity_provider_value",
        },
        "logging_config": {"component_config": {"enable_components": [1]}},
        "errors": [{"message": "message_value"}],
        "authorization": {
            "admin_users": [{"username": "username_value"}],
            "admin_groups": [{"group": "group_value"}],
        },
        "monitoring_config": {"managed_prometheus_config": {"enabled": True}},
        "proxy_config": {
            "kubernetes_secret": {"name": "name_value", "namespace": "namespace_value"}
        },
        "binary_authorization": {"evaluation_mode": 1},
        "security_posture_config": {"vulnerability_mode": 1},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = attached_service.UpdateAttachedClusterRequest.meta.fields[
        "attached_cluster"
    ]

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
    for field, value in request_init["attached_cluster"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["attached_cluster"][field])):
                    del request_init["attached_cluster"][field][i][subfield]
            else:
                del request_init["attached_cluster"][field][subfield]
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
        response = client.update_attached_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_attached_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_attached_cluster
        ] = mock_rpc

        request = {}
        client.update_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_attached_cluster_rest_required_fields(
    request_type=attached_service.UpdateAttachedClusterRequest,
):
    transport_class = transports.AttachedClustersRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_attached_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AttachedClustersClient(
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

            response = client.update_attached_cluster(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_attached_cluster_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_attached_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(
            (
                "attachedCluster",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_attached_cluster_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_update_attached_cluster"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_update_attached_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.UpdateAttachedClusterRequest.pb(
            attached_service.UpdateAttachedClusterRequest()
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

        request = attached_service.UpdateAttachedClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_attached_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_attached_cluster_rest_bad_request(
    transport: str = "rest", request_type=attached_service.UpdateAttachedClusterRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attached_cluster": {
            "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
        }
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
        client.update_attached_cluster(request)


def test_update_attached_cluster_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "attached_cluster": {
                "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_attached_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{attached_cluster.name=projects/*/locations/*/attachedClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_update_attached_cluster_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_attached_cluster(
            attached_service.UpdateAttachedClusterRequest(),
            attached_cluster=attached_resources.AttachedCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_attached_cluster_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.ImportAttachedClusterRequest,
        dict,
    ],
)
def test_import_attached_cluster_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        response = client.import_attached_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_import_attached_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.import_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.import_attached_cluster
        ] = mock_rpc

        request = {}
        client.import_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.import_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_import_attached_cluster_rest_required_fields(
    request_type=attached_service.ImportAttachedClusterRequest,
):
    transport_class = transports.AttachedClustersRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["fleet_membership"] = ""
    request_init["platform_version"] = ""
    request_init["distribution"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).import_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"
    jsonified_request["fleetMembership"] = "fleet_membership_value"
    jsonified_request["platformVersion"] = "platform_version_value"
    jsonified_request["distribution"] = "distribution_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).import_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "fleetMembership" in jsonified_request
    assert jsonified_request["fleetMembership"] == "fleet_membership_value"
    assert "platformVersion" in jsonified_request
    assert jsonified_request["platformVersion"] == "platform_version_value"
    assert "distribution" in jsonified_request
    assert jsonified_request["distribution"] == "distribution_value"

    client = AttachedClustersClient(
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

            response = client.import_attached_cluster(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_import_attached_cluster_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.import_attached_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "fleetMembership",
                "platformVersion",
                "distribution",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_import_attached_cluster_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_import_attached_cluster"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_import_attached_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.ImportAttachedClusterRequest.pb(
            attached_service.ImportAttachedClusterRequest()
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

        request = attached_service.ImportAttachedClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.import_attached_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_import_attached_cluster_rest_bad_request(
    transport: str = "rest", request_type=attached_service.ImportAttachedClusterRequest
):
    client = AttachedClustersClient(
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
        client.import_attached_cluster(request)


def test_import_attached_cluster_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.import_attached_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/attachedClusters:import"
            % client.transport._host,
            args[1],
        )


def test_import_attached_cluster_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_attached_cluster(
            attached_service.ImportAttachedClusterRequest(),
            parent="parent_value",
            fleet_membership="fleet_membership_value",
        )


def test_import_attached_cluster_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GetAttachedClusterRequest,
        dict,
    ],
)
def test_get_attached_cluster_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_resources.AttachedCluster(
            name="name_value",
            description="description_value",
            platform_version="platform_version_value",
            distribution="distribution_value",
            cluster_region="cluster_region_value",
            state=attached_resources.AttachedCluster.State.PROVISIONING,
            uid="uid_value",
            reconciling=True,
            etag="etag_value",
            kubernetes_version="kubernetes_version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attached_resources.AttachedCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_attached_cluster(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedCluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.platform_version == "platform_version_value"
    assert response.distribution == "distribution_value"
    assert response.cluster_region == "cluster_region_value"
    assert response.state == attached_resources.AttachedCluster.State.PROVISIONING
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"
    assert response.kubernetes_version == "kubernetes_version_value"


def test_get_attached_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_attached_cluster in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_attached_cluster
        ] = mock_rpc

        request = {}
        client.get_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_attached_cluster_rest_required_fields(
    request_type=attached_service.GetAttachedClusterRequest,
):
    transport_class = transports.AttachedClustersRestTransport

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
    ).get_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attached_resources.AttachedCluster()
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
            return_value = attached_resources.AttachedCluster.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_attached_cluster(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_attached_cluster_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_attached_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_attached_cluster_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_get_attached_cluster"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_get_attached_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.GetAttachedClusterRequest.pb(
            attached_service.GetAttachedClusterRequest()
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
        req.return_value._content = attached_resources.AttachedCluster.to_json(
            attached_resources.AttachedCluster()
        )

        request = attached_service.GetAttachedClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attached_resources.AttachedCluster()

        client.get_attached_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_attached_cluster_rest_bad_request(
    transport: str = "rest", request_type=attached_service.GetAttachedClusterRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
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
        client.get_attached_cluster(request)


def test_get_attached_cluster_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_resources.AttachedCluster()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
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
        return_value = attached_resources.AttachedCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_attached_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/attachedClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_get_attached_cluster_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attached_cluster(
            attached_service.GetAttachedClusterRequest(),
            name="name_value",
        )


def test_get_attached_cluster_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.ListAttachedClustersRequest,
        dict,
    ],
)
def test_list_attached_clusters_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_service.ListAttachedClustersResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attached_service.ListAttachedClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_attached_clusters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAttachedClustersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_attached_clusters_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_attached_clusters
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_attached_clusters
        ] = mock_rpc

        request = {}
        client.list_attached_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_attached_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_attached_clusters_rest_required_fields(
    request_type=attached_service.ListAttachedClustersRequest,
):
    transport_class = transports.AttachedClustersRestTransport

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
    ).list_attached_clusters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_attached_clusters._get_unset_required_fields(jsonified_request)
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

    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attached_service.ListAttachedClustersResponse()
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
            return_value = attached_service.ListAttachedClustersResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_attached_clusters(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_attached_clusters_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_attached_clusters._get_unset_required_fields({})
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
def test_list_attached_clusters_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_list_attached_clusters"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_list_attached_clusters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.ListAttachedClustersRequest.pb(
            attached_service.ListAttachedClustersRequest()
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
            attached_service.ListAttachedClustersResponse.to_json(
                attached_service.ListAttachedClustersResponse()
            )
        )

        request = attached_service.ListAttachedClustersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attached_service.ListAttachedClustersResponse()

        client.list_attached_clusters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_attached_clusters_rest_bad_request(
    transport: str = "rest", request_type=attached_service.ListAttachedClustersRequest
):
    client = AttachedClustersClient(
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
        client.list_attached_clusters(request)


def test_list_attached_clusters_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_service.ListAttachedClustersResponse()

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
        # Convert return value to protobuf type
        return_value = attached_service.ListAttachedClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_attached_clusters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/attachedClusters"
            % client.transport._host,
            args[1],
        )


def test_list_attached_clusters_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_attached_clusters(
            attached_service.ListAttachedClustersRequest(),
            parent="parent_value",
        )


def test_list_attached_clusters_rest_pager(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="abc",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[],
                next_page_token="def",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                ],
                next_page_token="ghi",
            ),
            attached_service.ListAttachedClustersResponse(
                attached_clusters=[
                    attached_resources.AttachedCluster(),
                    attached_resources.AttachedCluster(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            attached_service.ListAttachedClustersResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_attached_clusters(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, attached_resources.AttachedCluster) for i in results)

        pages = list(client.list_attached_clusters(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.DeleteAttachedClusterRequest,
        dict,
    ],
)
def test_delete_attached_cluster_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
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
        response = client.delete_attached_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_attached_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_attached_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_attached_cluster
        ] = mock_rpc

        request = {}
        client.delete_attached_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_attached_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_attached_cluster_rest_required_fields(
    request_type=attached_service.DeleteAttachedClusterRequest,
):
    transport_class = transports.AttachedClustersRestTransport

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
    ).delete_attached_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_attached_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "etag",
            "ignore_errors",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = AttachedClustersClient(
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_attached_cluster(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_attached_cluster_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_attached_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "etag",
                "ignoreErrors",
                "validateOnly",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_attached_cluster_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_delete_attached_cluster"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_delete_attached_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.DeleteAttachedClusterRequest.pb(
            attached_service.DeleteAttachedClusterRequest()
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

        request = attached_service.DeleteAttachedClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_attached_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_attached_cluster_rest_bad_request(
    transport: str = "rest", request_type=attached_service.DeleteAttachedClusterRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
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
        client.delete_attached_cluster(request)


def test_delete_attached_cluster_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/attachedClusters/sample3"
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

        client.delete_attached_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/attachedClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_attached_cluster_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_attached_cluster(
            attached_service.DeleteAttachedClusterRequest(),
            name="name_value",
        )


def test_delete_attached_cluster_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GetAttachedServerConfigRequest,
        dict,
    ],
)
def test_get_attached_server_config_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/attachedServerConfig"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_resources.AttachedServerConfig(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attached_resources.AttachedServerConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_attached_server_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, attached_resources.AttachedServerConfig)
    assert response.name == "name_value"


def test_get_attached_server_config_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_attached_server_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_attached_server_config
        ] = mock_rpc

        request = {}
        client.get_attached_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_attached_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_attached_server_config_rest_required_fields(
    request_type=attached_service.GetAttachedServerConfigRequest,
):
    transport_class = transports.AttachedClustersRestTransport

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
    ).get_attached_server_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_attached_server_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attached_resources.AttachedServerConfig()
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
            return_value = attached_resources.AttachedServerConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_attached_server_config(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_attached_server_config_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_attached_server_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_attached_server_config_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "post_get_attached_server_config"
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor, "pre_get_attached_server_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.GetAttachedServerConfigRequest.pb(
            attached_service.GetAttachedServerConfigRequest()
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
        req.return_value._content = attached_resources.AttachedServerConfig.to_json(
            attached_resources.AttachedServerConfig()
        )

        request = attached_service.GetAttachedServerConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attached_resources.AttachedServerConfig()

        client.get_attached_server_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_attached_server_config_rest_bad_request(
    transport: str = "rest",
    request_type=attached_service.GetAttachedServerConfigRequest,
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/attachedServerConfig"}
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
        client.get_attached_server_config(request)


def test_get_attached_server_config_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_resources.AttachedServerConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/attachedServerConfig"
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
        return_value = attached_resources.AttachedServerConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_attached_server_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/attachedServerConfig}"
            % client.transport._host,
            args[1],
        )


def test_get_attached_server_config_rest_flattened_error(transport: str = "rest"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_attached_server_config(
            attached_service.GetAttachedServerConfigRequest(),
            name="name_value",
        )


def test_get_attached_server_config_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GenerateAttachedClusterInstallManifestRequest,
        dict,
    ],
)
def test_generate_attached_cluster_install_manifest_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_service.GenerateAttachedClusterInstallManifestResponse(
            manifest="manifest_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.generate_attached_cluster_install_manifest(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterInstallManifestResponse
    )
    assert response.manifest == "manifest_value"


def test_generate_attached_cluster_install_manifest_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_attached_cluster_install_manifest
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_attached_cluster_install_manifest
        ] = mock_rpc

        request = {}
        client.generate_attached_cluster_install_manifest(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_attached_cluster_install_manifest(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_attached_cluster_install_manifest_rest_required_fields(
    request_type=attached_service.GenerateAttachedClusterInstallManifestRequest,
):
    transport_class = transports.AttachedClustersRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["attached_cluster_id"] = ""
    request_init["platform_version"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "attachedClusterId" not in jsonified_request
    assert "platformVersion" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_attached_cluster_install_manifest._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "attachedClusterId" in jsonified_request
    assert jsonified_request["attachedClusterId"] == request_init["attached_cluster_id"]
    assert "platformVersion" in jsonified_request
    assert jsonified_request["platformVersion"] == request_init["platform_version"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["attachedClusterId"] = "attached_cluster_id_value"
    jsonified_request["platformVersion"] = "platform_version_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_attached_cluster_install_manifest._get_unset_required_fields(
        jsonified_request
    )
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "attached_cluster_id",
            "platform_version",
            "proxy_config",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "attachedClusterId" in jsonified_request
    assert jsonified_request["attachedClusterId"] == "attached_cluster_id_value"
    assert "platformVersion" in jsonified_request
    assert jsonified_request["platformVersion"] == "platform_version_value"

    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attached_service.GenerateAttachedClusterInstallManifestResponse()
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
                attached_service.GenerateAttachedClusterInstallManifestResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.generate_attached_cluster_install_manifest(request)

            expected_params = [
                (
                    "attachedClusterId",
                    "",
                ),
                (
                    "platformVersion",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_generate_attached_cluster_install_manifest_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.generate_attached_cluster_install_manifest._get_unset_required_fields(
            {}
        )
    )
    assert set(unset_fields) == (
        set(
            (
                "attachedClusterId",
                "platformVersion",
                "proxyConfig",
            )
        )
        & set(
            (
                "parent",
                "attachedClusterId",
                "platformVersion",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_attached_cluster_install_manifest_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.AttachedClustersRestInterceptor,
        "post_generate_attached_cluster_install_manifest",
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor,
        "pre_generate_attached_cluster_install_manifest",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.GenerateAttachedClusterInstallManifestRequest.pb(
            attached_service.GenerateAttachedClusterInstallManifestRequest()
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
            attached_service.GenerateAttachedClusterInstallManifestResponse.to_json(
                attached_service.GenerateAttachedClusterInstallManifestResponse()
            )
        )

        request = attached_service.GenerateAttachedClusterInstallManifestRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse()
        )

        client.generate_attached_cluster_install_manifest(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_attached_cluster_install_manifest_rest_bad_request(
    transport: str = "rest",
    request_type=attached_service.GenerateAttachedClusterInstallManifestRequest,
):
    client = AttachedClustersClient(
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
        client.generate_attached_cluster_install_manifest(request)


def test_generate_attached_cluster_install_manifest_rest_flattened():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_service.GenerateAttachedClusterInstallManifestResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = (
            attached_service.GenerateAttachedClusterInstallManifestResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.generate_attached_cluster_install_manifest(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}:generateAttachedClusterInstallManifest"
            % client.transport._host,
            args[1],
        )


def test_generate_attached_cluster_install_manifest_rest_flattened_error(
    transport: str = "rest",
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_attached_cluster_install_manifest(
            attached_service.GenerateAttachedClusterInstallManifestRequest(),
            parent="parent_value",
            attached_cluster_id="attached_cluster_id_value",
        )


def test_generate_attached_cluster_install_manifest_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        attached_service.GenerateAttachedClusterAgentTokenRequest,
        dict,
    ],
)
def test_generate_attached_cluster_agent_token_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attached_cluster": "projects/sample1/locations/sample2/attachedClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = attached_service.GenerateAttachedClusterAgentTokenResponse(
            access_token="access_token_value",
            expires_in=1078,
            token_type="token_type_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = attached_service.GenerateAttachedClusterAgentTokenResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.generate_attached_cluster_agent_token(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, attached_service.GenerateAttachedClusterAgentTokenResponse
    )
    assert response.access_token == "access_token_value"
    assert response.expires_in == 1078
    assert response.token_type == "token_type_value"


def test_generate_attached_cluster_agent_token_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_attached_cluster_agent_token
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_attached_cluster_agent_token
        ] = mock_rpc

        request = {}
        client.generate_attached_cluster_agent_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_attached_cluster_agent_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_attached_cluster_agent_token_rest_required_fields(
    request_type=attached_service.GenerateAttachedClusterAgentTokenRequest,
):
    transport_class = transports.AttachedClustersRestTransport

    request_init = {}
    request_init["attached_cluster"] = ""
    request_init["subject_token"] = ""
    request_init["subject_token_type"] = ""
    request_init["version"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_attached_cluster_agent_token._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["attachedCluster"] = "attached_cluster_value"
    jsonified_request["subjectToken"] = "subject_token_value"
    jsonified_request["subjectTokenType"] = "subject_token_type_value"
    jsonified_request["version"] = "version_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_attached_cluster_agent_token._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "attachedCluster" in jsonified_request
    assert jsonified_request["attachedCluster"] == "attached_cluster_value"
    assert "subjectToken" in jsonified_request
    assert jsonified_request["subjectToken"] == "subject_token_value"
    assert "subjectTokenType" in jsonified_request
    assert jsonified_request["subjectTokenType"] == "subject_token_type_value"
    assert "version" in jsonified_request
    assert jsonified_request["version"] == "version_value"

    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = attached_service.GenerateAttachedClusterAgentTokenResponse()
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
            return_value = (
                attached_service.GenerateAttachedClusterAgentTokenResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.generate_attached_cluster_agent_token(request)

            expected_params = []
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_generate_attached_cluster_agent_token_rest_unset_required_fields():
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.generate_attached_cluster_agent_token._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "attachedCluster",
                "subjectToken",
                "subjectTokenType",
                "version",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_attached_cluster_agent_token_rest_interceptors(null_interceptor):
    transport = transports.AttachedClustersRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.AttachedClustersRestInterceptor(),
    )
    client = AttachedClustersClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.AttachedClustersRestInterceptor,
        "post_generate_attached_cluster_agent_token",
    ) as post, mock.patch.object(
        transports.AttachedClustersRestInterceptor,
        "pre_generate_attached_cluster_agent_token",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = attached_service.GenerateAttachedClusterAgentTokenRequest.pb(
            attached_service.GenerateAttachedClusterAgentTokenRequest()
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
            attached_service.GenerateAttachedClusterAgentTokenResponse.to_json(
                attached_service.GenerateAttachedClusterAgentTokenResponse()
            )
        )

        request = attached_service.GenerateAttachedClusterAgentTokenRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = attached_service.GenerateAttachedClusterAgentTokenResponse()

        client.generate_attached_cluster_agent_token(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_attached_cluster_agent_token_rest_bad_request(
    transport: str = "rest",
    request_type=attached_service.GenerateAttachedClusterAgentTokenRequest,
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "attached_cluster": "projects/sample1/locations/sample2/attachedClusters/sample3"
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
        client.generate_attached_cluster_agent_token(request)


def test_generate_attached_cluster_agent_token_rest_error():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AttachedClustersClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AttachedClustersClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AttachedClustersClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AttachedClustersClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AttachedClustersClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AttachedClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AttachedClustersGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
        transports.AttachedClustersRestTransport,
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
    transport = AttachedClustersClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AttachedClustersGrpcTransport,
    )


def test_attached_clusters_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AttachedClustersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_attached_clusters_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.gke_multicloud_v1.services.attached_clusters.transports.AttachedClustersTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AttachedClustersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_attached_cluster",
        "update_attached_cluster",
        "import_attached_cluster",
        "get_attached_cluster",
        "list_attached_clusters",
        "delete_attached_cluster",
        "get_attached_server_config",
        "generate_attached_cluster_install_manifest",
        "generate_attached_cluster_agent_token",
        "get_operation",
        "cancel_operation",
        "delete_operation",
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


def test_attached_clusters_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.gke_multicloud_v1.services.attached_clusters.transports.AttachedClustersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AttachedClustersTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_attached_clusters_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.gke_multicloud_v1.services.attached_clusters.transports.AttachedClustersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AttachedClustersTransport()
        adc.assert_called_once()


def test_attached_clusters_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AttachedClustersClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
    ],
)
def test_attached_clusters_transport_auth_adc(transport_class):
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
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
        transports.AttachedClustersRestTransport,
    ],
)
def test_attached_clusters_transport_auth_gdch_credentials(transport_class):
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
        (transports.AttachedClustersGrpcTransport, grpc_helpers),
        (transports.AttachedClustersGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_attached_clusters_transport_create_channel(transport_class, grpc_helpers):
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
            "gkemulticloud.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="gkemulticloud.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
    ],
)
def test_attached_clusters_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_attached_clusters_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.AttachedClustersRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_attached_clusters_rest_lro_client():
    client = AttachedClustersClient(
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
def test_attached_clusters_host_no_port(transport_name):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gkemulticloud.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "gkemulticloud.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://gkemulticloud.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_attached_clusters_host_with_port(transport_name):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gkemulticloud.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "gkemulticloud.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://gkemulticloud.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_attached_clusters_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = AttachedClustersClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = AttachedClustersClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_attached_cluster._session
    session2 = client2.transport.create_attached_cluster._session
    assert session1 != session2
    session1 = client1.transport.update_attached_cluster._session
    session2 = client2.transport.update_attached_cluster._session
    assert session1 != session2
    session1 = client1.transport.import_attached_cluster._session
    session2 = client2.transport.import_attached_cluster._session
    assert session1 != session2
    session1 = client1.transport.get_attached_cluster._session
    session2 = client2.transport.get_attached_cluster._session
    assert session1 != session2
    session1 = client1.transport.list_attached_clusters._session
    session2 = client2.transport.list_attached_clusters._session
    assert session1 != session2
    session1 = client1.transport.delete_attached_cluster._session
    session2 = client2.transport.delete_attached_cluster._session
    assert session1 != session2
    session1 = client1.transport.get_attached_server_config._session
    session2 = client2.transport.get_attached_server_config._session
    assert session1 != session2
    session1 = client1.transport.generate_attached_cluster_install_manifest._session
    session2 = client2.transport.generate_attached_cluster_install_manifest._session
    assert session1 != session2
    session1 = client1.transport.generate_attached_cluster_agent_token._session
    session2 = client2.transport.generate_attached_cluster_agent_token._session
    assert session1 != session2


def test_attached_clusters_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AttachedClustersGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_attached_clusters_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AttachedClustersGrpcAsyncIOTransport(
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
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
    ],
)
def test_attached_clusters_transport_channel_mtls_with_client_cert_source(
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
        transports.AttachedClustersGrpcTransport,
        transports.AttachedClustersGrpcAsyncIOTransport,
    ],
)
def test_attached_clusters_transport_channel_mtls_with_adc(transport_class):
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


def test_attached_clusters_grpc_lro_client():
    client = AttachedClustersClient(
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


def test_attached_clusters_grpc_lro_async_client():
    client = AttachedClustersAsyncClient(
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


def test_attached_cluster_path():
    project = "squid"
    location = "clam"
    attached_cluster = "whelk"
    expected = "projects/{project}/locations/{location}/attachedClusters/{attached_cluster}".format(
        project=project,
        location=location,
        attached_cluster=attached_cluster,
    )
    actual = AttachedClustersClient.attached_cluster_path(
        project, location, attached_cluster
    )
    assert expected == actual


def test_parse_attached_cluster_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "attached_cluster": "nudibranch",
    }
    path = AttachedClustersClient.attached_cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_attached_cluster_path(path)
    assert expected == actual


def test_attached_server_config_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}/attachedServerConfig".format(
        project=project,
        location=location,
    )
    actual = AttachedClustersClient.attached_server_config_path(project, location)
    assert expected == actual


def test_parse_attached_server_config_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = AttachedClustersClient.attached_server_config_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_attached_server_config_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AttachedClustersClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = AttachedClustersClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = AttachedClustersClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = AttachedClustersClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = AttachedClustersClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = AttachedClustersClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = AttachedClustersClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = AttachedClustersClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = AttachedClustersClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = AttachedClustersClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AttachedClustersClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AttachedClustersTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AttachedClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AttachedClustersTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AttachedClustersClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
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
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
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
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
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
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = AttachedClustersClient(
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
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc_asyncio"):
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
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
async def test_delete_operation_field_headers_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
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


def test_delete_operation_from_dict():
    client = AttachedClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = AttachedClustersClient(
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
    client = AttachedClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = AttachedClustersClient(
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
        client = AttachedClustersClient(
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
        (AttachedClustersClient, transports.AttachedClustersGrpcTransport),
        (AttachedClustersAsyncClient, transports.AttachedClustersGrpcAsyncIOTransport),
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
