# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import re

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import json
import math

from google.api_core import api_core_version
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

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
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.storage_control_v2.services.storage_control import (
    StorageControlAsyncClient,
    StorageControlClient,
    pagers,
    transports,
)
from google.cloud.storage_control_v2.types import storage_control

CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


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

    assert StorageControlClient._get_default_mtls_endpoint(None) is None
    assert (
        StorageControlClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        StorageControlClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        StorageControlClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        StorageControlClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        StorageControlClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert StorageControlClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert StorageControlClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert StorageControlClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            StorageControlClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert StorageControlClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert StorageControlClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert StorageControlClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            StorageControlClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert StorageControlClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert StorageControlClient._get_client_cert_source(None, False) is None
    assert (
        StorageControlClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        StorageControlClient._get_client_cert_source(mock_provided_cert_source, True)
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
                StorageControlClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                StorageControlClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    StorageControlClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlClient),
)
@mock.patch.object(
    StorageControlAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = StorageControlClient._DEFAULT_UNIVERSE
    default_endpoint = StorageControlClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = StorageControlClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        StorageControlClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        StorageControlClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == StorageControlClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageControlClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        StorageControlClient._get_api_endpoint(None, None, default_universe, "always")
        == StorageControlClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageControlClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == StorageControlClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        StorageControlClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        StorageControlClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        StorageControlClient._get_api_endpoint(
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
        StorageControlClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        StorageControlClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        StorageControlClient._get_universe_domain(None, None)
        == StorageControlClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        StorageControlClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = StorageControlClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = StorageControlClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (StorageControlClient, "grpc"),
        (StorageControlAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_control_client_from_service_account_info(client_class, transport_name):
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
        (transports.StorageControlGrpcTransport, "grpc"),
        (transports.StorageControlGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_storage_control_client_service_account_always_use_jwt(
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
        (StorageControlClient, "grpc"),
        (StorageControlAsyncClient, "grpc_asyncio"),
    ],
)
def test_storage_control_client_from_service_account_file(client_class, transport_name):
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


def test_storage_control_client_get_transport_class():
    transport = StorageControlClient.get_transport_class()
    available_transports = [
        transports.StorageControlGrpcTransport,
    ]
    assert transport in available_transports

    transport = StorageControlClient.get_transport_class("grpc")
    assert transport == transports.StorageControlGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (StorageControlClient, transports.StorageControlGrpcTransport, "grpc"),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    StorageControlClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlClient),
)
@mock.patch.object(
    StorageControlAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlAsyncClient),
)
def test_storage_control_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(StorageControlClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(StorageControlClient, "get_transport_class") as gtc:
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
        (StorageControlClient, transports.StorageControlGrpcTransport, "grpc", "true"),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (StorageControlClient, transports.StorageControlGrpcTransport, "grpc", "false"),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    StorageControlClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlClient),
)
@mock.patch.object(
    StorageControlAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_storage_control_client_mtls_env_auto(
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
    "client_class", [StorageControlClient, StorageControlAsyncClient]
)
@mock.patch.object(
    StorageControlClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageControlClient),
)
@mock.patch.object(
    StorageControlAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(StorageControlAsyncClient),
)
def test_storage_control_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [StorageControlClient, StorageControlAsyncClient]
)
@mock.patch.object(
    StorageControlClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlClient),
)
@mock.patch.object(
    StorageControlAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(StorageControlAsyncClient),
)
def test_storage_control_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = StorageControlClient._DEFAULT_UNIVERSE
    default_endpoint = StorageControlClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = StorageControlClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (StorageControlClient, transports.StorageControlGrpcTransport, "grpc"),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_storage_control_client_client_options_scopes(
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
            StorageControlClient,
            transports.StorageControlGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_control_client_client_options_credentials_file(
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


def test_storage_control_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.storage_control_v2.services.storage_control.transports.StorageControlGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = StorageControlClient(
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
            StorageControlClient,
            transports.StorageControlGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            StorageControlAsyncClient,
            transports.StorageControlGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_storage_control_client_create_channel_credentials_file(
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
        storage_control.CreateFolderRequest,
        dict,
    ],
)
def test_create_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder(
            name="name_value",
            metageneration=1491,
        )
        response = client.create_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.Folder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


def test_create_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.CreateFolderRequest(
        parent="parent_value",
        folder_id="folder_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.CreateFolderRequest(
            parent="parent_value",
            folder_id="folder_id_value",
        )


def test_create_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_folder in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_folder] = mock_rpc
        request = {}
        client.create_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_folder
        ] = mock_rpc

        request = {}
        await client.create_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_folder_async(
    transport: str = "grpc_asyncio", request_type=storage_control.CreateFolderRequest
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        response = await client.create_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.Folder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


@pytest.mark.asyncio
async def test_create_folder_async_from_dict():
    await test_create_folder_async(request_type=dict)


def test_create_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_folder(
            parent="parent_value",
            folder=storage_control.Folder(name="name_value"),
            folder_id="folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].folder
        mock_val = storage_control.Folder(name="name_value")
        assert arg == mock_val
        arg = args[0].folder_id
        mock_val = "folder_id_value"
        assert arg == mock_val


def test_create_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_folder(
            storage_control.CreateFolderRequest(),
            parent="parent_value",
            folder=storage_control.Folder(name="name_value"),
            folder_id="folder_id_value",
        )


@pytest.mark.asyncio
async def test_create_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_folder(
            parent="parent_value",
            folder=storage_control.Folder(name="name_value"),
            folder_id="folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].folder
        mock_val = storage_control.Folder(name="name_value")
        assert arg == mock_val
        arg = args[0].folder_id
        mock_val = "folder_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_folder(
            storage_control.CreateFolderRequest(),
            parent="parent_value",
            folder=storage_control.Folder(name="name_value"),
            folder_id="folder_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.DeleteFolderRequest,
        dict,
    ],
)
def test_delete_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.DeleteFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.DeleteFolderRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.DeleteFolderRequest(
            name="name_value",
        )


def test_delete_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_folder in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_folder] = mock_rpc
        request = {}
        client.delete_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_folder
        ] = mock_rpc

        request = {}
        await client.delete_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_folder_async(
    transport: str = "grpc_asyncio", request_type=storage_control.DeleteFolderRequest
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.DeleteFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_folder_async_from_dict():
    await test_delete_folder_async(request_type=dict)


def test_delete_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_folder(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_folder(
            storage_control.DeleteFolderRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_folder(
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
async def test_delete_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_folder(
            storage_control.DeleteFolderRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetFolderRequest,
        dict,
    ],
)
def test_get_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder(
            name="name_value",
            metageneration=1491,
        )
        response = client.get_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.Folder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


def test_get_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetFolderRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.GetFolderRequest(
            name="name_value",
        )


def test_get_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_folder in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_folder] = mock_rpc
        request = {}
        client.get_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_folder_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_folder
        ] = mock_rpc

        request = {}
        await client.get_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_folder_async(
    transport: str = "grpc_asyncio", request_type=storage_control.GetFolderRequest
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        response = await client.get_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.Folder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


@pytest.mark.asyncio
async def test_get_folder_async_from_dict():
    await test_get_folder_async(request_type=dict)


def test_get_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_folder(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_folder(
            storage_control.GetFolderRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.Folder()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_folder(
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
async def test_get_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_folder(
            storage_control.GetFolderRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.ListFoldersRequest,
        dict,
    ],
)
def test_list_folders(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListFoldersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListFoldersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFoldersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_folders_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.ListFoldersRequest(
        parent="parent_value",
        page_token="page_token_value",
        prefix="prefix_value",
        delimiter="delimiter_value",
        lexicographic_start="lexicographic_start_value",
        lexicographic_end="lexicographic_end_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_folders(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.ListFoldersRequest(
            parent="parent_value",
            page_token="page_token_value",
            prefix="prefix_value",
            delimiter="delimiter_value",
            lexicographic_start="lexicographic_start_value",
            lexicographic_end="lexicographic_end_value",
        )


def test_list_folders_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_folders in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_folders] = mock_rpc
        request = {}
        client.list_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_folders(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_folders_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_folders
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_folders
        ] = mock_rpc

        request = {}
        await client.list_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_folders(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_folders_async(
    transport: str = "grpc_asyncio", request_type=storage_control.ListFoldersRequest
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListFoldersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFoldersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_folders_async_from_dict():
    await test_list_folders_async(request_type=dict)


def test_list_folders_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListFoldersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_folders(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_folders_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_folders(
            storage_control.ListFoldersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_folders_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListFoldersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListFoldersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_folders(
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
async def test_list_folders_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_folders(
            storage_control.ListFoldersRequest(),
            parent="parent_value",
        )


def test_list_folders_pager(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListFoldersResponse(
                folders=[],
                next_page_token="def",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_folders(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage_control.Folder) for i in results)


def test_list_folders_pages(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListFoldersResponse(
                folders=[],
                next_page_token="def",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_folders(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_folders_async_pager():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_folders), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListFoldersResponse(
                folders=[],
                next_page_token="def",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_folders(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage_control.Folder) for i in responses)


@pytest.mark.asyncio
async def test_list_folders_async_pages():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_folders), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListFoldersResponse(
                folders=[],
                next_page_token="def",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListFoldersResponse(
                folders=[
                    storage_control.Folder(),
                    storage_control.Folder(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_folders(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.RenameFolderRequest,
        dict,
    ],
)
def test_rename_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.rename_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.RenameFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_rename_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.RenameFolderRequest(
        name="name_value",
        destination_folder_id="destination_folder_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.rename_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.RenameFolderRequest(
            name="name_value",
            destination_folder_id="destination_folder_id_value",
        )


def test_rename_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.rename_folder in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.rename_folder] = mock_rpc
        request = {}
        client.rename_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.rename_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_rename_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.rename_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.rename_folder
        ] = mock_rpc

        request = {}
        await client.rename_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.rename_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_rename_folder_async(
    transport: str = "grpc_asyncio", request_type=storage_control.RenameFolderRequest
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.rename_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.RenameFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_rename_folder_async_from_dict():
    await test_rename_folder_async(request_type=dict)


def test_rename_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rename_folder(
            name="name_value",
            destination_folder_id="destination_folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].destination_folder_id
        mock_val = "destination_folder_id_value"
        assert arg == mock_val


def test_rename_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_folder(
            storage_control.RenameFolderRequest(),
            name="name_value",
            destination_folder_id="destination_folder_id_value",
        )


@pytest.mark.asyncio
async def test_rename_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rename_folder(
            name="name_value",
            destination_folder_id="destination_folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].destination_folder_id
        mock_val = "destination_folder_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rename_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rename_folder(
            storage_control.RenameFolderRequest(),
            name="name_value",
            destination_folder_id="destination_folder_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetStorageLayoutRequest,
        dict,
    ],
)
def test_get_storage_layout(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.StorageLayout(
            name="name_value",
            location="location_value",
            location_type="location_type_value",
        )
        response = client.get_storage_layout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetStorageLayoutRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.StorageLayout)
    assert response.name == "name_value"
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"


def test_get_storage_layout_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetStorageLayoutRequest(
        name="name_value",
        prefix="prefix_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_storage_layout(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.GetStorageLayoutRequest(
            name="name_value",
            prefix="prefix_value",
        )


def test_get_storage_layout_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_storage_layout in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_storage_layout
        ] = mock_rpc
        request = {}
        client.get_storage_layout(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_storage_layout(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_storage_layout_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_storage_layout
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_storage_layout
        ] = mock_rpc

        request = {}
        await client.get_storage_layout(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_storage_layout(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_storage_layout_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetStorageLayoutRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.StorageLayout(
                name="name_value",
                location="location_value",
                location_type="location_type_value",
            )
        )
        response = await client.get_storage_layout(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetStorageLayoutRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.StorageLayout)
    assert response.name == "name_value"
    assert response.location == "location_value"
    assert response.location_type == "location_type_value"


@pytest.mark.asyncio
async def test_get_storage_layout_async_from_dict():
    await test_get_storage_layout_async(request_type=dict)


def test_get_storage_layout_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.StorageLayout()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_storage_layout(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_storage_layout_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_storage_layout(
            storage_control.GetStorageLayoutRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_storage_layout_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.StorageLayout()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.StorageLayout()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_storage_layout(
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
async def test_get_storage_layout_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_storage_layout(
            storage_control.GetStorageLayoutRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.CreateManagedFolderRequest,
        dict,
    ],
)
def test_create_managed_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder(
            name="name_value",
            metageneration=1491,
        )
        response = client.create_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.ManagedFolder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


def test_create_managed_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.CreateManagedFolderRequest(
        parent="parent_value",
        managed_folder_id="managed_folder_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_managed_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.CreateManagedFolderRequest(
            parent="parent_value",
            managed_folder_id="managed_folder_id_value",
        )


def test_create_managed_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_managed_folder
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_managed_folder
        ] = mock_rpc
        request = {}
        client.create_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_managed_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_managed_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_managed_folder
        ] = mock_rpc

        request = {}
        await client.create_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_managed_folder_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.CreateManagedFolderRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        response = await client.create_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.ManagedFolder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


@pytest.mark.asyncio
async def test_create_managed_folder_async_from_dict():
    await test_create_managed_folder_async(request_type=dict)


def test_create_managed_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_managed_folder(
            parent="parent_value",
            managed_folder=storage_control.ManagedFolder(name="name_value"),
            managed_folder_id="managed_folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].managed_folder
        mock_val = storage_control.ManagedFolder(name="name_value")
        assert arg == mock_val
        arg = args[0].managed_folder_id
        mock_val = "managed_folder_id_value"
        assert arg == mock_val


def test_create_managed_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_managed_folder(
            storage_control.CreateManagedFolderRequest(),
            parent="parent_value",
            managed_folder=storage_control.ManagedFolder(name="name_value"),
            managed_folder_id="managed_folder_id_value",
        )


@pytest.mark.asyncio
async def test_create_managed_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_managed_folder(
            parent="parent_value",
            managed_folder=storage_control.ManagedFolder(name="name_value"),
            managed_folder_id="managed_folder_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].managed_folder
        mock_val = storage_control.ManagedFolder(name="name_value")
        assert arg == mock_val
        arg = args[0].managed_folder_id
        mock_val = "managed_folder_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_managed_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_managed_folder(
            storage_control.CreateManagedFolderRequest(),
            parent="parent_value",
            managed_folder=storage_control.ManagedFolder(name="name_value"),
            managed_folder_id="managed_folder_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.DeleteManagedFolderRequest,
        dict,
    ],
)
def test_delete_managed_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.DeleteManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_managed_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.DeleteManagedFolderRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_managed_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.DeleteManagedFolderRequest(
            name="name_value",
        )


def test_delete_managed_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_managed_folder
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_managed_folder
        ] = mock_rpc
        request = {}
        client.delete_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_managed_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_managed_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_managed_folder
        ] = mock_rpc

        request = {}
        await client.delete_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.delete_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_managed_folder_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.DeleteManagedFolderRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.DeleteManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_managed_folder_async_from_dict():
    await test_delete_managed_folder_async(request_type=dict)


def test_delete_managed_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_managed_folder(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_managed_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_managed_folder(
            storage_control.DeleteManagedFolderRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_managed_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_managed_folder(
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
async def test_delete_managed_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_managed_folder(
            storage_control.DeleteManagedFolderRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetManagedFolderRequest,
        dict,
    ],
)
def test_get_managed_folder(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder(
            name="name_value",
            metageneration=1491,
        )
        response = client.get_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.ManagedFolder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


def test_get_managed_folder_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetManagedFolderRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_managed_folder(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.GetManagedFolderRequest(
            name="name_value",
        )


def test_get_managed_folder_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_managed_folder in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_managed_folder
        ] = mock_rpc
        request = {}
        client.get_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_managed_folder_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_managed_folder
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_managed_folder
        ] = mock_rpc

        request = {}
        await client.get_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_managed_folder(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_managed_folder_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetManagedFolderRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        response = await client.get_managed_folder(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetManagedFolderRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.ManagedFolder)
    assert response.name == "name_value"
    assert response.metageneration == 1491


@pytest.mark.asyncio
async def test_get_managed_folder_async_from_dict():
    await test_get_managed_folder_async(request_type=dict)


def test_get_managed_folder_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_managed_folder(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_managed_folder_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_managed_folder(
            storage_control.GetManagedFolderRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_managed_folder_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ManagedFolder()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_managed_folder(
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
async def test_get_managed_folder_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_managed_folder(
            storage_control.GetManagedFolderRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.ListManagedFoldersRequest,
        dict,
    ],
)
def test_list_managed_folders(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListManagedFoldersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_managed_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListManagedFoldersRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListManagedFoldersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_managed_folders_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.ListManagedFoldersRequest(
        parent="parent_value",
        page_token="page_token_value",
        prefix="prefix_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_managed_folders(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.ListManagedFoldersRequest(
            parent="parent_value",
            page_token="page_token_value",
            prefix="prefix_value",
        )


def test_list_managed_folders_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_managed_folders in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_managed_folders
        ] = mock_rpc
        request = {}
        client.list_managed_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_managed_folders(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_managed_folders_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_managed_folders
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_managed_folders
        ] = mock_rpc

        request = {}
        await client.list_managed_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_managed_folders(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_managed_folders_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.ListManagedFoldersRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListManagedFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_managed_folders(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListManagedFoldersRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListManagedFoldersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_managed_folders_async_from_dict():
    await test_list_managed_folders_async(request_type=dict)


def test_list_managed_folders_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListManagedFoldersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_managed_folders(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_managed_folders_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_managed_folders(
            storage_control.ListManagedFoldersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_managed_folders_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListManagedFoldersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListManagedFoldersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_managed_folders(
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
async def test_list_managed_folders_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_managed_folders(
            storage_control.ListManagedFoldersRequest(),
            parent="parent_value",
        )


def test_list_managed_folders_pager(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[],
                next_page_token="def",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_managed_folders(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage_control.ManagedFolder) for i in results)


def test_list_managed_folders_pages(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[],
                next_page_token="def",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_managed_folders(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_managed_folders_async_pager():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[],
                next_page_token="def",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_managed_folders(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage_control.ManagedFolder) for i in responses)


@pytest.mark.asyncio
async def test_list_managed_folders_async_pages():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[],
                next_page_token="def",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListManagedFoldersResponse(
                managed_folders=[
                    storage_control.ManagedFolder(),
                    storage_control.ManagedFolder(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_managed_folders(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.CreateAnywhereCacheRequest,
        dict,
    ],
)
def test_create_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.CreateAnywhereCacheRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.CreateAnywhereCacheRequest(
            parent="parent_value",
        )


def test_create_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_anywhere_cache
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_anywhere_cache
        ] = mock_rpc
        request = {}
        client.create_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.create_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.CreateAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.CreateAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_anywhere_cache_async_from_dict():
    await test_create_anywhere_cache_async(request_type=dict)


def test_create_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_anywhere_cache(
            parent="parent_value",
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].anywhere_cache
        mock_val = storage_control.AnywhereCache(name="name_value")
        assert arg == mock_val


def test_create_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_anywhere_cache(
            storage_control.CreateAnywhereCacheRequest(),
            parent="parent_value",
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_anywhere_cache(
            parent="parent_value",
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].anywhere_cache
        mock_val = storage_control.AnywhereCache(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_anywhere_cache(
            storage_control.CreateAnywhereCacheRequest(),
            parent="parent_value",
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.UpdateAnywhereCacheRequest,
        dict,
    ],
)
def test_update_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.UpdateAnywhereCacheRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.UpdateAnywhereCacheRequest()


def test_update_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_anywhere_cache
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_anywhere_cache
        ] = mock_rpc
        request = {}
        client.update_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.update_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.UpdateAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_anywhere_cache_async_from_dict():
    await test_update_anywhere_cache_async(request_type=dict)


def test_update_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_anywhere_cache(
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].anywhere_cache
        mock_val = storage_control.AnywhereCache(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_anywhere_cache(
            storage_control.UpdateAnywhereCacheRequest(),
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_anywhere_cache(
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].anywhere_cache
        mock_val = storage_control.AnywhereCache(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_anywhere_cache(
            storage_control.UpdateAnywhereCacheRequest(),
            anywhere_cache=storage_control.AnywhereCache(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.DisableAnywhereCacheRequest,
        dict,
    ],
)
def test_disable_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache(
            name="name_value",
            zone="zone_value",
            admission_policy="admission_policy_value",
            state="state_value",
            pending_update=True,
        )
        response = client.disable_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.DisableAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


def test_disable_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.DisableAnywhereCacheRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.disable_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.DisableAnywhereCacheRequest(
            name="name_value",
        )


def test_disable_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.disable_anywhere_cache
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.disable_anywhere_cache
        ] = mock_rpc
        request = {}
        client.disable_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.disable_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_disable_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.disable_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.disable_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.disable_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.disable_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_disable_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.DisableAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        response = await client.disable_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.DisableAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


@pytest.mark.asyncio
async def test_disable_anywhere_cache_async_from_dict():
    await test_disable_anywhere_cache_async(request_type=dict)


def test_disable_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.disable_anywhere_cache(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_disable_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.disable_anywhere_cache(
            storage_control.DisableAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_disable_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.disable_anywhere_cache(
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
async def test_disable_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.disable_anywhere_cache(
            storage_control.DisableAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.PauseAnywhereCacheRequest,
        dict,
    ],
)
def test_pause_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache(
            name="name_value",
            zone="zone_value",
            admission_policy="admission_policy_value",
            state="state_value",
            pending_update=True,
        )
        response = client.pause_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.PauseAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


def test_pause_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.PauseAnywhereCacheRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.pause_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.PauseAnywhereCacheRequest(
            name="name_value",
        )


def test_pause_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.pause_anywhere_cache in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.pause_anywhere_cache
        ] = mock_rpc
        request = {}
        client.pause_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.pause_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_pause_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.pause_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.pause_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.pause_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.pause_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_pause_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.PauseAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        response = await client.pause_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.PauseAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


@pytest.mark.asyncio
async def test_pause_anywhere_cache_async_from_dict():
    await test_pause_anywhere_cache_async(request_type=dict)


def test_pause_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.pause_anywhere_cache(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_pause_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pause_anywhere_cache(
            storage_control.PauseAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_pause_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.pause_anywhere_cache(
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
async def test_pause_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.pause_anywhere_cache(
            storage_control.PauseAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.ResumeAnywhereCacheRequest,
        dict,
    ],
)
def test_resume_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache(
            name="name_value",
            zone="zone_value",
            admission_policy="admission_policy_value",
            state="state_value",
            pending_update=True,
        )
        response = client.resume_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.ResumeAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


def test_resume_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.ResumeAnywhereCacheRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.resume_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.ResumeAnywhereCacheRequest(
            name="name_value",
        )


def test_resume_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.resume_anywhere_cache
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.resume_anywhere_cache
        ] = mock_rpc
        request = {}
        client.resume_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.resume_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_resume_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.resume_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.resume_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.resume_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.resume_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_resume_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.ResumeAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        response = await client.resume_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.ResumeAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


@pytest.mark.asyncio
async def test_resume_anywhere_cache_async_from_dict():
    await test_resume_anywhere_cache_async(request_type=dict)


def test_resume_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.resume_anywhere_cache(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_resume_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resume_anywhere_cache(
            storage_control.ResumeAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_resume_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.resume_anywhere_cache(
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
async def test_resume_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.resume_anywhere_cache(
            storage_control.ResumeAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetAnywhereCacheRequest,
        dict,
    ],
)
def test_get_anywhere_cache(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache(
            name="name_value",
            zone="zone_value",
            admission_policy="admission_policy_value",
            state="state_value",
            pending_update=True,
        )
        response = client.get_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


def test_get_anywhere_cache_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetAnywhereCacheRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_anywhere_cache(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.GetAnywhereCacheRequest(
            name="name_value",
        )


def test_get_anywhere_cache_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_anywhere_cache in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_anywhere_cache
        ] = mock_rpc
        request = {}
        client.get_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_anywhere_cache_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_anywhere_cache
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_anywhere_cache
        ] = mock_rpc

        request = {}
        await client.get_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_anywhere_cache(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_anywhere_cache_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetAnywhereCacheRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        response = await client.get_anywhere_cache(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetAnywhereCacheRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.AnywhereCache)
    assert response.name == "name_value"
    assert response.zone == "zone_value"
    assert response.admission_policy == "admission_policy_value"
    assert response.state == "state_value"
    assert response.pending_update is True


@pytest.mark.asyncio
async def test_get_anywhere_cache_async_from_dict():
    await test_get_anywhere_cache_async(request_type=dict)


def test_get_anywhere_cache_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_anywhere_cache(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_anywhere_cache_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_anywhere_cache(
            storage_control.GetAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_anywhere_cache_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.AnywhereCache()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_anywhere_cache(
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
async def test_get_anywhere_cache_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_anywhere_cache(
            storage_control.GetAnywhereCacheRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.ListAnywhereCachesRequest,
        dict,
    ],
)
def test_list_anywhere_caches(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListAnywhereCachesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_anywhere_caches(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListAnywhereCachesRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnywhereCachesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_anywhere_caches_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.ListAnywhereCachesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_anywhere_caches(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        assert args[0] == storage_control.ListAnywhereCachesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_anywhere_caches_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_anywhere_caches in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_anywhere_caches
        ] = mock_rpc
        request = {}
        client.list_anywhere_caches(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_anywhere_caches(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_anywhere_caches_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_anywhere_caches
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_anywhere_caches
        ] = mock_rpc

        request = {}
        await client.list_anywhere_caches(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_anywhere_caches(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_anywhere_caches_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.ListAnywhereCachesRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    if isinstance(request, dict):
        request["request_id"] = "explicit value for autopopulate-able field"
    else:
        request.request_id = "explicit value for autopopulate-able field"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListAnywhereCachesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_anywhere_caches(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.ListAnywhereCachesRequest()
        request.request_id = "explicit value for autopopulate-able field"
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnywhereCachesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_anywhere_caches_async_from_dict():
    await test_list_anywhere_caches_async(request_type=dict)


def test_list_anywhere_caches_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListAnywhereCachesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_anywhere_caches(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_anywhere_caches_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_anywhere_caches(
            storage_control.ListAnywhereCachesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_anywhere_caches_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.ListAnywhereCachesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListAnywhereCachesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_anywhere_caches(
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
async def test_list_anywhere_caches_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_anywhere_caches(
            storage_control.ListAnywhereCachesRequest(),
            parent="parent_value",
        )


def test_list_anywhere_caches_pager(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[],
                next_page_token="def",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        pager = client.list_anywhere_caches(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, storage_control.AnywhereCache) for i in results)


def test_list_anywhere_caches_pages(transport_name: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[],
                next_page_token="def",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_anywhere_caches(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_anywhere_caches_async_pager():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[],
                next_page_token="def",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_anywhere_caches(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, storage_control.AnywhereCache) for i in responses)


@pytest.mark.asyncio
async def test_list_anywhere_caches_async_pages():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
                next_page_token="abc",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[],
                next_page_token="def",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                ],
                next_page_token="ghi",
            ),
            storage_control.ListAnywhereCachesResponse(
                anywhere_caches=[
                    storage_control.AnywhereCache(),
                    storage_control.AnywhereCache(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_anywhere_caches(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetProjectIntelligenceConfigRequest,
        dict,
    ],
)
def test_get_project_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.get_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetProjectIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_get_project_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetProjectIntelligenceConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_project_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.GetProjectIntelligenceConfigRequest(
            name="name_value",
        )


def test_get_project_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_project_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_project_intelligence_config
        ] = mock_rpc
        request = {}
        client.get_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_project_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_project_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_project_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_project_intelligence_config
        ] = mock_rpc

        request = {}
        await client.get_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_project_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_project_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetProjectIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.get_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetProjectIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_get_project_intelligence_config_async_from_dict():
    await test_get_project_intelligence_config_async(request_type=dict)


def test_get_project_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetProjectIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_project_intelligence_config(request)

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
async def test_get_project_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetProjectIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.get_project_intelligence_config(request)

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


def test_get_project_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_project_intelligence_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_project_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_project_intelligence_config(
            storage_control.GetProjectIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_project_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_project_intelligence_config(
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
async def test_get_project_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_project_intelligence_config(
            storage_control.GetProjectIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.UpdateProjectIntelligenceConfigRequest,
        dict,
    ],
)
def test_update_project_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateProjectIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_update_project_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.UpdateProjectIntelligenceConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_project_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.UpdateProjectIntelligenceConfigRequest()


def test_update_project_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_project_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_project_intelligence_config
        ] = mock_rpc
        request = {}
        client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_project_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_project_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_project_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_project_intelligence_config
        ] = mock_rpc

        request = {}
        await client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_project_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_project_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.UpdateProjectIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateProjectIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_update_project_intelligence_config_async_from_dict():
    await test_update_project_intelligence_config_async(request_type=dict)


def test_update_project_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateProjectIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_project_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateProjectIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.update_project_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


def test_update_project_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_project_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_project_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_project_intelligence_config(
            storage_control.UpdateProjectIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_project_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_project_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_project_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_project_intelligence_config(
            storage_control.UpdateProjectIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetFolderIntelligenceConfigRequest,
        dict,
    ],
)
def test_get_folder_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.get_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetFolderIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_get_folder_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetFolderIntelligenceConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_folder_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.GetFolderIntelligenceConfigRequest(
            name="name_value",
        )


def test_get_folder_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_folder_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_folder_intelligence_config
        ] = mock_rpc
        request = {}
        client.get_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_folder_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_folder_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_folder_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_folder_intelligence_config
        ] = mock_rpc

        request = {}
        await client.get_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_folder_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_folder_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetFolderIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.get_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetFolderIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_get_folder_intelligence_config_async_from_dict():
    await test_get_folder_intelligence_config_async(request_type=dict)


def test_get_folder_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetFolderIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_folder_intelligence_config(request)

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
async def test_get_folder_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetFolderIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.get_folder_intelligence_config(request)

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


def test_get_folder_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_folder_intelligence_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_folder_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_folder_intelligence_config(
            storage_control.GetFolderIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_folder_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_folder_intelligence_config(
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
async def test_get_folder_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_folder_intelligence_config(
            storage_control.GetFolderIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.UpdateFolderIntelligenceConfigRequest,
        dict,
    ],
)
def test_update_folder_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateFolderIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_update_folder_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.UpdateFolderIntelligenceConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_folder_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.UpdateFolderIntelligenceConfigRequest()


def test_update_folder_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_folder_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_folder_intelligence_config
        ] = mock_rpc
        request = {}
        client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_folder_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_folder_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_folder_intelligence_config
        ] = mock_rpc

        request = {}
        await client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_folder_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.UpdateFolderIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateFolderIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_async_from_dict():
    await test_update_folder_intelligence_config_async(request_type=dict)


def test_update_folder_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateFolderIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateFolderIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.update_folder_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


def test_update_folder_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_folder_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_folder_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_folder_intelligence_config(
            storage_control.UpdateFolderIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_folder_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_folder_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_folder_intelligence_config(
            storage_control.UpdateFolderIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.GetOrganizationIntelligenceConfigRequest,
        dict,
    ],
)
def test_get_organization_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.get_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetOrganizationIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_get_organization_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.GetOrganizationIntelligenceConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_organization_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.GetOrganizationIntelligenceConfigRequest(
            name="name_value",
        )


def test_get_organization_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_organization_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_organization_intelligence_config
        ] = mock_rpc
        request = {}
        client.get_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_organization_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_organization_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_organization_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_organization_intelligence_config
        ] = mock_rpc

        request = {}
        await client.get_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_organization_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_organization_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.GetOrganizationIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.get_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.GetOrganizationIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_get_organization_intelligence_config_async_from_dict():
    await test_get_organization_intelligence_config_async(request_type=dict)


def test_get_organization_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetOrganizationIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_organization_intelligence_config(request)

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
async def test_get_organization_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.GetOrganizationIntelligenceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.get_organization_intelligence_config(request)

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


def test_get_organization_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_organization_intelligence_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_organization_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_organization_intelligence_config(
            storage_control.GetOrganizationIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_organization_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_organization_intelligence_config(
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
async def test_get_organization_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_organization_intelligence_config(
            storage_control.GetOrganizationIntelligenceConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        storage_control.UpdateOrganizationIntelligenceConfigRequest,
        dict,
    ],
)
def test_update_organization_intelligence_config(request_type, transport: str = "grpc"):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig(
            name="name_value",
            edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
        )
        response = client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateOrganizationIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


def test_update_organization_intelligence_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = storage_control.UpdateOrganizationIntelligenceConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_organization_intelligence_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == storage_control.UpdateOrganizationIntelligenceConfigRequest()


def test_update_organization_intelligence_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_organization_intelligence_config
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_organization_intelligence_config
        ] = mock_rpc
        request = {}
        client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_organization_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = StorageControlAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_organization_intelligence_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_organization_intelligence_config
        ] = mock_rpc

        request = {}
        await client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_organization_intelligence_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_async(
    transport: str = "grpc_asyncio",
    request_type=storage_control.UpdateOrganizationIntelligenceConfigRequest,
):
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        response = await client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = storage_control.UpdateOrganizationIntelligenceConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage_control.IntelligenceConfig)
    assert response.name == "name_value"
    assert (
        response.edition_config
        == storage_control.IntelligenceConfig.EditionConfig.INHERIT
    )


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_async_from_dict():
    await test_update_organization_intelligence_config_async(request_type=dict)


def test_update_organization_intelligence_config_field_headers():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateOrganizationIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_field_headers_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage_control.UpdateOrganizationIntelligenceConfigRequest()

    request.intelligence_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        await client.update_organization_intelligence_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "intelligence_config.name=name_value",
    ) in kw["metadata"]


def test_update_organization_intelligence_config_flattened():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_organization_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_organization_intelligence_config_flattened_error():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_organization_intelligence_config(
            storage_control.UpdateOrganizationIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_flattened_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage_control.IntelligenceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_organization_intelligence_config(
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].intelligence_config
        mock_val = storage_control.IntelligenceConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_organization_intelligence_config_flattened_error_async():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_organization_intelligence_config(
            storage_control.UpdateOrganizationIntelligenceConfigRequest(),
            intelligence_config=storage_control.IntelligenceConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageControlClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageControlClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = StorageControlClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = StorageControlClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = StorageControlClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.StorageControlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.StorageControlGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = StorageControlClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        call.return_value = storage_control.Folder()
        client.create_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        call.return_value = None
        client.delete_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        call.return_value = storage_control.Folder()
        client.get_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_folders_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        call.return_value = storage_control.ListFoldersResponse()
        client.list_folders(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.ListFoldersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_rename_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.rename_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.RenameFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_storage_layout_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        call.return_value = storage_control.StorageLayout()
        client.get_storage_layout(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetStorageLayoutRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_managed_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        call.return_value = storage_control.ManagedFolder()
        client.create_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_managed_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        call.return_value = None
        client.delete_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_managed_folder_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        call.return_value = storage_control.ManagedFolder()
        client.get_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_managed_folders_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        call.return_value = storage_control.ListManagedFoldersResponse()
        client.list_managed_folders(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListManagedFoldersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.UpdateAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_disable_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.disable_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DisableAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_pause_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.pause_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.PauseAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_resume_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.resume_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ResumeAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_anywhere_cache_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.get_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_anywhere_caches_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        call.return_value = storage_control.ListAnywhereCachesResponse()
        client.list_anywhere_caches(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListAnywhereCachesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_project_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_project_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetProjectIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_project_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_project_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateProjectIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_folder_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_folder_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetFolderIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_folder_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_folder_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateFolderIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_organization_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.get_organization_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetOrganizationIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_organization_intelligence_config_empty_call_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        call.return_value = storage_control.IntelligenceConfig()
        client.update_organization_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateOrganizationIntelligenceConfigRequest()

        assert args[0] == request_msg


def test_create_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        call.return_value = storage_control.Folder()
        client.create_folder(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateFolderRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_delete_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        call.return_value = None
        client.delete_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        call.return_value = storage_control.Folder()
        client.get_folder(request={"name": "projects/sample1/buckets/sample2/sample3"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_folders_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        call.return_value = storage_control.ListFoldersResponse()
        client.list_folders(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = storage_control.ListFoldersRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_rename_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.rename_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.RenameFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_storage_layout_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        call.return_value = storage_control.StorageLayout()
        client.get_storage_layout(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetStorageLayoutRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_create_managed_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        call.return_value = storage_control.ManagedFolder()
        client.create_managed_folder(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateManagedFolderRequest(
            **{"parent": "sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_delete_managed_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        call.return_value = None
        client.delete_managed_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteManagedFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_managed_folder_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        call.return_value = storage_control.ManagedFolder()
        client.get_managed_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetManagedFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_managed_folders_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        call.return_value = storage_control.ListManagedFoldersResponse()
        client.list_managed_folders(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListManagedFoldersRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_create_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_anywhere_cache(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateAnywhereCacheRequest(
            **{"parent": "sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_update_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_anywhere_cache(
            request={
                "anywhere_cache": {"name": "projects/sample1/buckets/sample2/sample3"}
            }
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.UpdateAnywhereCacheRequest(
            **{"anywhere_cache": {"name": "projects/sample1/buckets/sample2/sample3"}}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_disable_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.disable_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DisableAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_pause_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.pause_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.PauseAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_resume_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.resume_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ResumeAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_get_anywhere_cache_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        call.return_value = storage_control.AnywhereCache()
        client.get_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_list_anywhere_caches_routing_parameters_request_1_grpc():
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        call.return_value = storage_control.ListAnywhereCachesResponse()
        client.list_anywhere_caches(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListAnywhereCachesRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_transport_kind_grpc_asyncio():
    transport = StorageControlAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.create_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.get_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_folders_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_folders(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.ListFoldersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_rename_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.rename_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.RenameFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_storage_layout_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.StorageLayout(
                name="name_value",
                location="location_value",
                location_type="location_type_value",
            )
        )
        await client.get_storage_layout(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetStorageLayoutRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_managed_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.create_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_managed_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_managed_folder_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.get_managed_folder(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetManagedFolderRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_managed_folders_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListManagedFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_managed_folders(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListManagedFoldersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.update_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.UpdateAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_disable_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.disable_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DisableAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_pause_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.pause_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.PauseAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_resume_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.resume_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ResumeAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_anywhere_cache_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.get_anywhere_cache(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetAnywhereCacheRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_anywhere_caches_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListAnywhereCachesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_anywhere_caches(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListAnywhereCachesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_project_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.get_project_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetProjectIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_project_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.update_project_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateProjectIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_folder_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.get_folder_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetFolderIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_folder_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_folder_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.update_folder_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateFolderIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_organization_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.get_organization_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.GetOrganizationIntelligenceConfigRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_organization_intelligence_config_empty_call_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_intelligence_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.IntelligenceConfig(
                name="name_value",
                edition_config=storage_control.IntelligenceConfig.EditionConfig.INHERIT,
            )
        )
        await client.update_organization_intelligence_config(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = storage_control.UpdateOrganizationIntelligenceConfigRequest()

        assert args[0] == request_msg


@pytest.mark.asyncio
async def test_create_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.create_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.create_folder(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateFolderRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_delete_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.delete_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.get_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.Folder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.get_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_list_folders_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_folders), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_folders(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        request_msg = storage_control.ListFoldersRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_rename_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.rename_folder), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.rename_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.RenameFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_storage_layout_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_storage_layout), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.StorageLayout(
                name="name_value",
                location="location_value",
                location_type="location_type_value",
            )
        )
        await client.get_storage_layout(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetStorageLayoutRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_create_managed_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.create_managed_folder(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateManagedFolderRequest(
            **{"parent": "sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_delete_managed_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_managed_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DeleteManagedFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_managed_folder_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_managed_folder), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ManagedFolder(
                name="name_value",
                metageneration=1491,
            )
        )
        await client.get_managed_folder(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetManagedFolderRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_list_managed_folders_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_managed_folders), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListManagedFoldersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_managed_folders(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListManagedFoldersRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_create_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_anywhere_cache(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.CreateAnywhereCacheRequest(
            **{"parent": "sample1"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_update_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.update_anywhere_cache(
            request={
                "anywhere_cache": {"name": "projects/sample1/buckets/sample2/sample3"}
            }
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.UpdateAnywhereCacheRequest(
            **{"anywhere_cache": {"name": "projects/sample1/buckets/sample2/sample3"}}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_disable_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.disable_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.DisableAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_pause_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.pause_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.pause_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.PauseAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_resume_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.resume_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ResumeAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_get_anywhere_cache_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_anywhere_cache), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.AnywhereCache(
                name="name_value",
                zone="zone_value",
                admission_policy="admission_policy_value",
                state="state_value",
                pending_update=True,
            )
        )
        await client.get_anywhere_cache(
            request={"name": "projects/sample1/buckets/sample2/sample3"}
        )

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.GetAnywhereCacheRequest(
            **{"name": "projects/sample1/buckets/sample2/sample3"}
        )

        assert args[0] == request_msg

        expected_headers = {"bucket": "projects/sample1/buckets/sample2"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


@pytest.mark.asyncio
async def test_list_anywhere_caches_routing_parameters_request_1_grpc_asyncio():
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_anywhere_caches), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage_control.ListAnywhereCachesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_anywhere_caches(request={"parent": "sample1"})

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, kw = call.mock_calls[0]
        # Ensure that the uuid4 field is set according to AIP 4235
        assert re.match(
            r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",
            args[0].request_id,
        )
        # clear UUID field so that the check below succeeds
        args[0].request_id = None
        request_msg = storage_control.ListAnywhereCachesRequest(**{"parent": "sample1"})

        assert args[0] == request_msg

        expected_headers = {"bucket": "sample1"}
        assert (
            gapic_v1.routing_header.to_grpc_metadata(expected_headers) in kw["metadata"]
        )


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.StorageControlGrpcTransport,
    )


def test_storage_control_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.StorageControlTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_storage_control_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.storage_control_v2.services.storage_control.transports.StorageControlTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.StorageControlTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_folder",
        "delete_folder",
        "get_folder",
        "list_folders",
        "rename_folder",
        "get_storage_layout",
        "create_managed_folder",
        "delete_managed_folder",
        "get_managed_folder",
        "list_managed_folders",
        "create_anywhere_cache",
        "update_anywhere_cache",
        "disable_anywhere_cache",
        "pause_anywhere_cache",
        "resume_anywhere_cache",
        "get_anywhere_cache",
        "list_anywhere_caches",
        "get_project_intelligence_config",
        "update_project_intelligence_config",
        "get_folder_intelligence_config",
        "update_folder_intelligence_config",
        "get_organization_intelligence_config",
        "update_organization_intelligence_config",
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


def test_storage_control_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.storage_control_v2.services.storage_control.transports.StorageControlTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageControlTransport(
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


def test_storage_control_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.storage_control_v2.services.storage_control.transports.StorageControlTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.StorageControlTransport()
        adc.assert_called_once()


def test_storage_control_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        StorageControlClient()
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
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_storage_control_transport_auth_adc(transport_class):
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
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_storage_control_transport_auth_gdch_credentials(transport_class):
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
        (transports.StorageControlGrpcTransport, grpc_helpers),
        (transports.StorageControlGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_storage_control_transport_create_channel(transport_class, grpc_helpers):
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
    [
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_storage_control_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_storage_control_host_no_port(transport_name):
    client = StorageControlClient(
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
def test_storage_control_host_with_port(transport_name):
    client = StorageControlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="storage.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("storage.googleapis.com:8000")


def test_storage_control_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageControlGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_storage_control_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.StorageControlGrpcAsyncIOTransport(
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
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_storage_control_transport_channel_mtls_with_client_cert_source(
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
        transports.StorageControlGrpcTransport,
        transports.StorageControlGrpcAsyncIOTransport,
    ],
)
def test_storage_control_transport_channel_mtls_with_adc(transport_class):
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


def test_storage_control_grpc_lro_client():
    client = StorageControlClient(
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


def test_storage_control_grpc_lro_async_client():
    client = StorageControlAsyncClient(
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


def test_anywhere_cache_path():
    project = "squid"
    bucket = "clam"
    anywhere_cache = "whelk"
    expected = (
        "projects/{project}/buckets/{bucket}/anywhereCaches/{anywhere_cache}".format(
            project=project,
            bucket=bucket,
            anywhere_cache=anywhere_cache,
        )
    )
    actual = StorageControlClient.anywhere_cache_path(project, bucket, anywhere_cache)
    assert expected == actual


def test_parse_anywhere_cache_path():
    expected = {
        "project": "octopus",
        "bucket": "oyster",
        "anywhere_cache": "nudibranch",
    }
    path = StorageControlClient.anywhere_cache_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_anywhere_cache_path(path)
    assert expected == actual


def test_folder_path():
    project = "cuttlefish"
    bucket = "mussel"
    folder = "winkle"
    expected = "projects/{project}/buckets/{bucket}/folders/{folder}".format(
        project=project,
        bucket=bucket,
        folder=folder,
    )
    actual = StorageControlClient.folder_path(project, bucket, folder)
    assert expected == actual


def test_parse_folder_path():
    expected = {
        "project": "nautilus",
        "bucket": "scallop",
        "folder": "abalone",
    }
    path = StorageControlClient.folder_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_folder_path(path)
    assert expected == actual


def test_intelligence_config_path():
    folder = "squid"
    location = "clam"
    expected = "folders/{folder}/locations/{location}/intelligenceConfig".format(
        folder=folder,
        location=location,
    )
    actual = StorageControlClient.intelligence_config_path(folder, location)
    assert expected == actual


def test_parse_intelligence_config_path():
    expected = {
        "folder": "whelk",
        "location": "octopus",
    }
    path = StorageControlClient.intelligence_config_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_intelligence_config_path(path)
    assert expected == actual


def test_managed_folder_path():
    project = "oyster"
    bucket = "nudibranch"
    managed_folder = "cuttlefish"
    expected = (
        "projects/{project}/buckets/{bucket}/managedFolders/{managed_folder}".format(
            project=project,
            bucket=bucket,
            managed_folder=managed_folder,
        )
    )
    actual = StorageControlClient.managed_folder_path(project, bucket, managed_folder)
    assert expected == actual


def test_parse_managed_folder_path():
    expected = {
        "project": "mussel",
        "bucket": "winkle",
        "managed_folder": "nautilus",
    }
    path = StorageControlClient.managed_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_managed_folder_path(path)
    assert expected == actual


def test_storage_layout_path():
    project = "scallop"
    bucket = "abalone"
    expected = "projects/{project}/buckets/{bucket}/storageLayout".format(
        project=project,
        bucket=bucket,
    )
    actual = StorageControlClient.storage_layout_path(project, bucket)
    assert expected == actual


def test_parse_storage_layout_path():
    expected = {
        "project": "squid",
        "bucket": "clam",
    }
    path = StorageControlClient.storage_layout_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_storage_layout_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = StorageControlClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = StorageControlClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = StorageControlClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = StorageControlClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = StorageControlClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = StorageControlClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = StorageControlClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = StorageControlClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = StorageControlClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = StorageControlClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = StorageControlClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.StorageControlTransport, "_prep_wrapped_messages"
    ) as prep:
        client = StorageControlClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.StorageControlTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = StorageControlClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = StorageControlClient(
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
    client = StorageControlAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = StorageControlClient(
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
        (StorageControlClient, transports.StorageControlGrpcTransport),
        (StorageControlAsyncClient, transports.StorageControlGrpcAsyncIOTransport),
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
