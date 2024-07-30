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

from google.api import httpbody_pb2  # type: ignore
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
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
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

from google.cloud.devtools.cloudbuild_v1.services.cloud_build import (
    CloudBuildAsyncClient,
    CloudBuildClient,
    pagers,
    transports,
)
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild


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

    assert CloudBuildClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudBuildClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test__read_environment_variables():
    assert CloudBuildClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert CloudBuildClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert CloudBuildClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            CloudBuildClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert CloudBuildClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert CloudBuildClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert CloudBuildClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            CloudBuildClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert CloudBuildClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert CloudBuildClient._get_client_cert_source(None, False) is None
    assert (
        CloudBuildClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        CloudBuildClient._get_client_cert_source(mock_provided_cert_source, True)
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
                CloudBuildClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                CloudBuildClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    CloudBuildClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildClient),
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = CloudBuildClient._DEFAULT_UNIVERSE
    default_endpoint = CloudBuildClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CloudBuildClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        CloudBuildClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        CloudBuildClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == CloudBuildClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudBuildClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        CloudBuildClient._get_api_endpoint(None, None, default_universe, "always")
        == CloudBuildClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudBuildClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == CloudBuildClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        CloudBuildClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        CloudBuildClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        CloudBuildClient._get_api_endpoint(
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
        CloudBuildClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        CloudBuildClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        CloudBuildClient._get_universe_domain(None, None)
        == CloudBuildClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        CloudBuildClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest"),
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
        (CloudBuildClient, "grpc"),
        (CloudBuildAsyncClient, "grpc_asyncio"),
        (CloudBuildClient, "rest"),
    ],
)
def test_cloud_build_client_from_service_account_info(client_class, transport_name):
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
            "cloudbuild.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudbuild.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudBuildGrpcTransport, "grpc"),
        (transports.CloudBuildGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CloudBuildRestTransport, "rest"),
    ],
)
def test_cloud_build_client_service_account_always_use_jwt(
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
        (CloudBuildClient, "grpc"),
        (CloudBuildAsyncClient, "grpc_asyncio"),
        (CloudBuildClient, "rest"),
    ],
)
def test_cloud_build_client_from_service_account_file(client_class, transport_name):
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
            "cloudbuild.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudbuild.googleapis.com"
        )


def test_cloud_build_client_get_transport_class():
    transport = CloudBuildClient.get_transport_class()
    available_transports = [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildRestTransport,
    ]
    assert transport in available_transports

    transport = CloudBuildClient.get_transport_class("grpc")
    assert transport == transports.CloudBuildGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest"),
    ],
)
@mock.patch.object(
    CloudBuildClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildClient),
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildAsyncClient),
)
def test_cloud_build_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "true"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "false"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest", "true"),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    CloudBuildClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildClient),
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_build_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient])
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
def test_cloud_build_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient])
@mock.patch.object(
    CloudBuildClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildClient),
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(CloudBuildAsyncClient),
)
def test_cloud_build_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = CloudBuildClient._DEFAULT_UNIVERSE
    default_endpoint = CloudBuildClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = CloudBuildClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest"),
    ],
)
def test_cloud_build_client_client_options_scopes(
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", grpc_helpers),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (CloudBuildClient, transports.CloudBuildRestTransport, "rest", None),
    ],
)
def test_cloud_build_client_client_options_credentials_file(
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


def test_cloud_build_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBuildClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", grpc_helpers),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_build_client_create_channel_credentials_file(
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
            "cloudbuild.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="cloudbuild.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildRequest,
        dict,
    ],
)
def test_create_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest()


def test_create_build_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.CreateBuildRequest(
        parent="parent_value",
        project_id="project_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_build(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest(
            parent="parent_value",
            project_id="project_id_value",
        )


def test_create_build_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_build] = mock_rpc
        request = {}
        client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_build_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest()


@pytest.mark.asyncio
async def test_create_build_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_build
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_build
        ] = mock_object

        request = {}
        await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_build_async_from_dict():
    await test_create_build_async(request_type=dict)


def test_create_build_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build(
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].build
        mock_val = cloudbuild.Build(name="name_value")
        assert arg == mock_val


def test_create_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build(
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].build
        mock_val = cloudbuild.Build(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildRequest,
        dict,
    ],
)
def test_get_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )
        response = client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_get_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest()


def test_get_build_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.GetBuildRequest(
        name="name_value",
        project_id="project_id_value",
        id="id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_build(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest(
            name="name_value",
            project_id="project_id_value",
            id="id_value",
        )


def test_get_build_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_build] = mock_rpc
        request = {}
        client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_build_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.get_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest()


@pytest.mark.asyncio
async def test_get_build_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_build
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_build
        ] = mock_object

        request = {}
        await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_build_async_from_dict():
    await test_get_build_async(request_type=dict)


def test_get_build_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildRequest(
        **{"name": "projects/sample1/locations/sample2/builds/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        call.return_value = cloudbuild.Build()
        client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_get_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build(
            cloudbuild.GetBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_get_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build(
            cloudbuild.GetBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildsRequest,
        dict,
    ],
)
def test_list_builds(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListBuildsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_builds_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_builds()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest()


def test_list_builds_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.ListBuildsRequest(
        parent="parent_value",
        project_id="project_id_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_builds(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest(
            parent="parent_value",
            project_id="project_id_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_builds_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_builds in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_builds] = mock_rpc
        request = {}
        client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_builds(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_builds_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_builds()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest()


@pytest.mark.asyncio
async def test_list_builds_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_builds
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_builds
        ] = mock_object

        request = {}
        await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_builds(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_builds_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildsRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListBuildsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_builds_async_from_dict():
    await test_list_builds_async(request_type=dict)


def test_list_builds_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildsRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        call.return_value = cloudbuild.ListBuildsResponse()
        client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_builds_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_builds(
            project_id="project_id_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


def test_list_builds_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_builds_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_builds(
            project_id="project_id_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_builds_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


def test_list_builds_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_builds(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in results)


def test_list_builds_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_builds(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_builds_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_builds(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in responses)


@pytest.mark.asyncio
async def test_list_builds_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_builds(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CancelBuildRequest,
        dict,
    ],
)
def test_cancel_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )
        response = client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CancelBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_cancel_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.cancel_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest()


def test_cancel_build_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.CancelBuildRequest(
        name="name_value",
        project_id="project_id_value",
        id="id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.cancel_build(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest(
            name="name_value",
            project_id="project_id_value",
            id="id_value",
        )


def test_cancel_build_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.cancel_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.cancel_build] = mock_rpc
        request = {}
        client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.cancel_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_cancel_build_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.cancel_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest()


@pytest.mark.asyncio
async def test_cancel_build_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.cancel_build
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.cancel_build
        ] = mock_object

        request = {}
        await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.cancel_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_cancel_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CancelBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CancelBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_cancel_build_async_from_dict():
    await test_cancel_build_async(request_type=dict)


def test_cancel_build_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CancelBuildRequest(
        **{"name": "projects/sample1/locations/sample2/builds/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        call.return_value = cloudbuild.Build()
        client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_cancel_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_cancel_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_cancel_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RetryBuildRequest,
        dict,
    ],
)
def test_retry_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.RetryBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_retry_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.retry_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest()


def test_retry_build_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.RetryBuildRequest(
        name="name_value",
        project_id="project_id_value",
        id="id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.retry_build(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest(
            name="name_value",
            project_id="project_id_value",
            id="id_value",
        )


def test_retry_build_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.retry_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.retry_build] = mock_rpc
        request = {}
        client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.retry_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_retry_build_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.retry_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest()


@pytest.mark.asyncio
async def test_retry_build_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.retry_build
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.retry_build
        ] = mock_object

        request = {}
        await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.retry_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_retry_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RetryBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.RetryBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_retry_build_async_from_dict():
    await test_retry_build_async(request_type=dict)


def test_retry_build_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RetryBuildRequest(
        **{"name": "projects/sample1/locations/sample2/builds/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_retry_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retry_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_retry_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_retry_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retry_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_retry_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ApproveBuildRequest,
        dict,
    ],
)
def test_approve_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ApproveBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_approve_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.approve_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest()


def test_approve_build_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.ApproveBuildRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.approve_build(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest(
            name="name_value",
        )


def test_approve_build_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.approve_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.approve_build] = mock_rpc
        request = {}
        client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.approve_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_approve_build_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.approve_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest()


@pytest.mark.asyncio
async def test_approve_build_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.approve_build
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.approve_build
        ] = mock_object

        request = {}
        await client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.approve_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_approve_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ApproveBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ApproveBuildRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_approve_build_async_from_dict():
    await test_approve_build_async(request_type=dict)


def test_approve_build_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ApproveBuildRequest(
        **{"name": "projects/sample1/locations/sample2/builds/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_approve_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.approve_build(
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].approval_result
        mock_val = cloudbuild.ApprovalResult(approver_account="approver_account_value")
        assert arg == mock_val


def test_approve_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_build(
            cloudbuild.ApproveBuildRequest(),
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )


@pytest.mark.asyncio
async def test_approve_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.approve_build(
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].approval_result
        mock_val = cloudbuild.ApprovalResult(approver_account="approver_account_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_approve_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.approve_build(
            cloudbuild.ApproveBuildRequest(),
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildTriggerRequest,
        dict,
    ],
)
def test_create_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_create_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest()


def test_create_build_trigger_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.CreateBuildTriggerRequest(
        parent="parent_value",
        project_id="project_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_build_trigger(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest(
            parent="parent_value",
            project_id="project_id_value",
        )


def test_create_build_trigger_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_build_trigger
        ] = mock_rpc
        request = {}
        client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_build_trigger_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.create_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_create_build_trigger_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_build_trigger
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_build_trigger
        ] = mock_object

        request = {}
        await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_create_build_trigger_async_from_dict():
    await test_create_build_trigger_async(request_type=dict)


def test_create_build_trigger_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildTriggerRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


def test_create_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildTriggerRequest,
        dict,
    ],
)
def test_get_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_get_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest()


def test_get_build_trigger_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.GetBuildTriggerRequest(
        name="name_value",
        project_id="project_id_value",
        trigger_id="trigger_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_build_trigger(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest(
            name="name_value",
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_get_build_trigger_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_build_trigger in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_build_trigger
        ] = mock_rpc
        request = {}
        client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_build_trigger_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.get_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest()


@pytest.mark.asyncio
async def test_get_build_trigger_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_build_trigger
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_build_trigger
        ] = mock_object

        request = {}
        await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_build_trigger_async_from_dict():
    await test_get_build_trigger_async(request_type=dict)


def test_get_build_trigger_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildTriggerRequest(
        **{"name": "projects/sample1/locations/sample2/triggers/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


def test_get_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildTriggersRequest,
        dict,
    ],
)
def test_list_build_triggers(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListBuildTriggersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_build_triggers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_build_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest()


def test_list_build_triggers_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.ListBuildTriggersRequest(
        parent="parent_value",
        project_id="project_id_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_build_triggers(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest(
            parent="parent_value",
            project_id="project_id_value",
            page_token="page_token_value",
        )


def test_list_build_triggers_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_build_triggers in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_build_triggers
        ] = mock_rpc
        request = {}
        client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_build_triggers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_build_triggers_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_build_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest()


@pytest.mark.asyncio
async def test_list_build_triggers_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_build_triggers
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_build_triggers
        ] = mock_object

        request = {}
        await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_build_triggers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_build_triggers_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildTriggersRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListBuildTriggersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_build_triggers_async_from_dict():
    await test_list_build_triggers_async(request_type=dict)


def test_list_build_triggers_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildTriggersRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        call.return_value = cloudbuild.ListBuildTriggersResponse()
        client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_build_triggers_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_build_triggers(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


def test_list_build_triggers_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(),
            project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_build_triggers(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(),
            project_id="project_id_value",
        )


def test_list_build_triggers_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_build_triggers(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in results)


def test_list_build_triggers_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_build_triggers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_build_triggers_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_build_triggers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in responses)


@pytest.mark.asyncio
async def test_list_build_triggers_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_build_triggers(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteBuildTriggerRequest,
        dict,
    ],
)
def test_delete_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.DeleteBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()


def test_delete_build_trigger_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.DeleteBuildTriggerRequest(
        name="name_value",
        project_id="project_id_value",
        trigger_id="trigger_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_build_trigger(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest(
            name="name_value",
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_delete_build_trigger_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_build_trigger
        ] = mock_rpc
        request = {}
        client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_build_trigger_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()


@pytest.mark.asyncio
async def test_delete_build_trigger_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_build_trigger
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_build_trigger
        ] = mock_object

        request = {}
        await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.DeleteBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_build_trigger_async_from_dict():
    await test_delete_build_trigger_async(request_type=dict)


def test_delete_build_trigger_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteBuildTriggerRequest(
        **{"name": "projects/sample1/locations/sample2/triggers/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        call.return_value = None
        client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


def test_delete_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateBuildTriggerRequest,
        dict,
    ],
)
def test_update_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.UpdateBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_update_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()


def test_update_build_trigger_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.UpdateBuildTriggerRequest(
        project_id="project_id_value",
        trigger_id="trigger_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_build_trigger(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_update_build_trigger_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_build_trigger
        ] = mock_rpc
        request = {}
        client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_build_trigger_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.update_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_update_build_trigger_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_build_trigger
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_build_trigger
        ] = mock_object

        request = {}
        await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.UpdateBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_update_build_trigger_async_from_dict():
    await test_update_build_trigger_async(request_type=dict)


def test_update_build_trigger_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateBuildTriggerRequest(
        **{
            "trigger": {
                "resource_name": "projects/sample1/locations/sample2/triggers/sample3"
            }
        }
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_update_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


def test_update_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RunBuildTriggerRequest,
        dict,
    ],
)
def test_run_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.RunBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest()


def test_run_build_trigger_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.RunBuildTriggerRequest(
        name="name_value",
        project_id="project_id_value",
        trigger_id="trigger_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.run_build_trigger(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest(
            name="name_value",
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_run_build_trigger_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_build_trigger in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_build_trigger
        ] = mock_rpc
        request = {}
        client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.run_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_run_build_trigger_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest()


@pytest.mark.asyncio
async def test_run_build_trigger_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.run_build_trigger
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.run_build_trigger
        ] = mock_object

        request = {}
        await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.run_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_run_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RunBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.RunBuildTriggerRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_build_trigger_async_from_dict():
    await test_run_build_trigger_async(request_type=dict)


def test_run_build_trigger_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RunBuildTriggerRequest(
        **{"name": "projects/sample1/locations/sample2/triggers/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_run_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = cloudbuild.RepoSource(project_id="project_id_value")
        assert arg == mock_val


def test_run_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = cloudbuild.RepoSource(project_id="project_id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ReceiveTriggerWebhookRequest,
        dict,
    ],
)
def test_receive_trigger_webhook(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ReceiveTriggerWebhookResponse()
        response = client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ReceiveTriggerWebhookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


def test_receive_trigger_webhook_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.receive_trigger_webhook()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()


def test_receive_trigger_webhook_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.ReceiveTriggerWebhookRequest(
        name="name_value",
        project_id="project_id_value",
        trigger="trigger_value",
        secret="secret_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.receive_trigger_webhook(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest(
            name="name_value",
            project_id="project_id_value",
            trigger="trigger_value",
            secret="secret_value",
        )


def test_receive_trigger_webhook_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.receive_trigger_webhook
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.receive_trigger_webhook
        ] = mock_rpc
        request = {}
        client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.receive_trigger_webhook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_receive_trigger_webhook_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )
        response = await client.receive_trigger_webhook()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.receive_trigger_webhook
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.receive_trigger_webhook
        ] = mock_object

        request = {}
        await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.receive_trigger_webhook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async(
    transport: str = "grpc_asyncio",
    request_type=cloudbuild.ReceiveTriggerWebhookRequest,
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )
        response = await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ReceiveTriggerWebhookRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async_from_dict():
    await test_receive_trigger_webhook_async(request_type=dict)


def test_receive_trigger_webhook_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ReceiveTriggerWebhookRequest()

    request.project_id = "project_id_value"
    request.trigger = "trigger_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value = cloudbuild.ReceiveTriggerWebhookResponse()
        client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger=trigger_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_receive_trigger_webhook_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ReceiveTriggerWebhookRequest()

    request.project_id = "project_id_value"
    request.trigger = "trigger_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )
        await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger=trigger_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateWorkerPoolRequest,
        dict,
    ],
)
def test_create_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest()


def test_create_worker_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.CreateWorkerPoolRequest(
        parent="parent_value",
        worker_pool_id="worker_pool_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_worker_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest(
            parent="parent_value",
            worker_pool_id="worker_pool_id_value",
        )


def test_create_worker_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_worker_pool
        ] = mock_rpc
        request = {}
        client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_worker_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_create_worker_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_worker_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_worker_pool
        ] = mock_object

        request = {}
        await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.CreateWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_worker_pool_async_from_dict():
    await test_create_worker_pool_async(request_type=dict)


def test_create_worker_pool_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateWorkerPoolRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_create_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_worker_pool(
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].worker_pool_id
        mock_val = "worker_pool_id_value"
        assert arg == mock_val


def test_create_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_worker_pool(
            cloudbuild.CreateWorkerPoolRequest(),
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_worker_pool(
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].worker_pool_id
        mock_val = "worker_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_worker_pool(
            cloudbuild.CreateWorkerPoolRequest(),
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetWorkerPoolRequest,
        dict,
    ],
)
def test_get_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            state=cloudbuild.WorkerPool.State.CREATING,
            etag="etag_value",
        )
        response = client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.state == cloudbuild.WorkerPool.State.CREATING
    assert response.etag == "etag_value"


def test_get_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest()


def test_get_worker_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.GetWorkerPoolRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_worker_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest(
            name="name_value",
        )


def test_get_worker_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_worker_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_worker_pool] = mock_rpc
        request = {}
        client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_worker_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                state=cloudbuild.WorkerPool.State.CREATING,
                etag="etag_value",
            )
        )
        response = await client.get_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest()


@pytest.mark.asyncio
async def test_get_worker_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_worker_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_worker_pool
        ] = mock_object

        request = {}
        await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                state=cloudbuild.WorkerPool.State.CREATING,
                etag="etag_value",
            )
        )
        response = await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.GetWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.state == cloudbuild.WorkerPool.State.CREATING
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_worker_pool_async_from_dict():
    await test_get_worker_pool_async(request_type=dict)


def test_get_worker_pool_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetWorkerPoolRequest(
        **{"name": "projects/sample1/locations/sample2/workerPools/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        call.return_value = cloudbuild.WorkerPool()
        client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_get_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_worker_pool(
            cloudbuild.GetWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_worker_pool(
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
async def test_get_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_worker_pool(
            cloudbuild.GetWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteWorkerPoolRequest,
        dict,
    ],
)
def test_delete_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.DeleteWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()


def test_delete_worker_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.DeleteWorkerPoolRequest(
        name="name_value",
        etag="etag_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_worker_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest(
            name="name_value",
            etag="etag_value",
        )


def test_delete_worker_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_worker_pool
        ] = mock_rpc
        request = {}
        client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_worker_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()


@pytest.mark.asyncio
async def test_delete_worker_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_worker_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_worker_pool
        ] = mock_object

        request = {}
        await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.DeleteWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_worker_pool_async_from_dict():
    await test_delete_worker_pool_async(request_type=dict)


def test_delete_worker_pool_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteWorkerPoolRequest(
        **{"name": "projects/sample1/locations/sample2/workerPools/sample3"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_delete_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_worker_pool(
            cloudbuild.DeleteWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_worker_pool(
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
async def test_delete_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_worker_pool(
            cloudbuild.DeleteWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateWorkerPoolRequest,
        dict,
    ],
)
def test_update_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.UpdateWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()


def test_update_worker_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.UpdateWorkerPoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_worker_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()


def test_update_worker_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_worker_pool
        ] = mock_rpc
        request = {}
        client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_worker_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_update_worker_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_worker_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_worker_pool
        ] = mock_object

        request = {}
        await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.UpdateWorkerPoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_worker_pool_async_from_dict():
    await test_update_worker_pool_async(request_type=dict)


def test_update_worker_pool_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateWorkerPoolRequest(
        **{
            "worker_pool": {
                "name": "projects/sample1/locations/sample2/workerPools/sample3"
            }
        }
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_update_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_worker_pool(
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_worker_pool(
            cloudbuild.UpdateWorkerPoolRequest(),
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_worker_pool(
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_worker_pool(
            cloudbuild.UpdateWorkerPoolRequest(),
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListWorkerPoolsRequest,
        dict,
    ],
)
def test_list_worker_pools(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListWorkerPoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkerPoolsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_worker_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_worker_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest()


def test_list_worker_pools_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = cloudbuild.ListWorkerPoolsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_worker_pools(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_worker_pools_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_worker_pools in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_worker_pools
        ] = mock_rpc
        request = {}
        client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_worker_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_worker_pools_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_worker_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest()


@pytest.mark.asyncio
async def test_list_worker_pools_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = CloudBuildAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_worker_pools
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_worker_pools
        ] = mock_object

        request = {}
        await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_worker_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_worker_pools_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListWorkerPoolsRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = cloudbuild.ListWorkerPoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkerPoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_worker_pools_async_from_dict():
    await test_list_worker_pools_async(request_type=dict)


def test_list_worker_pools_routing_parameters():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListWorkerPoolsRequest(
        **{"parent": "projects/sample1/locations/sample2"}
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        call.return_value = cloudbuild.ListWorkerPoolsResponse()
        client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    _, _, kw = call.mock_calls[0]
    # This test doesn't assert anything useful.
    assert kw["metadata"]


def test_list_worker_pools_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_worker_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_worker_pools_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_worker_pools(
            cloudbuild.ListWorkerPoolsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_worker_pools_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_worker_pools(
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
async def test_list_worker_pools_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_worker_pools(
            cloudbuild.ListWorkerPoolsRequest(),
            parent="parent_value",
        )


def test_list_worker_pools_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_worker_pools(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.WorkerPool) for i in results)


def test_list_worker_pools_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_worker_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_worker_pools_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_worker_pools(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.WorkerPool) for i in responses)


@pytest.mark.asyncio
async def test_list_worker_pools_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_worker_pools(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildRequest,
        dict,
    ],
)
def test_create_build_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request_init["build"] = {
        "name": "name_value",
        "id": "id_value",
        "project_id": "project_id_value",
        "status": 10,
        "status_detail": "status_detail_value",
        "source": {
            "storage_source": {
                "bucket": "bucket_value",
                "object_": "object__value",
                "generation": 1068,
                "source_fetcher": 1,
            },
            "repo_source": {
                "project_id": "project_id_value",
                "repo_name": "repo_name_value",
                "branch_name": "branch_name_value",
                "tag_name": "tag_name_value",
                "commit_sha": "commit_sha_value",
                "dir_": "dir__value",
                "invert_regex": True,
                "substitutions": {},
            },
            "git_source": {
                "url": "url_value",
                "dir_": "dir__value",
                "revision": "revision_value",
            },
            "storage_source_manifest": {
                "bucket": "bucket_value",
                "object_": "object__value",
                "generation": 1068,
            },
        },
        "steps": [
            {
                "name": "name_value",
                "env": ["env_value1", "env_value2"],
                "args": ["args_value1", "args_value2"],
                "dir_": "dir__value",
                "id": "id_value",
                "wait_for": ["wait_for_value1", "wait_for_value2"],
                "entrypoint": "entrypoint_value",
                "secret_env": ["secret_env_value1", "secret_env_value2"],
                "volumes": [{"name": "name_value", "path": "path_value"}],
                "timing": {
                    "start_time": {"seconds": 751, "nanos": 543},
                    "end_time": {},
                },
                "pull_timing": {},
                "timeout": {"seconds": 751, "nanos": 543},
                "status": 10,
                "allow_failure": True,
                "exit_code": 948,
                "allow_exit_codes": [1702, 1703],
                "script": "script_value",
                "automap_substitutions": True,
            }
        ],
        "results": {
            "images": [
                {"name": "name_value", "digest": "digest_value", "push_timing": {}}
            ],
            "build_step_images": [
                "build_step_images_value1",
                "build_step_images_value2",
            ],
            "artifact_manifest": "artifact_manifest_value",
            "num_artifacts": 1392,
            "build_step_outputs": [
                b"build_step_outputs_blob1",
                b"build_step_outputs_blob2",
            ],
            "artifact_timing": {},
            "python_packages": [
                {
                    "uri": "uri_value",
                    "file_hashes": {
                        "file_hash": [{"type_": 1, "value": b"value_blob"}]
                    },
                    "push_timing": {},
                }
            ],
            "maven_artifacts": [
                {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
            ],
            "npm_packages": [
                {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
            ],
        },
        "create_time": {},
        "start_time": {},
        "finish_time": {},
        "timeout": {},
        "images": ["images_value1", "images_value2"],
        "queue_ttl": {},
        "artifacts": {
            "images": ["images_value1", "images_value2"],
            "objects": {
                "location": "location_value",
                "paths": ["paths_value1", "paths_value2"],
                "timing": {},
            },
            "maven_artifacts": [
                {
                    "repository": "repository_value",
                    "path": "path_value",
                    "artifact_id": "artifact_id_value",
                    "group_id": "group_id_value",
                    "version": "version_value",
                }
            ],
            "python_packages": [
                {
                    "repository": "repository_value",
                    "paths": ["paths_value1", "paths_value2"],
                }
            ],
            "npm_packages": [
                {"repository": "repository_value", "package_path": "package_path_value"}
            ],
        },
        "logs_bucket": "logs_bucket_value",
        "source_provenance": {
            "resolved_storage_source": {},
            "resolved_repo_source": {},
            "resolved_storage_source_manifest": {},
            "file_hashes": {},
        },
        "build_trigger_id": "build_trigger_id_value",
        "options": {
            "source_provenance_hash": [1],
            "requested_verify_option": 1,
            "machine_type": 1,
            "disk_size_gb": 1261,
            "substitution_option": 1,
            "dynamic_substitutions": True,
            "automap_substitutions": True,
            "log_streaming_option": 1,
            "worker_pool": "worker_pool_value",
            "pool": {"name": "name_value"},
            "logging": 1,
            "env": ["env_value1", "env_value2"],
            "secret_env": ["secret_env_value1", "secret_env_value2"],
            "volumes": {},
            "default_logs_bucket_behavior": 1,
        },
        "log_url": "log_url_value",
        "substitutions": {},
        "tags": ["tags_value1", "tags_value2"],
        "secrets": [{"kms_key_name": "kms_key_name_value", "secret_env": {}}],
        "timing": {},
        "approval": {
            "state": 1,
            "config": {"approval_required": True},
            "result": {
                "approver_account": "approver_account_value",
                "approval_time": {},
                "decision": 1,
                "comment": "comment_value",
                "url": "url_value",
            },
        },
        "service_account": "service_account_value",
        "available_secrets": {
            "secret_manager": [
                {"version_name": "version_name_value", "env": "env_value"}
            ],
            "inline": [{"kms_key_name": "kms_key_name_value", "env_map": {}}],
        },
        "warnings": [{"text": "text_value", "priority": 1}],
        "failure_info": {"type_": 1, "detail": "detail_value"},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.CreateBuildRequest.meta.fields["build"]

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
    for field, value in request_init["build"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["build"][field])):
                    del request_init["build"][field][i][subfield]
            else:
                del request_init["build"][field][subfield]
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
        response = client.create_build(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_build_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_build] = mock_rpc

        request = {}
        client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_build_rest_required_fields(request_type=cloudbuild.CreateBuildRequest):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_build._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("parent",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = CloudBuildClient(
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

            response = client.create_build(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_build_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_build._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("parent",))
        & set(
            (
                "projectId",
                "build",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_build_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_create_build"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_create_build"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.CreateBuildRequest.pb(cloudbuild.CreateBuildRequest())
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

        request = cloudbuild.CreateBuildRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_build(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_build_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.CreateBuildRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
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
        client.create_build(request)


def test_create_build_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_build(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/builds" % client.transport._host, args[1]
        )


def test_create_build_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


def test_create_build_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildRequest,
        dict,
    ],
)
def test_get_build_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.Build.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_build(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_get_build_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_build] = mock_rpc

        request = {}
        client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_build_rest_required_fields(request_type=cloudbuild.GetBuildRequest):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["id"] = "id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_build._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "id" in jsonified_request
    assert jsonified_request["id"] == "id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.Build()
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
            return_value = cloudbuild.Build.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_build(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_build_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_build._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("name",))
        & set(
            (
                "projectId",
                "id",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_build_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_get_build"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_get_build"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.GetBuildRequest.pb(cloudbuild.GetBuildRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloudbuild.Build.to_json(cloudbuild.Build())

        request = cloudbuild.GetBuildRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.Build()

        client.get_build(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_build_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.GetBuildRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
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
        client.get_build(request)


def test_get_build_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.Build()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            id="id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.Build.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_build(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/builds/{id}" % client.transport._host, args[1]
        )


def test_get_build_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build(
            cloudbuild.GetBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_get_build_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildsRequest,
        dict,
    ],
)
def test_list_builds_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListBuildsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ListBuildsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_builds(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_builds_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_builds in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_builds] = mock_rpc

        request = {}
        client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_builds(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_builds_rest_required_fields(request_type=cloudbuild.ListBuildsRequest):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_builds._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_builds._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
            "parent",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.ListBuildsResponse()
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
            return_value = cloudbuild.ListBuildsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_builds(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_builds_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_builds._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
                "parent",
            )
        )
        & set(("projectId",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_builds_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_list_builds"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_list_builds"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.ListBuildsRequest.pb(cloudbuild.ListBuildsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloudbuild.ListBuildsResponse.to_json(
            cloudbuild.ListBuildsResponse()
        )

        request = cloudbuild.ListBuildsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.ListBuildsResponse()

        client.list_builds(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_builds_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.ListBuildsRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
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
        client.list_builds(request)


def test_list_builds_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListBuildsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            filter="filter_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ListBuildsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_builds(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/builds" % client.transport._host, args[1]
        )


def test_list_builds_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


def test_list_builds_rest_pager(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(cloudbuild.ListBuildsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project_id": "sample1"}

        pager = client.list_builds(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in results)

        pages = list(client.list_builds(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CancelBuildRequest,
        dict,
    ],
)
def test_cancel_build_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.Build.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.cancel_build(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_cancel_build_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.cancel_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.cancel_build] = mock_rpc

        request = {}
        client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.cancel_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_cancel_build_rest_required_fields(request_type=cloudbuild.CancelBuildRequest):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).cancel_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["id"] = "id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).cancel_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "id" in jsonified_request
    assert jsonified_request["id"] == "id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.Build()
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
            return_value = cloudbuild.Build.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.cancel_build(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_cancel_build_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.cancel_build._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "projectId",
                "id",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_cancel_build_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_cancel_build"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_cancel_build"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.CancelBuildRequest.pb(cloudbuild.CancelBuildRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloudbuild.Build.to_json(cloudbuild.Build())

        request = cloudbuild.CancelBuildRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.Build()

        client.cancel_build(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_cancel_build_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.CancelBuildRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
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
        client.cancel_build(request)


def test_cancel_build_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.Build()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            id="id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.Build.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.cancel_build(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/builds/{id}:cancel" % client.transport._host,
            args[1],
        )


def test_cancel_build_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_cancel_build_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RetryBuildRequest,
        dict,
    ],
)
def test_retry_build_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
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
        response = client.retry_build(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_retry_build_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.retry_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.retry_build] = mock_rpc

        request = {}
        client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.retry_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_retry_build_rest_required_fields(request_type=cloudbuild.RetryBuildRequest):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retry_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["id"] = "id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).retry_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "id" in jsonified_request
    assert jsonified_request["id"] == "id_value"

    client = CloudBuildClient(
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

            response = client.retry_build(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_retry_build_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.retry_build._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "projectId",
                "id",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_retry_build_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_retry_build"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_retry_build"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.RetryBuildRequest.pb(cloudbuild.RetryBuildRequest())
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

        request = cloudbuild.RetryBuildRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.retry_build(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_retry_build_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.RetryBuildRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "id": "sample2"}
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
        client.retry_build(request)


def test_retry_build_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            id="id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.retry_build(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/builds/{id}:retry" % client.transport._host,
            args[1],
        )


def test_retry_build_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_retry_build_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ApproveBuildRequest,
        dict,
    ],
)
def test_approve_build_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/builds/sample2"}
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
        response = client.approve_build(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_approve_build_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.approve_build in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.approve_build] = mock_rpc

        request = {}
        client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.approve_build(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_approve_build_rest_required_fields(
    request_type=cloudbuild.ApproveBuildRequest,
):
    transport_class = transports.CloudBuildRestTransport

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
    ).approve_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).approve_build._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudBuildClient(
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

            response = client.approve_build(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_approve_build_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.approve_build._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_approve_build_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_approve_build"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_approve_build"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.ApproveBuildRequest.pb(cloudbuild.ApproveBuildRequest())
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

        request = cloudbuild.ApproveBuildRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.approve_build(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_approve_build_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.ApproveBuildRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/builds/sample2"}
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
        client.approve_build(request)


def test_approve_build_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/builds/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.approve_build(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/builds/*}:approve" % client.transport._host, args[1]
        )


def test_approve_build_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_build(
            cloudbuild.ApproveBuildRequest(),
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )


def test_approve_build_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildTriggerRequest,
        dict,
    ],
)
def test_create_build_trigger_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request_init["trigger"] = {
        "resource_name": "resource_name_value",
        "id": "id_value",
        "description": "description_value",
        "name": "name_value",
        "tags": ["tags_value1", "tags_value2"],
        "trigger_template": {
            "project_id": "project_id_value",
            "repo_name": "repo_name_value",
            "branch_name": "branch_name_value",
            "tag_name": "tag_name_value",
            "commit_sha": "commit_sha_value",
            "dir_": "dir__value",
            "invert_regex": True,
            "substitutions": {},
        },
        "github": {
            "installation_id": 1598,
            "owner": "owner_value",
            "name": "name_value",
            "pull_request": {
                "branch": "branch_value",
                "comment_control": 1,
                "invert_regex": True,
            },
            "push": {
                "branch": "branch_value",
                "tag": "tag_value",
                "invert_regex": True,
            },
        },
        "pubsub_config": {
            "subscription": "subscription_value",
            "topic": "topic_value",
            "service_account_email": "service_account_email_value",
            "state": 1,
        },
        "webhook_config": {"secret": "secret_value", "state": 1},
        "autodetect": True,
        "build": {
            "name": "name_value",
            "id": "id_value",
            "project_id": "project_id_value",
            "status": 10,
            "status_detail": "status_detail_value",
            "source": {
                "storage_source": {
                    "bucket": "bucket_value",
                    "object_": "object__value",
                    "generation": 1068,
                    "source_fetcher": 1,
                },
                "repo_source": {},
                "git_source": {
                    "url": "url_value",
                    "dir_": "dir__value",
                    "revision": "revision_value",
                },
                "storage_source_manifest": {
                    "bucket": "bucket_value",
                    "object_": "object__value",
                    "generation": 1068,
                },
            },
            "steps": [
                {
                    "name": "name_value",
                    "env": ["env_value1", "env_value2"],
                    "args": ["args_value1", "args_value2"],
                    "dir_": "dir__value",
                    "id": "id_value",
                    "wait_for": ["wait_for_value1", "wait_for_value2"],
                    "entrypoint": "entrypoint_value",
                    "secret_env": ["secret_env_value1", "secret_env_value2"],
                    "volumes": [{"name": "name_value", "path": "path_value"}],
                    "timing": {
                        "start_time": {"seconds": 751, "nanos": 543},
                        "end_time": {},
                    },
                    "pull_timing": {},
                    "timeout": {"seconds": 751, "nanos": 543},
                    "status": 10,
                    "allow_failure": True,
                    "exit_code": 948,
                    "allow_exit_codes": [1702, 1703],
                    "script": "script_value",
                    "automap_substitutions": True,
                }
            ],
            "results": {
                "images": [
                    {"name": "name_value", "digest": "digest_value", "push_timing": {}}
                ],
                "build_step_images": [
                    "build_step_images_value1",
                    "build_step_images_value2",
                ],
                "artifact_manifest": "artifact_manifest_value",
                "num_artifacts": 1392,
                "build_step_outputs": [
                    b"build_step_outputs_blob1",
                    b"build_step_outputs_blob2",
                ],
                "artifact_timing": {},
                "python_packages": [
                    {
                        "uri": "uri_value",
                        "file_hashes": {
                            "file_hash": [{"type_": 1, "value": b"value_blob"}]
                        },
                        "push_timing": {},
                    }
                ],
                "maven_artifacts": [
                    {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
                ],
                "npm_packages": [
                    {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
                ],
            },
            "create_time": {},
            "start_time": {},
            "finish_time": {},
            "timeout": {},
            "images": ["images_value1", "images_value2"],
            "queue_ttl": {},
            "artifacts": {
                "images": ["images_value1", "images_value2"],
                "objects": {
                    "location": "location_value",
                    "paths": ["paths_value1", "paths_value2"],
                    "timing": {},
                },
                "maven_artifacts": [
                    {
                        "repository": "repository_value",
                        "path": "path_value",
                        "artifact_id": "artifact_id_value",
                        "group_id": "group_id_value",
                        "version": "version_value",
                    }
                ],
                "python_packages": [
                    {
                        "repository": "repository_value",
                        "paths": ["paths_value1", "paths_value2"],
                    }
                ],
                "npm_packages": [
                    {
                        "repository": "repository_value",
                        "package_path": "package_path_value",
                    }
                ],
            },
            "logs_bucket": "logs_bucket_value",
            "source_provenance": {
                "resolved_storage_source": {},
                "resolved_repo_source": {},
                "resolved_storage_source_manifest": {},
                "file_hashes": {},
            },
            "build_trigger_id": "build_trigger_id_value",
            "options": {
                "source_provenance_hash": [1],
                "requested_verify_option": 1,
                "machine_type": 1,
                "disk_size_gb": 1261,
                "substitution_option": 1,
                "dynamic_substitutions": True,
                "automap_substitutions": True,
                "log_streaming_option": 1,
                "worker_pool": "worker_pool_value",
                "pool": {"name": "name_value"},
                "logging": 1,
                "env": ["env_value1", "env_value2"],
                "secret_env": ["secret_env_value1", "secret_env_value2"],
                "volumes": {},
                "default_logs_bucket_behavior": 1,
            },
            "log_url": "log_url_value",
            "substitutions": {},
            "tags": ["tags_value1", "tags_value2"],
            "secrets": [{"kms_key_name": "kms_key_name_value", "secret_env": {}}],
            "timing": {},
            "approval": {
                "state": 1,
                "config": {"approval_required": True},
                "result": {
                    "approver_account": "approver_account_value",
                    "approval_time": {},
                    "decision": 1,
                    "comment": "comment_value",
                    "url": "url_value",
                },
            },
            "service_account": "service_account_value",
            "available_secrets": {
                "secret_manager": [
                    {"version_name": "version_name_value", "env": "env_value"}
                ],
                "inline": [{"kms_key_name": "kms_key_name_value", "env_map": {}}],
            },
            "warnings": [{"text": "text_value", "priority": 1}],
            "failure_info": {"type_": 1, "detail": "detail_value"},
        },
        "filename": "filename_value",
        "git_file_source": {
            "path": "path_value",
            "uri": "uri_value",
            "repository": "repository_value",
            "repo_type": 1,
            "revision": "revision_value",
            "github_enterprise_config": "github_enterprise_config_value",
        },
        "create_time": {},
        "disabled": True,
        "substitutions": {},
        "ignored_files": ["ignored_files_value1", "ignored_files_value2"],
        "included_files": ["included_files_value1", "included_files_value2"],
        "filter": "filter_value",
        "source_to_build": {
            "uri": "uri_value",
            "repository": "repository_value",
            "ref": "ref_value",
            "repo_type": 1,
            "github_enterprise_config": "github_enterprise_config_value",
        },
        "service_account": "service_account_value",
        "repository_event_config": {
            "repository": "repository_value",
            "repository_type": 1,
            "pull_request": {},
            "push": {},
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.CreateBuildTriggerRequest.meta.fields["trigger"]

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
    for field, value in request_init["trigger"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["trigger"][field])):
                    del request_init["trigger"][field][i][subfield]
            else:
                del request_init["trigger"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_build_trigger(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_create_build_trigger_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_build_trigger
        ] = mock_rpc

        request = {}
        client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_build_trigger_rest_required_fields(
    request_type=cloudbuild.CreateBuildTriggerRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_build_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_build_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("parent",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.BuildTrigger()
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
            return_value = cloudbuild.BuildTrigger.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_build_trigger(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_build_trigger_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_build_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("parent",))
        & set(
            (
                "projectId",
                "trigger",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_build_trigger_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_create_build_trigger"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_create_build_trigger"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.CreateBuildTriggerRequest.pb(
            cloudbuild.CreateBuildTriggerRequest()
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
        req.return_value._content = cloudbuild.BuildTrigger.to_json(
            cloudbuild.BuildTrigger()
        )

        request = cloudbuild.CreateBuildTriggerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.BuildTrigger()

        client.create_build_trigger(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_build_trigger_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.CreateBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
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
        client.create_build_trigger(request)


def test_create_build_trigger_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_build_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers" % client.transport._host, args[1]
        )


def test_create_build_trigger_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


def test_create_build_trigger_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildTriggerRequest,
        dict,
    ],
)
def test_get_build_trigger_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_build_trigger(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_get_build_trigger_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_build_trigger in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_build_trigger
        ] = mock_rpc

        request = {}
        client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_build_trigger_rest_required_fields(
    request_type=cloudbuild.GetBuildTriggerRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["trigger_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_build_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["triggerId"] = "trigger_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_build_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == "trigger_id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.BuildTrigger()
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
            return_value = cloudbuild.BuildTrigger.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_build_trigger(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_build_trigger_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_build_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("name",))
        & set(
            (
                "projectId",
                "triggerId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_build_trigger_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_get_build_trigger"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_get_build_trigger"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.GetBuildTriggerRequest.pb(
            cloudbuild.GetBuildTriggerRequest()
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
        req.return_value._content = cloudbuild.BuildTrigger.to_json(
            cloudbuild.BuildTrigger()
        )

        request = cloudbuild.GetBuildTriggerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.BuildTrigger()

        client.get_build_trigger(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_build_trigger_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.GetBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
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
        client.get_build_trigger(request)


def test_get_build_trigger_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "trigger_id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_build_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers/{trigger_id}"
            % client.transport._host,
            args[1],
        )


def test_get_build_trigger_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_get_build_trigger_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildTriggersRequest,
        dict,
    ],
)
def test_list_build_triggers_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListBuildTriggersResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ListBuildTriggersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_build_triggers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_build_triggers_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_build_triggers in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_build_triggers
        ] = mock_rpc

        request = {}
        client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_build_triggers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_build_triggers_rest_required_fields(
    request_type=cloudbuild.ListBuildTriggersRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_build_triggers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_build_triggers._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "parent",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.ListBuildTriggersResponse()
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
            return_value = cloudbuild.ListBuildTriggersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_build_triggers(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_build_triggers_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_build_triggers._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "parent",
            )
        )
        & set(("projectId",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_build_triggers_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_list_build_triggers"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_list_build_triggers"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.ListBuildTriggersRequest.pb(
            cloudbuild.ListBuildTriggersRequest()
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
        req.return_value._content = cloudbuild.ListBuildTriggersResponse.to_json(
            cloudbuild.ListBuildTriggersResponse()
        )

        request = cloudbuild.ListBuildTriggersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.ListBuildTriggersResponse()

        client.list_build_triggers(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_build_triggers_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.ListBuildTriggersRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1"}
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
        client.list_build_triggers(request)


def test_list_build_triggers_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListBuildTriggersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ListBuildTriggersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_build_triggers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers" % client.transport._host, args[1]
        )


def test_list_build_triggers_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(),
            project_id="project_id_value",
        )


def test_list_build_triggers_rest_pager(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloudbuild.ListBuildTriggersResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project_id": "sample1"}

        pager = client.list_build_triggers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in results)

        pages = list(client.list_build_triggers(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteBuildTriggerRequest,
        dict,
    ],
)
def test_delete_build_trigger_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
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
        response = client.delete_build_trigger(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_build_trigger_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_build_trigger
        ] = mock_rpc

        request = {}
        client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_build_trigger_rest_required_fields(
    request_type=cloudbuild.DeleteBuildTriggerRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["trigger_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_build_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["triggerId"] = "trigger_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_build_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == "trigger_id_value"

    client = CloudBuildClient(
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

            response = client.delete_build_trigger(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_build_trigger_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_build_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("name",))
        & set(
            (
                "projectId",
                "triggerId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_build_trigger_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_delete_build_trigger"
    ) as pre:
        pre.assert_not_called()
        pb_message = cloudbuild.DeleteBuildTriggerRequest.pb(
            cloudbuild.DeleteBuildTriggerRequest()
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

        request = cloudbuild.DeleteBuildTriggerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_build_trigger(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_build_trigger_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.DeleteBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
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
        client.delete_build_trigger(request)


def test_delete_build_trigger_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "trigger_id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_build_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers/{trigger_id}"
            % client.transport._host,
            args[1],
        )


def test_delete_build_trigger_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_delete_build_trigger_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateBuildTriggerRequest,
        dict,
    ],
)
def test_update_build_trigger_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
    request_init["trigger"] = {
        "resource_name": "resource_name_value",
        "id": "id_value",
        "description": "description_value",
        "name": "name_value",
        "tags": ["tags_value1", "tags_value2"],
        "trigger_template": {
            "project_id": "project_id_value",
            "repo_name": "repo_name_value",
            "branch_name": "branch_name_value",
            "tag_name": "tag_name_value",
            "commit_sha": "commit_sha_value",
            "dir_": "dir__value",
            "invert_regex": True,
            "substitutions": {},
        },
        "github": {
            "installation_id": 1598,
            "owner": "owner_value",
            "name": "name_value",
            "pull_request": {
                "branch": "branch_value",
                "comment_control": 1,
                "invert_regex": True,
            },
            "push": {
                "branch": "branch_value",
                "tag": "tag_value",
                "invert_regex": True,
            },
        },
        "pubsub_config": {
            "subscription": "subscription_value",
            "topic": "topic_value",
            "service_account_email": "service_account_email_value",
            "state": 1,
        },
        "webhook_config": {"secret": "secret_value", "state": 1},
        "autodetect": True,
        "build": {
            "name": "name_value",
            "id": "id_value",
            "project_id": "project_id_value",
            "status": 10,
            "status_detail": "status_detail_value",
            "source": {
                "storage_source": {
                    "bucket": "bucket_value",
                    "object_": "object__value",
                    "generation": 1068,
                    "source_fetcher": 1,
                },
                "repo_source": {},
                "git_source": {
                    "url": "url_value",
                    "dir_": "dir__value",
                    "revision": "revision_value",
                },
                "storage_source_manifest": {
                    "bucket": "bucket_value",
                    "object_": "object__value",
                    "generation": 1068,
                },
            },
            "steps": [
                {
                    "name": "name_value",
                    "env": ["env_value1", "env_value2"],
                    "args": ["args_value1", "args_value2"],
                    "dir_": "dir__value",
                    "id": "id_value",
                    "wait_for": ["wait_for_value1", "wait_for_value2"],
                    "entrypoint": "entrypoint_value",
                    "secret_env": ["secret_env_value1", "secret_env_value2"],
                    "volumes": [{"name": "name_value", "path": "path_value"}],
                    "timing": {
                        "start_time": {"seconds": 751, "nanos": 543},
                        "end_time": {},
                    },
                    "pull_timing": {},
                    "timeout": {"seconds": 751, "nanos": 543},
                    "status": 10,
                    "allow_failure": True,
                    "exit_code": 948,
                    "allow_exit_codes": [1702, 1703],
                    "script": "script_value",
                    "automap_substitutions": True,
                }
            ],
            "results": {
                "images": [
                    {"name": "name_value", "digest": "digest_value", "push_timing": {}}
                ],
                "build_step_images": [
                    "build_step_images_value1",
                    "build_step_images_value2",
                ],
                "artifact_manifest": "artifact_manifest_value",
                "num_artifacts": 1392,
                "build_step_outputs": [
                    b"build_step_outputs_blob1",
                    b"build_step_outputs_blob2",
                ],
                "artifact_timing": {},
                "python_packages": [
                    {
                        "uri": "uri_value",
                        "file_hashes": {
                            "file_hash": [{"type_": 1, "value": b"value_blob"}]
                        },
                        "push_timing": {},
                    }
                ],
                "maven_artifacts": [
                    {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
                ],
                "npm_packages": [
                    {"uri": "uri_value", "file_hashes": {}, "push_timing": {}}
                ],
            },
            "create_time": {},
            "start_time": {},
            "finish_time": {},
            "timeout": {},
            "images": ["images_value1", "images_value2"],
            "queue_ttl": {},
            "artifacts": {
                "images": ["images_value1", "images_value2"],
                "objects": {
                    "location": "location_value",
                    "paths": ["paths_value1", "paths_value2"],
                    "timing": {},
                },
                "maven_artifacts": [
                    {
                        "repository": "repository_value",
                        "path": "path_value",
                        "artifact_id": "artifact_id_value",
                        "group_id": "group_id_value",
                        "version": "version_value",
                    }
                ],
                "python_packages": [
                    {
                        "repository": "repository_value",
                        "paths": ["paths_value1", "paths_value2"],
                    }
                ],
                "npm_packages": [
                    {
                        "repository": "repository_value",
                        "package_path": "package_path_value",
                    }
                ],
            },
            "logs_bucket": "logs_bucket_value",
            "source_provenance": {
                "resolved_storage_source": {},
                "resolved_repo_source": {},
                "resolved_storage_source_manifest": {},
                "file_hashes": {},
            },
            "build_trigger_id": "build_trigger_id_value",
            "options": {
                "source_provenance_hash": [1],
                "requested_verify_option": 1,
                "machine_type": 1,
                "disk_size_gb": 1261,
                "substitution_option": 1,
                "dynamic_substitutions": True,
                "automap_substitutions": True,
                "log_streaming_option": 1,
                "worker_pool": "worker_pool_value",
                "pool": {"name": "name_value"},
                "logging": 1,
                "env": ["env_value1", "env_value2"],
                "secret_env": ["secret_env_value1", "secret_env_value2"],
                "volumes": {},
                "default_logs_bucket_behavior": 1,
            },
            "log_url": "log_url_value",
            "substitutions": {},
            "tags": ["tags_value1", "tags_value2"],
            "secrets": [{"kms_key_name": "kms_key_name_value", "secret_env": {}}],
            "timing": {},
            "approval": {
                "state": 1,
                "config": {"approval_required": True},
                "result": {
                    "approver_account": "approver_account_value",
                    "approval_time": {},
                    "decision": 1,
                    "comment": "comment_value",
                    "url": "url_value",
                },
            },
            "service_account": "service_account_value",
            "available_secrets": {
                "secret_manager": [
                    {"version_name": "version_name_value", "env": "env_value"}
                ],
                "inline": [{"kms_key_name": "kms_key_name_value", "env_map": {}}],
            },
            "warnings": [{"text": "text_value", "priority": 1}],
            "failure_info": {"type_": 1, "detail": "detail_value"},
        },
        "filename": "filename_value",
        "git_file_source": {
            "path": "path_value",
            "uri": "uri_value",
            "repository": "repository_value",
            "repo_type": 1,
            "revision": "revision_value",
            "github_enterprise_config": "github_enterprise_config_value",
        },
        "create_time": {},
        "disabled": True,
        "substitutions": {},
        "ignored_files": ["ignored_files_value1", "ignored_files_value2"],
        "included_files": ["included_files_value1", "included_files_value2"],
        "filter": "filter_value",
        "source_to_build": {
            "uri": "uri_value",
            "repository": "repository_value",
            "ref": "ref_value",
            "repo_type": 1,
            "github_enterprise_config": "github_enterprise_config_value",
        },
        "service_account": "service_account_value",
        "repository_event_config": {
            "repository": "repository_value",
            "repository_type": 1,
            "pull_request": {},
            "push": {},
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.UpdateBuildTriggerRequest.meta.fields["trigger"]

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
    for field, value in request_init["trigger"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["trigger"][field])):
                    del request_init["trigger"][field][i][subfield]
            else:
                del request_init["trigger"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_build_trigger(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_update_build_trigger_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_build_trigger in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_build_trigger
        ] = mock_rpc

        request = {}
        client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_build_trigger_rest_required_fields(
    request_type=cloudbuild.UpdateBuildTriggerRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["trigger_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_build_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["triggerId"] = "trigger_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_build_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == "trigger_id_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.BuildTrigger()
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

            # Convert return value to protobuf type
            return_value = cloudbuild.BuildTrigger.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_build_trigger(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_build_trigger_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_build_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "projectId",
                "triggerId",
                "trigger",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_build_trigger_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_update_build_trigger"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_update_build_trigger"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.UpdateBuildTriggerRequest.pb(
            cloudbuild.UpdateBuildTriggerRequest()
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
        req.return_value._content = cloudbuild.BuildTrigger.to_json(
            cloudbuild.BuildTrigger()
        )

        request = cloudbuild.UpdateBuildTriggerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.BuildTrigger()

        client.update_build_trigger(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_build_trigger_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.UpdateBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
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
        client.update_build_trigger(request)


def test_update_build_trigger_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.BuildTrigger()

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "trigger_id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.BuildTrigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_build_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers/{trigger_id}"
            % client.transport._host,
            args[1],
        )


def test_update_build_trigger_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


def test_update_build_trigger_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RunBuildTriggerRequest,
        dict,
    ],
)
def test_run_build_trigger_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
    request_init["source"] = {
        "project_id": "project_id_value",
        "repo_name": "repo_name_value",
        "branch_name": "branch_name_value",
        "tag_name": "tag_name_value",
        "commit_sha": "commit_sha_value",
        "dir_": "dir__value",
        "invert_regex": True,
        "substitutions": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.RunBuildTriggerRequest.meta.fields["source"]

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
    for field, value in request_init["source"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["source"][field])):
                    del request_init["source"][field][i][subfield]
            else:
                del request_init["source"][field][subfield]
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
        response = client.run_build_trigger(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_run_build_trigger_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.run_build_trigger in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.run_build_trigger
        ] = mock_rpc

        request = {}
        client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.run_build_trigger(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_run_build_trigger_rest_required_fields(
    request_type=cloudbuild.RunBuildTriggerRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["project_id"] = ""
    request_init["trigger_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).run_build_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["projectId"] = "project_id_value"
    jsonified_request["triggerId"] = "trigger_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).run_build_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("name",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "projectId" in jsonified_request
    assert jsonified_request["projectId"] == "project_id_value"
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == "trigger_id_value"

    client = CloudBuildClient(
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

            response = client.run_build_trigger(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_run_build_trigger_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.run_build_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("name",))
        & set(
            (
                "projectId",
                "triggerId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_run_build_trigger_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_run_build_trigger"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_run_build_trigger"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.RunBuildTriggerRequest.pb(
            cloudbuild.RunBuildTriggerRequest()
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

        request = cloudbuild.RunBuildTriggerRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.run_build_trigger(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_run_build_trigger_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.RunBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger_id": "sample2"}
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
        client.run_build_trigger(request)


def test_run_build_trigger_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"project_id": "sample1", "trigger_id": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.run_build_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/projects/{project_id}/triggers/{trigger_id}:run"
            % client.transport._host,
            args[1],
        )


def test_run_build_trigger_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


def test_run_build_trigger_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ReceiveTriggerWebhookRequest,
        dict,
    ],
)
def test_receive_trigger_webhook_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger": "sample2"}
    request_init["body"] = {
        "content_type": "content_type_value",
        "data": b"data_blob",
        "extensions": [
            {
                "type_url": "type.googleapis.com/google.protobuf.Duration",
                "value": b"\x08\x0c\x10\xdb\x07",
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.ReceiveTriggerWebhookRequest.meta.fields["body"]

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
    for field, value in request_init["body"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["body"][field])):
                    del request_init["body"][field][i][subfield]
            else:
                del request_init["body"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ReceiveTriggerWebhookResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ReceiveTriggerWebhookResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.receive_trigger_webhook(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


def test_receive_trigger_webhook_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.receive_trigger_webhook
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.receive_trigger_webhook
        ] = mock_rpc

        request = {}
        client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.receive_trigger_webhook(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_receive_trigger_webhook_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_receive_trigger_webhook"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_receive_trigger_webhook"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.ReceiveTriggerWebhookRequest.pb(
            cloudbuild.ReceiveTriggerWebhookRequest()
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
        req.return_value._content = cloudbuild.ReceiveTriggerWebhookResponse.to_json(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )

        request = cloudbuild.ReceiveTriggerWebhookRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.ReceiveTriggerWebhookResponse()

        client.receive_trigger_webhook(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_receive_trigger_webhook_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.ReceiveTriggerWebhookRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_id": "sample1", "trigger": "sample2"}
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
        client.receive_trigger_webhook(request)


def test_receive_trigger_webhook_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateWorkerPoolRequest,
        dict,
    ],
)
def test_create_worker_pool_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["worker_pool"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "uid": "uid_value",
        "annotations": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "state": 1,
        "private_pool_v1_config": {
            "worker_config": {
                "machine_type": "machine_type_value",
                "disk_size_gb": 1261,
            },
            "network_config": {
                "peered_network": "peered_network_value",
                "egress_option": 1,
                "peered_network_ip_range": "peered_network_ip_range_value",
            },
        },
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.CreateWorkerPoolRequest.meta.fields["worker_pool"]

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
    for field, value in request_init["worker_pool"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["worker_pool"][field])):
                    del request_init["worker_pool"][field][i][subfield]
            else:
                del request_init["worker_pool"][field][subfield]
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
        response = client.create_worker_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_worker_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_worker_pool
        ] = mock_rpc

        request = {}
        client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_worker_pool_rest_required_fields(
    request_type=cloudbuild.CreateWorkerPoolRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["worker_pool_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "workerPoolId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_worker_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "workerPoolId" in jsonified_request
    assert jsonified_request["workerPoolId"] == request_init["worker_pool_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["workerPoolId"] = "worker_pool_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_worker_pool._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "validate_only",
            "worker_pool_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "workerPoolId" in jsonified_request
    assert jsonified_request["workerPoolId"] == "worker_pool_id_value"

    client = CloudBuildClient(
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

            response = client.create_worker_pool(request)

            expected_params = [
                (
                    "workerPoolId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_worker_pool_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_worker_pool._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "validateOnly",
                "workerPoolId",
            )
        )
        & set(
            (
                "parent",
                "workerPool",
                "workerPoolId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_worker_pool_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_create_worker_pool"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_create_worker_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.CreateWorkerPoolRequest.pb(
            cloudbuild.CreateWorkerPoolRequest()
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

        request = cloudbuild.CreateWorkerPoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_worker_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_worker_pool_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.CreateWorkerPoolRequest
):
    client = CloudBuildClient(
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
        client.create_worker_pool(request)


def test_create_worker_pool_rest_flattened():
    client = CloudBuildClient(
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
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_worker_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/workerPools"
            % client.transport._host,
            args[1],
        )


def test_create_worker_pool_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_worker_pool(
            cloudbuild.CreateWorkerPoolRequest(),
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )


def test_create_worker_pool_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetWorkerPoolRequest,
        dict,
    ],
)
def test_get_worker_pool_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/workerPools/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.WorkerPool(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            state=cloudbuild.WorkerPool.State.CREATING,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.WorkerPool.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_worker_pool(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.state == cloudbuild.WorkerPool.State.CREATING
    assert response.etag == "etag_value"


def test_get_worker_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_worker_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_worker_pool] = mock_rpc

        request = {}
        client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_worker_pool_rest_required_fields(
    request_type=cloudbuild.GetWorkerPoolRequest,
):
    transport_class = transports.CloudBuildRestTransport

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
    ).get_worker_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_worker_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.WorkerPool()
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
            return_value = cloudbuild.WorkerPool.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_worker_pool(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_worker_pool_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_worker_pool._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_worker_pool_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_get_worker_pool"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_get_worker_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.GetWorkerPoolRequest.pb(
            cloudbuild.GetWorkerPoolRequest()
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
        req.return_value._content = cloudbuild.WorkerPool.to_json(
            cloudbuild.WorkerPool()
        )

        request = cloudbuild.GetWorkerPoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.WorkerPool()

        client.get_worker_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_worker_pool_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.GetWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/workerPools/sample3"}
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
        client.get_worker_pool(request)


def test_get_worker_pool_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.WorkerPool()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/workerPools/sample3"
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
        return_value = cloudbuild.WorkerPool.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_worker_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/workerPools/*}"
            % client.transport._host,
            args[1],
        )


def test_get_worker_pool_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_worker_pool(
            cloudbuild.GetWorkerPoolRequest(),
            name="name_value",
        )


def test_get_worker_pool_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteWorkerPoolRequest,
        dict,
    ],
)
def test_delete_worker_pool_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/workerPools/sample3"}
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
        response = client.delete_worker_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_worker_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_worker_pool
        ] = mock_rpc

        request = {}
        client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_worker_pool_rest_required_fields(
    request_type=cloudbuild.DeleteWorkerPoolRequest,
):
    transport_class = transports.CloudBuildRestTransport

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
    ).delete_worker_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_worker_pool._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "etag",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudBuildClient(
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

            response = client.delete_worker_pool(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_worker_pool_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_worker_pool._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "etag",
                "validateOnly",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_worker_pool_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_delete_worker_pool"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_delete_worker_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.DeleteWorkerPoolRequest.pb(
            cloudbuild.DeleteWorkerPoolRequest()
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

        request = cloudbuild.DeleteWorkerPoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_worker_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_worker_pool_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.DeleteWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/workerPools/sample3"}
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
        client.delete_worker_pool(request)


def test_delete_worker_pool_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/workerPools/sample3"
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

        client.delete_worker_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/workerPools/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_worker_pool_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_worker_pool(
            cloudbuild.DeleteWorkerPoolRequest(),
            name="name_value",
        )


def test_delete_worker_pool_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateWorkerPoolRequest,
        dict,
    ],
)
def test_update_worker_pool_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "worker_pool": {
            "name": "projects/sample1/locations/sample2/workerPools/sample3"
        }
    }
    request_init["worker_pool"] = {
        "name": "projects/sample1/locations/sample2/workerPools/sample3",
        "display_name": "display_name_value",
        "uid": "uid_value",
        "annotations": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "state": 1,
        "private_pool_v1_config": {
            "worker_config": {
                "machine_type": "machine_type_value",
                "disk_size_gb": 1261,
            },
            "network_config": {
                "peered_network": "peered_network_value",
                "egress_option": 1,
                "peered_network_ip_range": "peered_network_ip_range_value",
            },
        },
        "etag": "etag_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudbuild.UpdateWorkerPoolRequest.meta.fields["worker_pool"]

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
    for field, value in request_init["worker_pool"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["worker_pool"][field])):
                    del request_init["worker_pool"][field][i][subfield]
            else:
                del request_init["worker_pool"][field][subfield]
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
        response = client.update_worker_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_worker_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_worker_pool in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_worker_pool
        ] = mock_rpc

        request = {}
        client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_worker_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_worker_pool_rest_required_fields(
    request_type=cloudbuild.UpdateWorkerPoolRequest,
):
    transport_class = transports.CloudBuildRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_worker_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_worker_pool._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CloudBuildClient(
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

            response = client.update_worker_pool(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_worker_pool_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_worker_pool._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "updateMask",
                "validateOnly",
            )
        )
        & set(("workerPool",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_worker_pool_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_update_worker_pool"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_update_worker_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.UpdateWorkerPoolRequest.pb(
            cloudbuild.UpdateWorkerPoolRequest()
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

        request = cloudbuild.UpdateWorkerPoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_worker_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_worker_pool_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.UpdateWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "worker_pool": {
            "name": "projects/sample1/locations/sample2/workerPools/sample3"
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
        client.update_worker_pool(request)


def test_update_worker_pool_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "worker_pool": {
                "name": "projects/sample1/locations/sample2/workerPools/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_worker_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{worker_pool.name=projects/*/locations/*/workerPools/*}"
            % client.transport._host,
            args[1],
        )


def test_update_worker_pool_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_worker_pool(
            cloudbuild.UpdateWorkerPoolRequest(),
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_worker_pool_rest_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListWorkerPoolsRequest,
        dict,
    ],
)
def test_list_worker_pools_rest(request_type):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListWorkerPoolsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudbuild.ListWorkerPoolsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_worker_pools(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkerPoolsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_worker_pools_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_worker_pools in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_worker_pools
        ] = mock_rpc

        request = {}
        client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_worker_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_worker_pools_rest_required_fields(
    request_type=cloudbuild.ListWorkerPoolsRequest,
):
    transport_class = transports.CloudBuildRestTransport

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
    ).list_worker_pools._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_worker_pools._get_unset_required_fields(jsonified_request)
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

    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudbuild.ListWorkerPoolsResponse()
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
            return_value = cloudbuild.ListWorkerPoolsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_worker_pools(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_worker_pools_rest_unset_required_fields():
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_worker_pools._get_unset_required_fields({})
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
def test_list_worker_pools_rest_interceptors(null_interceptor):
    transport = transports.CloudBuildRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudBuildRestInterceptor(),
    )
    client = CloudBuildClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudBuildRestInterceptor, "post_list_worker_pools"
    ) as post, mock.patch.object(
        transports.CloudBuildRestInterceptor, "pre_list_worker_pools"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudbuild.ListWorkerPoolsRequest.pb(
            cloudbuild.ListWorkerPoolsRequest()
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
        req.return_value._content = cloudbuild.ListWorkerPoolsResponse.to_json(
            cloudbuild.ListWorkerPoolsResponse()
        )

        request = cloudbuild.ListWorkerPoolsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudbuild.ListWorkerPoolsResponse()

        client.list_worker_pools(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_worker_pools_rest_bad_request(
    transport: str = "rest", request_type=cloudbuild.ListWorkerPoolsRequest
):
    client = CloudBuildClient(
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
        client.list_worker_pools(request)


def test_list_worker_pools_rest_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudbuild.ListWorkerPoolsResponse()

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
        return_value = cloudbuild.ListWorkerPoolsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_worker_pools(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/workerPools"
            % client.transport._host,
            args[1],
        )


def test_list_worker_pools_rest_flattened_error(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_worker_pools(
            cloudbuild.ListWorkerPoolsRequest(),
            parent="parent_value",
        )


def test_list_worker_pools_rest_pager(transport: str = "rest"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloudbuild.ListWorkerPoolsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_worker_pools(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.WorkerPool) for i in results)

        pages = list(client.list_worker_pools(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudBuildClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudBuildGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
        transports.CloudBuildRestTransport,
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
    transport = CloudBuildClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudBuildGrpcTransport,
    )


def test_cloud_build_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudBuildTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_build_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudBuildTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_build",
        "get_build",
        "list_builds",
        "cancel_build",
        "retry_build",
        "approve_build",
        "create_build_trigger",
        "get_build_trigger",
        "list_build_triggers",
        "delete_build_trigger",
        "update_build_trigger",
        "run_build_trigger",
        "receive_trigger_webhook",
        "create_worker_pool",
        "get_worker_pool",
        "delete_worker_pool",
        "update_worker_pool",
        "list_worker_pools",
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


def test_cloud_build_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_build_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport()
        adc.assert_called_once()


def test_cloud_build_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudBuildClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
    ],
)
def test_cloud_build_transport_auth_adc(transport_class):
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
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
        transports.CloudBuildRestTransport,
    ],
)
def test_cloud_build_transport_auth_gdch_credentials(transport_class):
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
        (transports.CloudBuildGrpcTransport, grpc_helpers),
        (transports.CloudBuildGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_build_transport_create_channel(transport_class, grpc_helpers):
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
            "cloudbuild.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="cloudbuild.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_cloud_build_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CloudBuildRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_cloud_build_rest_lro_client():
    client = CloudBuildClient(
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
def test_cloud_build_host_no_port(transport_name):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudbuild.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudbuild.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_build_host_with_port(transport_name):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudbuild.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudbuild.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_cloud_build_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = CloudBuildClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CloudBuildClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_build._session
    session2 = client2.transport.create_build._session
    assert session1 != session2
    session1 = client1.transport.get_build._session
    session2 = client2.transport.get_build._session
    assert session1 != session2
    session1 = client1.transport.list_builds._session
    session2 = client2.transport.list_builds._session
    assert session1 != session2
    session1 = client1.transport.cancel_build._session
    session2 = client2.transport.cancel_build._session
    assert session1 != session2
    session1 = client1.transport.retry_build._session
    session2 = client2.transport.retry_build._session
    assert session1 != session2
    session1 = client1.transport.approve_build._session
    session2 = client2.transport.approve_build._session
    assert session1 != session2
    session1 = client1.transport.create_build_trigger._session
    session2 = client2.transport.create_build_trigger._session
    assert session1 != session2
    session1 = client1.transport.get_build_trigger._session
    session2 = client2.transport.get_build_trigger._session
    assert session1 != session2
    session1 = client1.transport.list_build_triggers._session
    session2 = client2.transport.list_build_triggers._session
    assert session1 != session2
    session1 = client1.transport.delete_build_trigger._session
    session2 = client2.transport.delete_build_trigger._session
    assert session1 != session2
    session1 = client1.transport.update_build_trigger._session
    session2 = client2.transport.update_build_trigger._session
    assert session1 != session2
    session1 = client1.transport.run_build_trigger._session
    session2 = client2.transport.run_build_trigger._session
    assert session1 != session2
    session1 = client1.transport.receive_trigger_webhook._session
    session2 = client2.transport.receive_trigger_webhook._session
    assert session1 != session2
    session1 = client1.transport.create_worker_pool._session
    session2 = client2.transport.create_worker_pool._session
    assert session1 != session2
    session1 = client1.transport.get_worker_pool._session
    session2 = client2.transport.get_worker_pool._session
    assert session1 != session2
    session1 = client1.transport.delete_worker_pool._session
    session2 = client2.transport.delete_worker_pool._session
    assert session1 != session2
    session1 = client1.transport.update_worker_pool._session
    session2 = client2.transport.update_worker_pool._session
    assert session1 != session2
    session1 = client1.transport.list_worker_pools._session
    session2 = client2.transport.list_worker_pools._session
    assert session1 != session2


def test_cloud_build_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_build_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcAsyncIOTransport(
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
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_adc(transport_class):
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


def test_cloud_build_grpc_lro_client():
    client = CloudBuildClient(
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


def test_cloud_build_grpc_lro_async_client():
    client = CloudBuildAsyncClient(
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


def test_build_path():
    project = "squid"
    build = "clam"
    expected = "projects/{project}/builds/{build}".format(
        project=project,
        build=build,
    )
    actual = CloudBuildClient.build_path(project, build)
    assert expected == actual


def test_parse_build_path():
    expected = {
        "project": "whelk",
        "build": "octopus",
    }
    path = CloudBuildClient.build_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_path(path)
    assert expected == actual


def test_build_trigger_path():
    project = "oyster"
    trigger = "nudibranch"
    expected = "projects/{project}/triggers/{trigger}".format(
        project=project,
        trigger=trigger,
    )
    actual = CloudBuildClient.build_trigger_path(project, trigger)
    assert expected == actual


def test_parse_build_trigger_path():
    expected = {
        "project": "cuttlefish",
        "trigger": "mussel",
    }
    path = CloudBuildClient.build_trigger_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_trigger_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "winkle"
    location = "nautilus"
    keyring = "scallop"
    key = "abalone"
    expected = "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".format(
        project=project,
        location=location,
        keyring=keyring,
        key=key,
    )
    actual = CloudBuildClient.crypto_key_path(project, location, keyring, key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "keyring": "whelk",
        "key": "octopus",
    }
    path = CloudBuildClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_crypto_key_path(path)
    assert expected == actual


def test_github_enterprise_config_path():
    project = "oyster"
    config = "nudibranch"
    expected = "projects/{project}/githubEnterpriseConfigs/{config}".format(
        project=project,
        config=config,
    )
    actual = CloudBuildClient.github_enterprise_config_path(project, config)
    assert expected == actual


def test_parse_github_enterprise_config_path():
    expected = {
        "project": "cuttlefish",
        "config": "mussel",
    }
    path = CloudBuildClient.github_enterprise_config_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_github_enterprise_config_path(path)
    assert expected == actual


def test_network_path():
    project = "winkle"
    network = "nautilus"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project,
        network=network,
    )
    actual = CloudBuildClient.network_path(project, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "scallop",
        "network": "abalone",
    }
    path = CloudBuildClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_network_path(path)
    assert expected == actual


def test_repository_path():
    project = "squid"
    location = "clam"
    connection = "whelk"
    repository = "octopus"
    expected = "projects/{project}/locations/{location}/connections/{connection}/repositories/{repository}".format(
        project=project,
        location=location,
        connection=connection,
        repository=repository,
    )
    actual = CloudBuildClient.repository_path(project, location, connection, repository)
    assert expected == actual


def test_parse_repository_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "connection": "cuttlefish",
        "repository": "mussel",
    }
    path = CloudBuildClient.repository_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_repository_path(path)
    assert expected == actual


def test_secret_version_path():
    project = "winkle"
    secret = "nautilus"
    version = "scallop"
    expected = "projects/{project}/secrets/{secret}/versions/{version}".format(
        project=project,
        secret=secret,
        version=version,
    )
    actual = CloudBuildClient.secret_version_path(project, secret, version)
    assert expected == actual


def test_parse_secret_version_path():
    expected = {
        "project": "abalone",
        "secret": "squid",
        "version": "clam",
    }
    path = CloudBuildClient.secret_version_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_secret_version_path(path)
    assert expected == actual


def test_service_account_path():
    project = "whelk"
    service_account = "octopus"
    expected = "projects/{project}/serviceAccounts/{service_account}".format(
        project=project,
        service_account=service_account,
    )
    actual = CloudBuildClient.service_account_path(project, service_account)
    assert expected == actual


def test_parse_service_account_path():
    expected = {
        "project": "oyster",
        "service_account": "nudibranch",
    }
    path = CloudBuildClient.service_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_service_account_path(path)
    assert expected == actual


def test_subscription_path():
    project = "cuttlefish"
    subscription = "mussel"
    expected = "projects/{project}/subscriptions/{subscription}".format(
        project=project,
        subscription=subscription,
    )
    actual = CloudBuildClient.subscription_path(project, subscription)
    assert expected == actual


def test_parse_subscription_path():
    expected = {
        "project": "winkle",
        "subscription": "nautilus",
    }
    path = CloudBuildClient.subscription_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_subscription_path(path)
    assert expected == actual


def test_topic_path():
    project = "scallop"
    topic = "abalone"
    expected = "projects/{project}/topics/{topic}".format(
        project=project,
        topic=topic,
    )
    actual = CloudBuildClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "squid",
        "topic": "clam",
    }
    path = CloudBuildClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_topic_path(path)
    assert expected == actual


def test_worker_pool_path():
    project = "whelk"
    location = "octopus"
    worker_pool = "oyster"
    expected = (
        "projects/{project}/locations/{location}/workerPools/{worker_pool}".format(
            project=project,
            location=location,
            worker_pool=worker_pool,
        )
    )
    actual = CloudBuildClient.worker_pool_path(project, location, worker_pool)
    assert expected == actual


def test_parse_worker_pool_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "worker_pool": "mussel",
    }
    path = CloudBuildClient.worker_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_worker_pool_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudBuildClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = CloudBuildClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudBuildClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = CloudBuildClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudBuildClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = CloudBuildClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudBuildClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = CloudBuildClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudBuildClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = CloudBuildClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudBuildClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudBuildAsyncClient(
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
        client = CloudBuildClient(
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
        client = CloudBuildClient(
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport),
        (CloudBuildAsyncClient, transports.CloudBuildGrpcAsyncIOTransport),
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
