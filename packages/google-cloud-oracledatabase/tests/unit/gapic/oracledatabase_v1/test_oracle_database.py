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
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
from google.type import month_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore

from google.cloud.oracledatabase_v1.services.oracle_database import (
    OracleDatabaseAsyncClient,
    OracleDatabaseClient,
    pagers,
    transports,
)
from google.cloud.oracledatabase_v1.types import (
    autonomous_database_character_set,
    autonomous_db_backup,
    autonomous_db_version,
    common,
    db_node,
    db_server,
    db_system_shape,
    entitlement,
    exadata_infra,
    gi_version,
    oracledatabase,
    vm_cluster,
)
from google.cloud.oracledatabase_v1.types import (
    autonomous_database as gco_autonomous_database,
)
from google.cloud.oracledatabase_v1.types import autonomous_database

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

    assert OracleDatabaseClient._get_default_mtls_endpoint(None) is None
    assert (
        OracleDatabaseClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OracleDatabaseClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OracleDatabaseClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OracleDatabaseClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OracleDatabaseClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert OracleDatabaseClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            OracleDatabaseClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            OracleDatabaseClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert OracleDatabaseClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert OracleDatabaseClient._get_client_cert_source(None, False) is None
    assert (
        OracleDatabaseClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        OracleDatabaseClient._get_client_cert_source(mock_provided_cert_source, True)
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
                OracleDatabaseClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                OracleDatabaseClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    OracleDatabaseClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseClient),
)
@mock.patch.object(
    OracleDatabaseAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = OracleDatabaseClient._DEFAULT_UNIVERSE
    default_endpoint = OracleDatabaseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = OracleDatabaseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        OracleDatabaseClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == OracleDatabaseClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(None, None, default_universe, "always")
        == OracleDatabaseClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == OracleDatabaseClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        OracleDatabaseClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        OracleDatabaseClient._get_api_endpoint(
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
        OracleDatabaseClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        OracleDatabaseClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        OracleDatabaseClient._get_universe_domain(None, None)
        == OracleDatabaseClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        OracleDatabaseClient._get_universe_domain("", None)
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
    client = OracleDatabaseClient(credentials=cred)
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
    client = OracleDatabaseClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OracleDatabaseClient, "grpc"),
        (OracleDatabaseAsyncClient, "grpc_asyncio"),
        (OracleDatabaseClient, "rest"),
    ],
)
def test_oracle_database_client_from_service_account_info(client_class, transport_name):
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
            "oracledatabase.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://oracledatabase.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.OracleDatabaseGrpcTransport, "grpc"),
        (transports.OracleDatabaseGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.OracleDatabaseRestTransport, "rest"),
    ],
)
def test_oracle_database_client_service_account_always_use_jwt(
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
        (OracleDatabaseClient, "grpc"),
        (OracleDatabaseAsyncClient, "grpc_asyncio"),
        (OracleDatabaseClient, "rest"),
    ],
)
def test_oracle_database_client_from_service_account_file(client_class, transport_name):
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
            "oracledatabase.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://oracledatabase.googleapis.com"
        )


def test_oracle_database_client_get_transport_class():
    transport = OracleDatabaseClient.get_transport_class()
    available_transports = [
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseRestTransport,
    ]
    assert transport in available_transports

    transport = OracleDatabaseClient.get_transport_class("grpc")
    assert transport == transports.OracleDatabaseGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OracleDatabaseClient, transports.OracleDatabaseGrpcTransport, "grpc"),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (OracleDatabaseClient, transports.OracleDatabaseRestTransport, "rest"),
    ],
)
@mock.patch.object(
    OracleDatabaseClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseClient),
)
@mock.patch.object(
    OracleDatabaseAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseAsyncClient),
)
def test_oracle_database_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(OracleDatabaseClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(OracleDatabaseClient, "get_transport_class") as gtc:
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
        (OracleDatabaseClient, transports.OracleDatabaseGrpcTransport, "grpc", "true"),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (OracleDatabaseClient, transports.OracleDatabaseGrpcTransport, "grpc", "false"),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (OracleDatabaseClient, transports.OracleDatabaseRestTransport, "rest", "true"),
        (OracleDatabaseClient, transports.OracleDatabaseRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    OracleDatabaseClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseClient),
)
@mock.patch.object(
    OracleDatabaseAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_oracle_database_client_mtls_env_auto(
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
    "client_class", [OracleDatabaseClient, OracleDatabaseAsyncClient]
)
@mock.patch.object(
    OracleDatabaseClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OracleDatabaseClient),
)
@mock.patch.object(
    OracleDatabaseAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OracleDatabaseAsyncClient),
)
def test_oracle_database_client_get_mtls_endpoint_and_cert_source(client_class):
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
    "client_class", [OracleDatabaseClient, OracleDatabaseAsyncClient]
)
@mock.patch.object(
    OracleDatabaseClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseClient),
)
@mock.patch.object(
    OracleDatabaseAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OracleDatabaseAsyncClient),
)
def test_oracle_database_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = OracleDatabaseClient._DEFAULT_UNIVERSE
    default_endpoint = OracleDatabaseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = OracleDatabaseClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
        (OracleDatabaseClient, transports.OracleDatabaseGrpcTransport, "grpc"),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (OracleDatabaseClient, transports.OracleDatabaseRestTransport, "rest"),
    ],
)
def test_oracle_database_client_client_options_scopes(
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
            OracleDatabaseClient,
            transports.OracleDatabaseGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (OracleDatabaseClient, transports.OracleDatabaseRestTransport, "rest", None),
    ],
)
def test_oracle_database_client_client_options_credentials_file(
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


def test_oracle_database_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.oracledatabase_v1.services.oracle_database.transports.OracleDatabaseGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OracleDatabaseClient(
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
            OracleDatabaseClient,
            transports.OracleDatabaseGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OracleDatabaseAsyncClient,
            transports.OracleDatabaseGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_oracle_database_client_create_channel_credentials_file(
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
            "oracledatabase.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="oracledatabase.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListCloudExadataInfrastructuresRequest,
        dict,
    ],
)
def test_list_cloud_exadata_infrastructures(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_cloud_exadata_infrastructures(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListCloudExadataInfrastructuresRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudExadataInfrastructuresPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_cloud_exadata_infrastructures_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListCloudExadataInfrastructuresRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_cloud_exadata_infrastructures(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListCloudExadataInfrastructuresRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_cloud_exadata_infrastructures_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_cloud_exadata_infrastructures
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_cloud_exadata_infrastructures
        ] = mock_rpc
        request = {}
        client.list_cloud_exadata_infrastructures(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_cloud_exadata_infrastructures(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_cloud_exadata_infrastructures
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_cloud_exadata_infrastructures
        ] = mock_rpc

        request = {}
        await client.list_cloud_exadata_infrastructures(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_cloud_exadata_infrastructures(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListCloudExadataInfrastructuresRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_cloud_exadata_infrastructures(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListCloudExadataInfrastructuresRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudExadataInfrastructuresAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_async_from_dict():
    await test_list_cloud_exadata_infrastructures_async(request_type=dict)


def test_list_cloud_exadata_infrastructures_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListCloudExadataInfrastructuresRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()
        client.list_cloud_exadata_infrastructures(request)

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
async def test_list_cloud_exadata_infrastructures_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListCloudExadataInfrastructuresRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudExadataInfrastructuresResponse()
        )
        await client.list_cloud_exadata_infrastructures(request)

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


def test_list_cloud_exadata_infrastructures_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_cloud_exadata_infrastructures(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_cloud_exadata_infrastructures_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cloud_exadata_infrastructures(
            oracledatabase.ListCloudExadataInfrastructuresRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudExadataInfrastructuresResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_cloud_exadata_infrastructures(
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
async def test_list_cloud_exadata_infrastructures_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_cloud_exadata_infrastructures(
            oracledatabase.ListCloudExadataInfrastructuresRequest(),
            parent="parent_value",
        )


def test_list_cloud_exadata_infrastructures_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
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
        pager = client.list_cloud_exadata_infrastructures(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, exadata_infra.CloudExadataInfrastructure) for i in results
        )


def test_list_cloud_exadata_infrastructures_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_cloud_exadata_infrastructures(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_cloud_exadata_infrastructures(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, exadata_infra.CloudExadataInfrastructure) for i in responses
        )


@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_cloud_exadata_infrastructures(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_get_cloud_exadata_infrastructure(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = exadata_infra.CloudExadataInfrastructure(
            name="name_value",
            display_name="display_name_value",
            gcp_oracle_zone="gcp_oracle_zone_value",
            entitlement_id="entitlement_id_value",
        )
        response = client.get_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, exadata_infra.CloudExadataInfrastructure)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.entitlement_id == "entitlement_id_value"


def test_get_cloud_exadata_infrastructure_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.GetCloudExadataInfrastructureRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_cloud_exadata_infrastructure(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.GetCloudExadataInfrastructureRequest(
            name="name_value",
        )


def test_get_cloud_exadata_infrastructure_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_cloud_exadata_infrastructure
        ] = mock_rpc
        request = {}
        client.get_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cloud_exadata_infrastructure_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_cloud_exadata_infrastructure
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        await client.get_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cloud_exadata_infrastructure_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.GetCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            exadata_infra.CloudExadataInfrastructure(
                name="name_value",
                display_name="display_name_value",
                gcp_oracle_zone="gcp_oracle_zone_value",
                entitlement_id="entitlement_id_value",
            )
        )
        response = await client.get_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, exadata_infra.CloudExadataInfrastructure)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.entitlement_id == "entitlement_id_value"


@pytest.mark.asyncio
async def test_get_cloud_exadata_infrastructure_async_from_dict():
    await test_get_cloud_exadata_infrastructure_async(request_type=dict)


def test_get_cloud_exadata_infrastructure_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetCloudExadataInfrastructureRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = exadata_infra.CloudExadataInfrastructure()
        client.get_cloud_exadata_infrastructure(request)

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
async def test_get_cloud_exadata_infrastructure_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetCloudExadataInfrastructureRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            exadata_infra.CloudExadataInfrastructure()
        )
        await client.get_cloud_exadata_infrastructure(request)

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


def test_get_cloud_exadata_infrastructure_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = exadata_infra.CloudExadataInfrastructure()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cloud_exadata_infrastructure(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_cloud_exadata_infrastructure_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cloud_exadata_infrastructure(
            oracledatabase.GetCloudExadataInfrastructureRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cloud_exadata_infrastructure_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = exadata_infra.CloudExadataInfrastructure()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            exadata_infra.CloudExadataInfrastructure()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cloud_exadata_infrastructure(
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
async def test_get_cloud_exadata_infrastructure_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cloud_exadata_infrastructure(
            oracledatabase.GetCloudExadataInfrastructureRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_create_cloud_exadata_infrastructure(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cloud_exadata_infrastructure_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.CreateCloudExadataInfrastructureRequest(
        parent="parent_value",
        cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_cloud_exadata_infrastructure(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.CreateCloudExadataInfrastructureRequest(
            parent="parent_value",
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )


def test_create_cloud_exadata_infrastructure_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_cloud_exadata_infrastructure
        ] = mock_rpc
        request = {}
        client.create_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_cloud_exadata_infrastructure
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        await client.create_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.CreateCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_async_from_dict():
    await test_create_cloud_exadata_infrastructure_async(request_type=dict)


def test_create_cloud_exadata_infrastructure_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateCloudExadataInfrastructureRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cloud_exadata_infrastructure(request)

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
async def test_create_cloud_exadata_infrastructure_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateCloudExadataInfrastructureRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_cloud_exadata_infrastructure(request)

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


def test_create_cloud_exadata_infrastructure_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cloud_exadata_infrastructure(
            parent="parent_value",
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cloud_exadata_infrastructure
        mock_val = exadata_infra.CloudExadataInfrastructure(name="name_value")
        assert arg == mock_val
        arg = args[0].cloud_exadata_infrastructure_id
        mock_val = "cloud_exadata_infrastructure_id_value"
        assert arg == mock_val


def test_create_cloud_exadata_infrastructure_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cloud_exadata_infrastructure(
            oracledatabase.CreateCloudExadataInfrastructureRequest(),
            parent="parent_value",
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )


@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cloud_exadata_infrastructure(
            parent="parent_value",
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cloud_exadata_infrastructure
        mock_val = exadata_infra.CloudExadataInfrastructure(name="name_value")
        assert arg == mock_val
        arg = args[0].cloud_exadata_infrastructure_id
        mock_val = "cloud_exadata_infrastructure_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cloud_exadata_infrastructure(
            oracledatabase.CreateCloudExadataInfrastructureRequest(),
            parent="parent_value",
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_delete_cloud_exadata_infrastructure(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_cloud_exadata_infrastructure_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.DeleteCloudExadataInfrastructureRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_cloud_exadata_infrastructure(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.DeleteCloudExadataInfrastructureRequest(
            name="name_value",
        )


def test_delete_cloud_exadata_infrastructure_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_cloud_exadata_infrastructure
        ] = mock_rpc
        request = {}
        client.delete_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cloud_exadata_infrastructure_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_cloud_exadata_infrastructure
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        await client.delete_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cloud_exadata_infrastructure_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.DeleteCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteCloudExadataInfrastructureRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_cloud_exadata_infrastructure_async_from_dict():
    await test_delete_cloud_exadata_infrastructure_async(request_type=dict)


def test_delete_cloud_exadata_infrastructure_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteCloudExadataInfrastructureRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_cloud_exadata_infrastructure(request)

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
async def test_delete_cloud_exadata_infrastructure_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteCloudExadataInfrastructureRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_cloud_exadata_infrastructure(request)

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


def test_delete_cloud_exadata_infrastructure_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cloud_exadata_infrastructure(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_cloud_exadata_infrastructure_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cloud_exadata_infrastructure(
            oracledatabase.DeleteCloudExadataInfrastructureRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_cloud_exadata_infrastructure_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cloud_exadata_infrastructure(
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
async def test_delete_cloud_exadata_infrastructure_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cloud_exadata_infrastructure(
            oracledatabase.DeleteCloudExadataInfrastructureRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListCloudVmClustersRequest,
        dict,
    ],
)
def test_list_cloud_vm_clusters(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudVmClustersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_cloud_vm_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListCloudVmClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudVmClustersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_cloud_vm_clusters_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListCloudVmClustersRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_cloud_vm_clusters(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListCloudVmClustersRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_cloud_vm_clusters_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_cloud_vm_clusters
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_cloud_vm_clusters
        ] = mock_rpc
        request = {}
        client.list_cloud_vm_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_cloud_vm_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_cloud_vm_clusters
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_cloud_vm_clusters
        ] = mock_rpc

        request = {}
        await client.list_cloud_vm_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_cloud_vm_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListCloudVmClustersRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudVmClustersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_cloud_vm_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListCloudVmClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudVmClustersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_async_from_dict():
    await test_list_cloud_vm_clusters_async(request_type=dict)


def test_list_cloud_vm_clusters_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListCloudVmClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListCloudVmClustersResponse()
        client.list_cloud_vm_clusters(request)

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
async def test_list_cloud_vm_clusters_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListCloudVmClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudVmClustersResponse()
        )
        await client.list_cloud_vm_clusters(request)

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


def test_list_cloud_vm_clusters_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudVmClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_cloud_vm_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_cloud_vm_clusters_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cloud_vm_clusters(
            oracledatabase.ListCloudVmClustersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListCloudVmClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudVmClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_cloud_vm_clusters(
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
async def test_list_cloud_vm_clusters_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_cloud_vm_clusters(
            oracledatabase.ListCloudVmClustersRequest(),
            parent="parent_value",
        )


def test_list_cloud_vm_clusters_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
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
        pager = client.list_cloud_vm_clusters(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, vm_cluster.CloudVmCluster) for i in results)


def test_list_cloud_vm_clusters_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_cloud_vm_clusters(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_cloud_vm_clusters(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vm_cluster.CloudVmCluster) for i in responses)


@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_cloud_vm_clusters(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetCloudVmClusterRequest,
        dict,
    ],
)
def test_get_cloud_vm_cluster(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vm_cluster.CloudVmCluster(
            name="name_value",
            exadata_infrastructure="exadata_infrastructure_value",
            display_name="display_name_value",
            gcp_oracle_zone="gcp_oracle_zone_value",
            cidr="cidr_value",
            backup_subnet_cidr="backup_subnet_cidr_value",
            network="network_value",
        )
        response = client.get_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, vm_cluster.CloudVmCluster)
    assert response.name == "name_value"
    assert response.exadata_infrastructure == "exadata_infrastructure_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.cidr == "cidr_value"
    assert response.backup_subnet_cidr == "backup_subnet_cidr_value"
    assert response.network == "network_value"


def test_get_cloud_vm_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.GetCloudVmClusterRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_cloud_vm_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.GetCloudVmClusterRequest(
            name="name_value",
        )


def test_get_cloud_vm_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_cloud_vm_cluster in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_cloud_vm_cluster
        ] = mock_rpc
        request = {}
        client.get_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cloud_vm_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_cloud_vm_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        await client.get_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cloud_vm_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.GetCloudVmClusterRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vm_cluster.CloudVmCluster(
                name="name_value",
                exadata_infrastructure="exadata_infrastructure_value",
                display_name="display_name_value",
                gcp_oracle_zone="gcp_oracle_zone_value",
                cidr="cidr_value",
                backup_subnet_cidr="backup_subnet_cidr_value",
                network="network_value",
            )
        )
        response = await client.get_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, vm_cluster.CloudVmCluster)
    assert response.name == "name_value"
    assert response.exadata_infrastructure == "exadata_infrastructure_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.cidr == "cidr_value"
    assert response.backup_subnet_cidr == "backup_subnet_cidr_value"
    assert response.network == "network_value"


@pytest.mark.asyncio
async def test_get_cloud_vm_cluster_async_from_dict():
    await test_get_cloud_vm_cluster_async(request_type=dict)


def test_get_cloud_vm_cluster_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetCloudVmClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = vm_cluster.CloudVmCluster()
        client.get_cloud_vm_cluster(request)

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
async def test_get_cloud_vm_cluster_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetCloudVmClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vm_cluster.CloudVmCluster()
        )
        await client.get_cloud_vm_cluster(request)

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


def test_get_cloud_vm_cluster_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vm_cluster.CloudVmCluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cloud_vm_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_cloud_vm_cluster_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cloud_vm_cluster(
            oracledatabase.GetCloudVmClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cloud_vm_cluster_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vm_cluster.CloudVmCluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vm_cluster.CloudVmCluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cloud_vm_cluster(
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
async def test_get_cloud_vm_cluster_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cloud_vm_cluster(
            oracledatabase.GetCloudVmClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateCloudVmClusterRequest,
        dict,
    ],
)
def test_create_cloud_vm_cluster(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cloud_vm_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.CreateCloudVmClusterRequest(
        parent="parent_value",
        cloud_vm_cluster_id="cloud_vm_cluster_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_cloud_vm_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.CreateCloudVmClusterRequest(
            parent="parent_value",
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )


def test_create_cloud_vm_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_cloud_vm_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_cloud_vm_cluster
        ] = mock_rpc
        request = {}
        client.create_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_cloud_vm_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        await client.create_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.CreateCloudVmClusterRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_async_from_dict():
    await test_create_cloud_vm_cluster_async(request_type=dict)


def test_create_cloud_vm_cluster_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateCloudVmClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cloud_vm_cluster(request)

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
async def test_create_cloud_vm_cluster_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateCloudVmClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_cloud_vm_cluster(request)

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


def test_create_cloud_vm_cluster_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cloud_vm_cluster(
            parent="parent_value",
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cloud_vm_cluster
        mock_val = vm_cluster.CloudVmCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].cloud_vm_cluster_id
        mock_val = "cloud_vm_cluster_id_value"
        assert arg == mock_val


def test_create_cloud_vm_cluster_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cloud_vm_cluster(
            oracledatabase.CreateCloudVmClusterRequest(),
            parent="parent_value",
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )


@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cloud_vm_cluster(
            parent="parent_value",
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cloud_vm_cluster
        mock_val = vm_cluster.CloudVmCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].cloud_vm_cluster_id
        mock_val = "cloud_vm_cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cloud_vm_cluster(
            oracledatabase.CreateCloudVmClusterRequest(),
            parent="parent_value",
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteCloudVmClusterRequest,
        dict,
    ],
)
def test_delete_cloud_vm_cluster(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_cloud_vm_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.DeleteCloudVmClusterRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_cloud_vm_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.DeleteCloudVmClusterRequest(
            name="name_value",
        )


def test_delete_cloud_vm_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_cloud_vm_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_cloud_vm_cluster
        ] = mock_rpc
        request = {}
        client.delete_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cloud_vm_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_cloud_vm_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        await client.delete_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cloud_vm_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.DeleteCloudVmClusterRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteCloudVmClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_cloud_vm_cluster_async_from_dict():
    await test_delete_cloud_vm_cluster_async(request_type=dict)


def test_delete_cloud_vm_cluster_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteCloudVmClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_cloud_vm_cluster(request)

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
async def test_delete_cloud_vm_cluster_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteCloudVmClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_cloud_vm_cluster(request)

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


def test_delete_cloud_vm_cluster_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cloud_vm_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_cloud_vm_cluster_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cloud_vm_cluster(
            oracledatabase.DeleteCloudVmClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_cloud_vm_cluster_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cloud_vm_cluster(
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
async def test_delete_cloud_vm_cluster_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cloud_vm_cluster(
            oracledatabase.DeleteCloudVmClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListEntitlementsRequest,
        dict,
    ],
)
def test_list_entitlements(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListEntitlementsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListEntitlementsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntitlementsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_entitlements_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListEntitlementsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_entitlements(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListEntitlementsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_entitlements_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_entitlements in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_entitlements
        ] = mock_rpc
        request = {}
        client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_entitlements(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_entitlements_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_entitlements
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_entitlements
        ] = mock_rpc

        request = {}
        await client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_entitlements(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_entitlements_async(
    transport: str = "grpc_asyncio", request_type=oracledatabase.ListEntitlementsRequest
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListEntitlementsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListEntitlementsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntitlementsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entitlements_async_from_dict():
    await test_list_entitlements_async(request_type=dict)


def test_list_entitlements_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListEntitlementsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListEntitlementsResponse()
        client.list_entitlements(request)

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
async def test_list_entitlements_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListEntitlementsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListEntitlementsResponse()
        )
        await client.list_entitlements(request)

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


def test_list_entitlements_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListEntitlementsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_entitlements(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_entitlements_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entitlements(
            oracledatabase.ListEntitlementsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_entitlements_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListEntitlementsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListEntitlementsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_entitlements(
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
async def test_list_entitlements_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_entitlements(
            oracledatabase.ListEntitlementsRequest(),
            parent="parent_value",
        )


def test_list_entitlements_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[],
                next_page_token="def",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
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
        pager = client.list_entitlements(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, entitlement.Entitlement) for i in results)


def test_list_entitlements_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[],
                next_page_token="def",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_entitlements(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entitlements_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[],
                next_page_token="def",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entitlements(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, entitlement.Entitlement) for i in responses)


@pytest.mark.asyncio
async def test_list_entitlements_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[],
                next_page_token="def",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_entitlements(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbServersRequest,
        dict,
    ],
)
def test_list_db_servers(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbServersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_db_servers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbServersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbServersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_db_servers_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListDbServersRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_db_servers(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListDbServersRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_db_servers_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_db_servers in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_db_servers] = mock_rpc
        request = {}
        client.list_db_servers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_servers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_servers_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_db_servers
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_db_servers
        ] = mock_rpc

        request = {}
        await client.list_db_servers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_db_servers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_servers_async(
    transport: str = "grpc_asyncio", request_type=oracledatabase.ListDbServersRequest
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbServersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_db_servers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbServersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbServersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_db_servers_async_from_dict():
    await test_list_db_servers_async(request_type=dict)


def test_list_db_servers_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbServersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        call.return_value = oracledatabase.ListDbServersResponse()
        client.list_db_servers(request)

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
async def test_list_db_servers_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbServersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbServersResponse()
        )
        await client.list_db_servers(request)

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


def test_list_db_servers_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbServersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_db_servers(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_db_servers_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_servers(
            oracledatabase.ListDbServersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_db_servers_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbServersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbServersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_db_servers(
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
async def test_list_db_servers_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_db_servers(
            oracledatabase.ListDbServersRequest(),
            parent="parent_value",
        )


def test_list_db_servers_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
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
        pager = client.list_db_servers(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_server.DbServer) for i in results)


def test_list_db_servers_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_db_servers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_db_servers_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_servers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_db_servers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, db_server.DbServer) for i in responses)


@pytest.mark.asyncio
async def test_list_db_servers_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_servers), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_db_servers(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbNodesRequest,
        dict,
    ],
)
def test_list_db_nodes(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbNodesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_db_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbNodesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbNodesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_db_nodes_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListDbNodesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_db_nodes(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListDbNodesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_db_nodes_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_db_nodes in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_db_nodes] = mock_rpc
        request = {}
        client.list_db_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_nodes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_nodes_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_db_nodes
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_db_nodes
        ] = mock_rpc

        request = {}
        await client.list_db_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_db_nodes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_nodes_async(
    transport: str = "grpc_asyncio", request_type=oracledatabase.ListDbNodesRequest
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbNodesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_db_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbNodesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbNodesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_db_nodes_async_from_dict():
    await test_list_db_nodes_async(request_type=dict)


def test_list_db_nodes_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbNodesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        call.return_value = oracledatabase.ListDbNodesResponse()
        client.list_db_nodes(request)

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
async def test_list_db_nodes_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbNodesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbNodesResponse()
        )
        await client.list_db_nodes(request)

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


def test_list_db_nodes_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbNodesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_db_nodes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_db_nodes_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_nodes(
            oracledatabase.ListDbNodesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_db_nodes_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbNodesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbNodesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_db_nodes(
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
async def test_list_db_nodes_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_db_nodes(
            oracledatabase.ListDbNodesRequest(),
            parent="parent_value",
        )


def test_list_db_nodes_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
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
        pager = client.list_db_nodes(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_node.DbNode) for i in results)


def test_list_db_nodes_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_db_nodes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_db_nodes_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_nodes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_db_nodes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, db_node.DbNode) for i in responses)


@pytest.mark.asyncio
async def test_list_db_nodes_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_nodes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_db_nodes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListGiVersionsRequest,
        dict,
    ],
)
def test_list_gi_versions(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListGiVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_gi_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListGiVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGiVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_gi_versions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListGiVersionsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_gi_versions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListGiVersionsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_gi_versions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_gi_versions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_gi_versions
        ] = mock_rpc
        request = {}
        client.list_gi_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_gi_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_gi_versions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_gi_versions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_gi_versions
        ] = mock_rpc

        request = {}
        await client.list_gi_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_gi_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_gi_versions_async(
    transport: str = "grpc_asyncio", request_type=oracledatabase.ListGiVersionsRequest
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListGiVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_gi_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListGiVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGiVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_gi_versions_async_from_dict():
    await test_list_gi_versions_async(request_type=dict)


def test_list_gi_versions_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListGiVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        call.return_value = oracledatabase.ListGiVersionsResponse()
        client.list_gi_versions(request)

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
async def test_list_gi_versions_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListGiVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListGiVersionsResponse()
        )
        await client.list_gi_versions(request)

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


def test_list_gi_versions_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListGiVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_gi_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_gi_versions_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_gi_versions(
            oracledatabase.ListGiVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_gi_versions_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListGiVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListGiVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_gi_versions(
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
async def test_list_gi_versions_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_gi_versions(
            oracledatabase.ListGiVersionsRequest(),
            parent="parent_value",
        )


def test_list_gi_versions_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
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
        pager = client.list_gi_versions(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gi_version.GiVersion) for i in results)


def test_list_gi_versions_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_gi_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_gi_versions_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_gi_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_gi_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, gi_version.GiVersion) for i in responses)


@pytest.mark.asyncio
async def test_list_gi_versions_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_gi_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_gi_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbSystemShapesRequest,
        dict,
    ],
)
def test_list_db_system_shapes(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbSystemShapesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_db_system_shapes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbSystemShapesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbSystemShapesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_db_system_shapes_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListDbSystemShapesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_db_system_shapes(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListDbSystemShapesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_db_system_shapes_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_db_system_shapes
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_db_system_shapes
        ] = mock_rpc
        request = {}
        client.list_db_system_shapes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_system_shapes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_system_shapes_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_db_system_shapes
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_db_system_shapes
        ] = mock_rpc

        request = {}
        await client.list_db_system_shapes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_db_system_shapes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_db_system_shapes_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListDbSystemShapesRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbSystemShapesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_db_system_shapes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListDbSystemShapesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbSystemShapesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_db_system_shapes_async_from_dict():
    await test_list_db_system_shapes_async(request_type=dict)


def test_list_db_system_shapes_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbSystemShapesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListDbSystemShapesResponse()
        client.list_db_system_shapes(request)

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
async def test_list_db_system_shapes_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListDbSystemShapesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbSystemShapesResponse()
        )
        await client.list_db_system_shapes(request)

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


def test_list_db_system_shapes_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbSystemShapesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_db_system_shapes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_db_system_shapes_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_system_shapes(
            oracledatabase.ListDbSystemShapesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_db_system_shapes_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListDbSystemShapesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbSystemShapesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_db_system_shapes(
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
async def test_list_db_system_shapes_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_db_system_shapes(
            oracledatabase.ListDbSystemShapesRequest(),
            parent="parent_value",
        )


def test_list_db_system_shapes_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
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
        pager = client.list_db_system_shapes(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_system_shape.DbSystemShape) for i in results)


def test_list_db_system_shapes_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_db_system_shapes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_db_system_shapes_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_db_system_shapes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, db_system_shape.DbSystemShape) for i in responses)


@pytest.mark.asyncio
async def test_list_db_system_shapes_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_db_system_shapes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabasesRequest,
        dict,
    ],
)
def test_list_autonomous_databases(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabasesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_autonomous_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabasesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabasesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_autonomous_databases_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListAutonomousDatabasesRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_autonomous_databases(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListAutonomousDatabasesRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_autonomous_databases_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_databases
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_databases
        ] = mock_rpc
        request = {}
        client.list_autonomous_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_databases(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_databases_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_autonomous_databases
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_autonomous_databases
        ] = mock_rpc

        request = {}
        await client.list_autonomous_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_autonomous_databases(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_databases_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListAutonomousDatabasesRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabasesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_autonomous_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabasesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabasesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_autonomous_databases_async_from_dict():
    await test_list_autonomous_databases_async(request_type=dict)


def test_list_autonomous_databases_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabasesResponse()
        client.list_autonomous_databases(request)

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
async def test_list_autonomous_databases_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabasesResponse()
        )
        await client.list_autonomous_databases(request)

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


def test_list_autonomous_databases_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabasesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_autonomous_databases(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_autonomous_databases_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_databases(
            oracledatabase.ListAutonomousDatabasesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_autonomous_databases_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabasesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabasesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_autonomous_databases(
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
async def test_list_autonomous_databases_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_autonomous_databases(
            oracledatabase.ListAutonomousDatabasesRequest(),
            parent="parent_value",
        )


def test_list_autonomous_databases_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
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
        pager = client.list_autonomous_databases(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_database.AutonomousDatabase) for i in results
        )


def test_list_autonomous_databases_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_autonomous_databases(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_autonomous_databases_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_autonomous_databases(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, autonomous_database.AutonomousDatabase) for i in responses
        )


@pytest.mark.asyncio
async def test_list_autonomous_databases_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_autonomous_databases(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetAutonomousDatabaseRequest,
        dict,
    ],
)
def test_get_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = autonomous_database.AutonomousDatabase(
            name="name_value",
            database="database_value",
            display_name="display_name_value",
            entitlement_id="entitlement_id_value",
            admin_password="admin_password_value",
            network="network_value",
            cidr="cidr_value",
        )
        response = client.get_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, autonomous_database.AutonomousDatabase)
    assert response.name == "name_value"
    assert response.database == "database_value"
    assert response.display_name == "display_name_value"
    assert response.entitlement_id == "entitlement_id_value"
    assert response.admin_password == "admin_password_value"
    assert response.network == "network_value"
    assert response.cidr == "cidr_value"


def test_get_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.GetAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.GetAutonomousDatabaseRequest(
            name="name_value",
        )


def test_get_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_autonomous_database
        ] = mock_rpc
        request = {}
        client.get_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_autonomous_database
        ] = mock_rpc

        request = {}
        await client.get_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.GetAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            autonomous_database.AutonomousDatabase(
                name="name_value",
                database="database_value",
                display_name="display_name_value",
                entitlement_id="entitlement_id_value",
                admin_password="admin_password_value",
                network="network_value",
                cidr="cidr_value",
            )
        )
        response = await client.get_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GetAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, autonomous_database.AutonomousDatabase)
    assert response.name == "name_value"
    assert response.database == "database_value"
    assert response.display_name == "display_name_value"
    assert response.entitlement_id == "entitlement_id_value"
    assert response.admin_password == "admin_password_value"
    assert response.network == "network_value"
    assert response.cidr == "cidr_value"


@pytest.mark.asyncio
async def test_get_autonomous_database_async_from_dict():
    await test_get_autonomous_database_async(request_type=dict)


def test_get_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        call.return_value = autonomous_database.AutonomousDatabase()
        client.get_autonomous_database(request)

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
async def test_get_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GetAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            autonomous_database.AutonomousDatabase()
        )
        await client.get_autonomous_database(request)

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


def test_get_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = autonomous_database.AutonomousDatabase()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_autonomous_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_autonomous_database(
            oracledatabase.GetAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = autonomous_database.AutonomousDatabase()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            autonomous_database.AutonomousDatabase()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_autonomous_database(
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
async def test_get_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_autonomous_database(
            oracledatabase.GetAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateAutonomousDatabaseRequest,
        dict,
    ],
)
def test_create_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.CreateAutonomousDatabaseRequest(
        parent="parent_value",
        autonomous_database_id="autonomous_database_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.CreateAutonomousDatabaseRequest(
            parent="parent_value",
            autonomous_database_id="autonomous_database_id_value",
        )


def test_create_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_autonomous_database
        ] = mock_rpc
        request = {}
        client.create_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_autonomous_database
        ] = mock_rpc

        request = {}
        await client.create_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.CreateAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.CreateAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_autonomous_database_async_from_dict():
    await test_create_autonomous_database_async(request_type=dict)


def test_create_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateAutonomousDatabaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_autonomous_database(request)

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
async def test_create_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.CreateAutonomousDatabaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_autonomous_database(request)

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


def test_create_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_autonomous_database(
            parent="parent_value",
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].autonomous_database
        mock_val = gco_autonomous_database.AutonomousDatabase(name="name_value")
        assert arg == mock_val
        arg = args[0].autonomous_database_id
        mock_val = "autonomous_database_id_value"
        assert arg == mock_val


def test_create_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_autonomous_database(
            oracledatabase.CreateAutonomousDatabaseRequest(),
            parent="parent_value",
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )


@pytest.mark.asyncio
async def test_create_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_autonomous_database(
            parent="parent_value",
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].autonomous_database
        mock_val = gco_autonomous_database.AutonomousDatabase(name="name_value")
        assert arg == mock_val
        arg = args[0].autonomous_database_id
        mock_val = "autonomous_database_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_autonomous_database(
            oracledatabase.CreateAutonomousDatabaseRequest(),
            parent="parent_value",
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteAutonomousDatabaseRequest,
        dict,
    ],
)
def test_delete_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.DeleteAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.DeleteAutonomousDatabaseRequest(
            name="name_value",
        )


def test_delete_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_autonomous_database
        ] = mock_rpc
        request = {}
        client.delete_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_autonomous_database
        ] = mock_rpc

        request = {}
        await client.delete_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.DeleteAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.DeleteAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_autonomous_database_async_from_dict():
    await test_delete_autonomous_database_async(request_type=dict)


def test_delete_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_autonomous_database(request)

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
async def test_delete_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.DeleteAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_autonomous_database(request)

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


def test_delete_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_autonomous_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_autonomous_database(
            oracledatabase.DeleteAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_autonomous_database(
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
async def test_delete_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_autonomous_database(
            oracledatabase.DeleteAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.RestoreAutonomousDatabaseRequest,
        dict,
    ],
)
def test_restore_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restore_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.RestoreAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restore_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.RestoreAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.restore_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.RestoreAutonomousDatabaseRequest(
            name="name_value",
        )


def test_restore_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restore_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restore_autonomous_database
        ] = mock_rpc
        request = {}
        client.restore_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.restore_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restore_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.restore_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.restore_autonomous_database
        ] = mock_rpc

        request = {}
        await client.restore_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.restore_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restore_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.RestoreAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restore_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.RestoreAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restore_autonomous_database_async_from_dict():
    await test_restore_autonomous_database_async(request_type=dict)


def test_restore_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.RestoreAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_autonomous_database(request)

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
async def test_restore_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.RestoreAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restore_autonomous_database(request)

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


def test_restore_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restore_autonomous_database(
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        assert TimestampRule().to_proto(
            args[0].restore_time
        ) == timestamp_pb2.Timestamp(seconds=751)


def test_restore_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_autonomous_database(
            oracledatabase.RestoreAutonomousDatabaseRequest(),
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )


@pytest.mark.asyncio
async def test_restore_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restore_autonomous_database(
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        assert TimestampRule().to_proto(
            args[0].restore_time
        ) == timestamp_pb2.Timestamp(seconds=751)


@pytest.mark.asyncio
async def test_restore_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restore_autonomous_database(
            oracledatabase.RestoreAutonomousDatabaseRequest(),
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        dict,
    ],
)
def test_generate_autonomous_database_wallet(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse(
            archive_content=b"archive_content_blob",
        )
        response = client.generate_autonomous_database_wallet(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GenerateAutonomousDatabaseWalletRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, oracledatabase.GenerateAutonomousDatabaseWalletResponse)
    assert response.archive_content == b"archive_content_blob"


def test_generate_autonomous_database_wallet_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.GenerateAutonomousDatabaseWalletRequest(
        name="name_value",
        password="password_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_autonomous_database_wallet(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.GenerateAutonomousDatabaseWalletRequest(
            name="name_value",
            password="password_value",
        )


def test_generate_autonomous_database_wallet_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_autonomous_database_wallet
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_autonomous_database_wallet
        ] = mock_rpc
        request = {}
        client.generate_autonomous_database_wallet(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_autonomous_database_wallet(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_autonomous_database_wallet
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_autonomous_database_wallet
        ] = mock_rpc

        request = {}
        await client.generate_autonomous_database_wallet(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.generate_autonomous_database_wallet(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.GenerateAutonomousDatabaseWalletRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.GenerateAutonomousDatabaseWalletResponse(
                archive_content=b"archive_content_blob",
            )
        )
        response = await client.generate_autonomous_database_wallet(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.GenerateAutonomousDatabaseWalletRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, oracledatabase.GenerateAutonomousDatabaseWalletResponse)
    assert response.archive_content == b"archive_content_blob"


@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_async_from_dict():
    await test_generate_autonomous_database_wallet_async(request_type=dict)


def test_generate_autonomous_database_wallet_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GenerateAutonomousDatabaseWalletRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        call.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        client.generate_autonomous_database_wallet(request)

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
async def test_generate_autonomous_database_wallet_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.GenerateAutonomousDatabaseWalletRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        )
        await client.generate_autonomous_database_wallet(request)

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


def test_generate_autonomous_database_wallet_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_autonomous_database_wallet(
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].type_
        mock_val = autonomous_database.GenerateType.ALL
        assert arg == mock_val
        arg = args[0].is_regional
        mock_val = True
        assert arg == mock_val
        arg = args[0].password
        mock_val = "password_value"
        assert arg == mock_val


def test_generate_autonomous_database_wallet_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_autonomous_database_wallet(
            oracledatabase.GenerateAutonomousDatabaseWalletRequest(),
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )


@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_autonomous_database_wallet(
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].type_
        mock_val = autonomous_database.GenerateType.ALL
        assert arg == mock_val
        arg = args[0].is_regional
        mock_val = True
        assert arg == mock_val
        arg = args[0].password
        mock_val = "password_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_autonomous_database_wallet(
            oracledatabase.GenerateAutonomousDatabaseWalletRequest(),
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDbVersionsRequest,
        dict,
    ],
)
def test_list_autonomous_db_versions(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDbVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_autonomous_db_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDbVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDbVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_autonomous_db_versions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListAutonomousDbVersionsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_autonomous_db_versions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListAutonomousDbVersionsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_autonomous_db_versions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_db_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_db_versions
        ] = mock_rpc
        request = {}
        client.list_autonomous_db_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_db_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_autonomous_db_versions
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_autonomous_db_versions
        ] = mock_rpc

        request = {}
        await client.list_autonomous_db_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_autonomous_db_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListAutonomousDbVersionsRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDbVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_autonomous_db_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDbVersionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDbVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_async_from_dict():
    await test_list_autonomous_db_versions_async(request_type=dict)


def test_list_autonomous_db_versions_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDbVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDbVersionsResponse()
        client.list_autonomous_db_versions(request)

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
async def test_list_autonomous_db_versions_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDbVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDbVersionsResponse()
        )
        await client.list_autonomous_db_versions(request)

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


def test_list_autonomous_db_versions_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDbVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_autonomous_db_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_autonomous_db_versions_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_db_versions(
            oracledatabase.ListAutonomousDbVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDbVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDbVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_autonomous_db_versions(
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
async def test_list_autonomous_db_versions_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_autonomous_db_versions(
            oracledatabase.ListAutonomousDbVersionsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_db_versions_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
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
        pager = client.list_autonomous_db_versions(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_db_version.AutonomousDbVersion) for i in results
        )


def test_list_autonomous_db_versions_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_autonomous_db_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_autonomous_db_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, autonomous_db_version.AutonomousDbVersion) for i in responses
        )


@pytest.mark.asyncio
async def test_list_autonomous_db_versions_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_autonomous_db_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        dict,
    ],
)
def test_list_autonomous_database_character_sets(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_autonomous_database_character_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseCharacterSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_autonomous_database_character_sets_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_autonomous_database_character_sets(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
        )


def test_list_autonomous_database_character_sets_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_database_character_sets
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_database_character_sets
        ] = mock_rpc
        request = {}
        client.list_autonomous_database_character_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_database_character_sets(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_autonomous_database_character_sets
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_autonomous_database_character_sets
        ] = mock_rpc

        request = {}
        await client.list_autonomous_database_character_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_autonomous_database_character_sets(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_autonomous_database_character_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseCharacterSetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_async_from_dict():
    await test_list_autonomous_database_character_sets_async(request_type=dict)


def test_list_autonomous_database_character_sets_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        client.list_autonomous_database_character_sets(request)

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
async def test_list_autonomous_database_character_sets_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        )
        await client.list_autonomous_database_character_sets(request)

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


def test_list_autonomous_database_character_sets_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_autonomous_database_character_sets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_autonomous_database_character_sets_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_database_character_sets(
            oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_autonomous_database_character_sets(
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
async def test_list_autonomous_database_character_sets_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_autonomous_database_character_sets(
            oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_database_character_sets_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
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
        pager = client.list_autonomous_database_character_sets(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, autonomous_database_character_set.AutonomousDatabaseCharacterSet
            )
            for i in results
        )


def test_list_autonomous_database_character_sets_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_autonomous_database_character_sets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_autonomous_database_character_sets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i, autonomous_database_character_set.AutonomousDatabaseCharacterSet
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_autonomous_database_character_sets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabaseBackupsRequest,
        dict,
    ],
)
def test_list_autonomous_database_backups(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_autonomous_database_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabaseBackupsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseBackupsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_autonomous_database_backups_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.ListAutonomousDatabaseBackupsRequest(
        parent="parent_value",
        filter="filter_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_autonomous_database_backups(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.ListAutonomousDatabaseBackupsRequest(
            parent="parent_value",
            filter="filter_value",
            page_token="page_token_value",
        )


def test_list_autonomous_database_backups_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_database_backups
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_database_backups
        ] = mock_rpc
        request = {}
        client.list_autonomous_database_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_database_backups(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_autonomous_database_backups
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_autonomous_database_backups
        ] = mock_rpc

        request = {}
        await client.list_autonomous_database_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_autonomous_database_backups(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.ListAutonomousDatabaseBackupsRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_autonomous_database_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.ListAutonomousDatabaseBackupsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseBackupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_async_from_dict():
    await test_list_autonomous_database_backups_async(request_type=dict)


def test_list_autonomous_database_backups_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabaseBackupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()
        client.list_autonomous_database_backups(request)

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
async def test_list_autonomous_database_backups_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.ListAutonomousDatabaseBackupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseBackupsResponse()
        )
        await client.list_autonomous_database_backups(request)

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


def test_list_autonomous_database_backups_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_autonomous_database_backups(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_autonomous_database_backups_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_database_backups(
            oracledatabase.ListAutonomousDatabaseBackupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseBackupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_autonomous_database_backups(
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
async def test_list_autonomous_database_backups_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_autonomous_database_backups(
            oracledatabase.ListAutonomousDatabaseBackupsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_database_backups_pager(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
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
        pager = client.list_autonomous_database_backups(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_db_backup.AutonomousDatabaseBackup)
            for i in results
        )


def test_list_autonomous_database_backups_pages(transport_name: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_autonomous_database_backups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_async_pager():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_autonomous_database_backups(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, autonomous_db_backup.AutonomousDatabaseBackup)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_autonomous_database_backups_async_pages():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_autonomous_database_backups(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.StopAutonomousDatabaseRequest,
        dict,
    ],
)
def test_stop_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.stop_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.StopAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_stop_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.StopAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.stop_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.StopAutonomousDatabaseRequest(
            name="name_value",
        )


def test_stop_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.stop_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.stop_autonomous_database
        ] = mock_rpc
        request = {}
        client.stop_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.stop_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_stop_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.stop_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.stop_autonomous_database
        ] = mock_rpc

        request = {}
        await client.stop_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.stop_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_stop_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.StopAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.stop_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.StopAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_stop_autonomous_database_async_from_dict():
    await test_stop_autonomous_database_async(request_type=dict)


def test_stop_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.StopAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.stop_autonomous_database(request)

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
async def test_stop_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.StopAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.stop_autonomous_database(request)

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


def test_stop_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.stop_autonomous_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_stop_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_autonomous_database(
            oracledatabase.StopAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_stop_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.stop_autonomous_database(
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
async def test_stop_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.stop_autonomous_database(
            oracledatabase.StopAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.StartAutonomousDatabaseRequest,
        dict,
    ],
)
def test_start_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.StartAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.StartAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.start_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.StartAutonomousDatabaseRequest(
            name="name_value",
        )


def test_start_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.start_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.start_autonomous_database
        ] = mock_rpc
        request = {}
        client.start_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.start_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_start_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.start_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.start_autonomous_database
        ] = mock_rpc

        request = {}
        await client.start_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.start_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_start_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.StartAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.StartAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_autonomous_database_async_from_dict():
    await test_start_autonomous_database_async(request_type=dict)


def test_start_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.StartAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_autonomous_database(request)

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
async def test_start_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.StartAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_autonomous_database(request)

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


def test_start_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_autonomous_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_start_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_autonomous_database(
            oracledatabase.StartAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_start_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_autonomous_database(
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
async def test_start_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_autonomous_database(
            oracledatabase.StartAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.RestartAutonomousDatabaseRequest,
        dict,
    ],
)
def test_restart_autonomous_database(request_type, transport: str = "grpc"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restart_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.RestartAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restart_autonomous_database_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = oracledatabase.RestartAutonomousDatabaseRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.restart_autonomous_database(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oracledatabase.RestartAutonomousDatabaseRequest(
            name="name_value",
        )


def test_restart_autonomous_database_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restart_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restart_autonomous_database
        ] = mock_rpc
        request = {}
        client.restart_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.restart_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restart_autonomous_database_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OracleDatabaseAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.restart_autonomous_database
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.restart_autonomous_database
        ] = mock_rpc

        request = {}
        await client.restart_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods call wrapper_fn to build a cached
        # client._transport.operations_client instance on first rpc call.
        # Subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.restart_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_restart_autonomous_database_async(
    transport: str = "grpc_asyncio",
    request_type=oracledatabase.RestartAutonomousDatabaseRequest,
):
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restart_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = oracledatabase.RestartAutonomousDatabaseRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restart_autonomous_database_async_from_dict():
    await test_restart_autonomous_database_async(request_type=dict)


def test_restart_autonomous_database_field_headers():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.RestartAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restart_autonomous_database(request)

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
async def test_restart_autonomous_database_field_headers_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oracledatabase.RestartAutonomousDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restart_autonomous_database(request)

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


def test_restart_autonomous_database_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restart_autonomous_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_restart_autonomous_database_flattened_error():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restart_autonomous_database(
            oracledatabase.RestartAutonomousDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_restart_autonomous_database_flattened_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restart_autonomous_database(
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
async def test_restart_autonomous_database_flattened_error_async():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restart_autonomous_database(
            oracledatabase.RestartAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_list_cloud_exadata_infrastructures_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_cloud_exadata_infrastructures
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_cloud_exadata_infrastructures
        ] = mock_rpc

        request = {}
        client.list_cloud_exadata_infrastructures(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_cloud_exadata_infrastructures(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_cloud_exadata_infrastructures_rest_required_fields(
    request_type=oracledatabase.ListCloudExadataInfrastructuresRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_cloud_exadata_infrastructures._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_cloud_exadata_infrastructures._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()
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
            return_value = oracledatabase.ListCloudExadataInfrastructuresResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_cloud_exadata_infrastructures(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_cloud_exadata_infrastructures_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_cloud_exadata_infrastructures._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_cloud_exadata_infrastructures_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()

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
        return_value = oracledatabase.ListCloudExadataInfrastructuresResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_cloud_exadata_infrastructures(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cloudExadataInfrastructures"
            % client.transport._host,
            args[1],
        )


def test_list_cloud_exadata_infrastructures_rest_flattened_error(
    transport: str = "rest",
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cloud_exadata_infrastructures(
            oracledatabase.ListCloudExadataInfrastructuresRequest(),
            parent="parent_value",
        )


def test_list_cloud_exadata_infrastructures_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                cloud_exadata_infrastructures=[
                    exadata_infra.CloudExadataInfrastructure(),
                    exadata_infra.CloudExadataInfrastructure(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListCloudExadataInfrastructuresResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_cloud_exadata_infrastructures(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, exadata_infra.CloudExadataInfrastructure) for i in results
        )

        pages = list(
            client.list_cloud_exadata_infrastructures(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_cloud_exadata_infrastructure_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        client.get_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_cloud_exadata_infrastructure_rest_required_fields(
    request_type=oracledatabase.GetCloudExadataInfrastructureRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).get_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = exadata_infra.CloudExadataInfrastructure()
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
            return_value = exadata_infra.CloudExadataInfrastructure.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_cloud_exadata_infrastructure(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_cloud_exadata_infrastructure_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.get_cloud_exadata_infrastructure._get_unset_required_fields({})
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_cloud_exadata_infrastructure_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = exadata_infra.CloudExadataInfrastructure()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        return_value = exadata_infra.CloudExadataInfrastructure.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_cloud_exadata_infrastructure(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cloudExadataInfrastructures/*}"
            % client.transport._host,
            args[1],
        )


def test_get_cloud_exadata_infrastructure_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cloud_exadata_infrastructure(
            oracledatabase.GetCloudExadataInfrastructureRequest(),
            name="name_value",
        )


def test_create_cloud_exadata_infrastructure_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        client.create_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_cloud_exadata_infrastructure_rest_required_fields(
    request_type=oracledatabase.CreateCloudExadataInfrastructureRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["cloud_exadata_infrastructure_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "cloudExadataInfrastructureId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "cloudExadataInfrastructureId" in jsonified_request
    assert (
        jsonified_request["cloudExadataInfrastructureId"]
        == request_init["cloud_exadata_infrastructure_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request[
        "cloudExadataInfrastructureId"
    ] = "cloud_exadata_infrastructure_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "cloud_exadata_infrastructure_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "cloudExadataInfrastructureId" in jsonified_request
    assert (
        jsonified_request["cloudExadataInfrastructureId"]
        == "cloud_exadata_infrastructure_id_value"
    )

    client = OracleDatabaseClient(
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

            response = client.create_cloud_exadata_infrastructure(request)

            expected_params = [
                (
                    "cloudExadataInfrastructureId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_cloud_exadata_infrastructure_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.create_cloud_exadata_infrastructure._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "cloudExadataInfrastructureId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "cloudExadataInfrastructureId",
                "cloudExadataInfrastructure",
            )
        )
    )


def test_create_cloud_exadata_infrastructure_rest_flattened():
    client = OracleDatabaseClient(
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
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_cloud_exadata_infrastructure(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cloudExadataInfrastructures"
            % client.transport._host,
            args[1],
        )


def test_create_cloud_exadata_infrastructure_rest_flattened_error(
    transport: str = "rest",
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cloud_exadata_infrastructure(
            oracledatabase.CreateCloudExadataInfrastructureRequest(),
            parent="parent_value",
            cloud_exadata_infrastructure=exadata_infra.CloudExadataInfrastructure(
                name="name_value"
            ),
            cloud_exadata_infrastructure_id="cloud_exadata_infrastructure_id_value",
        )


def test_delete_cloud_exadata_infrastructure_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_cloud_exadata_infrastructure
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_cloud_exadata_infrastructure
        ] = mock_rpc

        request = {}
        client.delete_cloud_exadata_infrastructure(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cloud_exadata_infrastructure(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_cloud_exadata_infrastructure_rest_required_fields(
    request_type=oracledatabase.DeleteCloudExadataInfrastructureRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).delete_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_cloud_exadata_infrastructure._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "force",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_cloud_exadata_infrastructure(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_cloud_exadata_infrastructure_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.delete_cloud_exadata_infrastructure._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(
            (
                "force",
                "requestId",
            )
        )
        & set(("name",))
    )


def test_delete_cloud_exadata_infrastructure_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_cloud_exadata_infrastructure(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cloudExadataInfrastructures/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_cloud_exadata_infrastructure_rest_flattened_error(
    transport: str = "rest",
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cloud_exadata_infrastructure(
            oracledatabase.DeleteCloudExadataInfrastructureRequest(),
            name="name_value",
        )


def test_list_cloud_vm_clusters_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_cloud_vm_clusters
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_cloud_vm_clusters
        ] = mock_rpc

        request = {}
        client.list_cloud_vm_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_cloud_vm_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_cloud_vm_clusters_rest_required_fields(
    request_type=oracledatabase.ListCloudVmClustersRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_cloud_vm_clusters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_cloud_vm_clusters._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListCloudVmClustersResponse()
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
            return_value = oracledatabase.ListCloudVmClustersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_cloud_vm_clusters(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_cloud_vm_clusters_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_cloud_vm_clusters._get_unset_required_fields({})
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


def test_list_cloud_vm_clusters_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListCloudVmClustersResponse()

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
        return_value = oracledatabase.ListCloudVmClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_cloud_vm_clusters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cloudVmClusters"
            % client.transport._host,
            args[1],
        )


def test_list_cloud_vm_clusters_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cloud_vm_clusters(
            oracledatabase.ListCloudVmClustersRequest(),
            parent="parent_value",
        )


def test_list_cloud_vm_clusters_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[],
                next_page_token="def",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListCloudVmClustersResponse(
                cloud_vm_clusters=[
                    vm_cluster.CloudVmCluster(),
                    vm_cluster.CloudVmCluster(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListCloudVmClustersResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_cloud_vm_clusters(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, vm_cluster.CloudVmCluster) for i in results)

        pages = list(client.list_cloud_vm_clusters(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_cloud_vm_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_cloud_vm_cluster in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        client.get_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_cloud_vm_cluster_rest_required_fields(
    request_type=oracledatabase.GetCloudVmClusterRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).get_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = vm_cluster.CloudVmCluster()
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
            return_value = vm_cluster.CloudVmCluster.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_cloud_vm_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_cloud_vm_cluster_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_cloud_vm_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_cloud_vm_cluster_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = vm_cluster.CloudVmCluster()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        return_value = vm_cluster.CloudVmCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_cloud_vm_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cloudVmClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_get_cloud_vm_cluster_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cloud_vm_cluster(
            oracledatabase.GetCloudVmClusterRequest(),
            name="name_value",
        )


def test_create_cloud_vm_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_cloud_vm_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        client.create_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_cloud_vm_cluster_rest_required_fields(
    request_type=oracledatabase.CreateCloudVmClusterRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["cloud_vm_cluster_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "cloudVmClusterId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "cloudVmClusterId" in jsonified_request
    assert jsonified_request["cloudVmClusterId"] == request_init["cloud_vm_cluster_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["cloudVmClusterId"] = "cloud_vm_cluster_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "cloud_vm_cluster_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "cloudVmClusterId" in jsonified_request
    assert jsonified_request["cloudVmClusterId"] == "cloud_vm_cluster_id_value"

    client = OracleDatabaseClient(
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

            response = client.create_cloud_vm_cluster(request)

            expected_params = [
                (
                    "cloudVmClusterId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_cloud_vm_cluster_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_cloud_vm_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "cloudVmClusterId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "cloudVmClusterId",
                "cloudVmCluster",
            )
        )
    )


def test_create_cloud_vm_cluster_rest_flattened():
    client = OracleDatabaseClient(
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
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_cloud_vm_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cloudVmClusters"
            % client.transport._host,
            args[1],
        )


def test_create_cloud_vm_cluster_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cloud_vm_cluster(
            oracledatabase.CreateCloudVmClusterRequest(),
            parent="parent_value",
            cloud_vm_cluster=vm_cluster.CloudVmCluster(name="name_value"),
            cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        )


def test_delete_cloud_vm_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_cloud_vm_cluster
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_cloud_vm_cluster
        ] = mock_rpc

        request = {}
        client.delete_cloud_vm_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cloud_vm_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_cloud_vm_cluster_rest_required_fields(
    request_type=oracledatabase.DeleteCloudVmClusterRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).delete_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_cloud_vm_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "force",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_cloud_vm_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_cloud_vm_cluster_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_cloud_vm_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "force",
                "requestId",
            )
        )
        & set(("name",))
    )


def test_delete_cloud_vm_cluster_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_cloud_vm_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cloudVmClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_cloud_vm_cluster_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cloud_vm_cluster(
            oracledatabase.DeleteCloudVmClusterRequest(),
            name="name_value",
        )


def test_list_entitlements_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_entitlements in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_entitlements
        ] = mock_rpc

        request = {}
        client.list_entitlements(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_entitlements(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_entitlements_rest_required_fields(
    request_type=oracledatabase.ListEntitlementsRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_entitlements._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_entitlements._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListEntitlementsResponse()
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
            return_value = oracledatabase.ListEntitlementsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_entitlements(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_entitlements_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_entitlements._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_entitlements_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListEntitlementsResponse()

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
        return_value = oracledatabase.ListEntitlementsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_entitlements(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/entitlements"
            % client.transport._host,
            args[1],
        )


def test_list_entitlements_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entitlements(
            oracledatabase.ListEntitlementsRequest(),
            parent="parent_value",
        )


def test_list_entitlements_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[],
                next_page_token="def",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListEntitlementsResponse(
                entitlements=[
                    entitlement.Entitlement(),
                    entitlement.Entitlement(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListEntitlementsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_entitlements(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, entitlement.Entitlement) for i in results)

        pages = list(client.list_entitlements(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_db_servers_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_db_servers in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_db_servers] = mock_rpc

        request = {}
        client.list_db_servers(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_servers(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_db_servers_rest_required_fields(
    request_type=oracledatabase.ListDbServersRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_db_servers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_db_servers._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListDbServersResponse()
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
            return_value = oracledatabase.ListDbServersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_db_servers(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_db_servers_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_db_servers._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_db_servers_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbServersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        return_value = oracledatabase.ListDbServersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_db_servers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/cloudExadataInfrastructures/*}/dbServers"
            % client.transport._host,
            args[1],
        )


def test_list_db_servers_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_servers(
            oracledatabase.ListDbServersRequest(),
            parent="parent_value",
        )


def test_list_db_servers_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbServersResponse(
                db_servers=[
                    db_server.DbServer(),
                    db_server.DbServer(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListDbServersResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
        }

        pager = client.list_db_servers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_server.DbServer) for i in results)

        pages = list(client.list_db_servers(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_db_nodes_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_db_nodes in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_db_nodes] = mock_rpc

        request = {}
        client.list_db_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_nodes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_db_nodes_rest_required_fields(
    request_type=oracledatabase.ListDbNodesRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_db_nodes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_db_nodes._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListDbNodesResponse()
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
            return_value = oracledatabase.ListDbNodesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_db_nodes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_db_nodes_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_db_nodes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_db_nodes_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbNodesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        return_value = oracledatabase.ListDbNodesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_db_nodes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/cloudVmClusters/*}/dbNodes"
            % client.transport._host,
            args[1],
        )


def test_list_db_nodes_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_nodes(
            oracledatabase.ListDbNodesRequest(),
            parent="parent_value",
        )


def test_list_db_nodes_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbNodesResponse(
                db_nodes=[
                    db_node.DbNode(),
                    db_node.DbNode(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListDbNodesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
        }

        pager = client.list_db_nodes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_node.DbNode) for i in results)

        pages = list(client.list_db_nodes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_gi_versions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_gi_versions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_gi_versions
        ] = mock_rpc

        request = {}
        client.list_gi_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_gi_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_gi_versions_rest_required_fields(
    request_type=oracledatabase.ListGiVersionsRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_gi_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_gi_versions._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListGiVersionsResponse()
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
            return_value = oracledatabase.ListGiVersionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_gi_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_gi_versions_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_gi_versions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_gi_versions_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListGiVersionsResponse()

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
        return_value = oracledatabase.ListGiVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_gi_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/giVersions" % client.transport._host,
            args[1],
        )


def test_list_gi_versions_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_gi_versions(
            oracledatabase.ListGiVersionsRequest(),
            parent="parent_value",
        )


def test_list_gi_versions_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListGiVersionsResponse(
                gi_versions=[
                    gi_version.GiVersion(),
                    gi_version.GiVersion(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListGiVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_gi_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, gi_version.GiVersion) for i in results)

        pages = list(client.list_gi_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_db_system_shapes_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_db_system_shapes
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_db_system_shapes
        ] = mock_rpc

        request = {}
        client.list_db_system_shapes(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_db_system_shapes(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_db_system_shapes_rest_required_fields(
    request_type=oracledatabase.ListDbSystemShapesRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_db_system_shapes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_db_system_shapes._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListDbSystemShapesResponse()
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
            return_value = oracledatabase.ListDbSystemShapesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_db_system_shapes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_db_system_shapes_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_db_system_shapes._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_db_system_shapes_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbSystemShapesResponse()

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
        return_value = oracledatabase.ListDbSystemShapesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_db_system_shapes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/dbSystemShapes"
            % client.transport._host,
            args[1],
        )


def test_list_db_system_shapes_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_db_system_shapes(
            oracledatabase.ListDbSystemShapesRequest(),
            parent="parent_value",
        )


def test_list_db_system_shapes_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[],
                next_page_token="def",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListDbSystemShapesResponse(
                db_system_shapes=[
                    db_system_shape.DbSystemShape(),
                    db_system_shape.DbSystemShape(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListDbSystemShapesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_db_system_shapes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, db_system_shape.DbSystemShape) for i in results)

        pages = list(client.list_db_system_shapes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_autonomous_databases_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_databases
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_databases
        ] = mock_rpc

        request = {}
        client.list_autonomous_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_databases(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_autonomous_databases_rest_required_fields(
    request_type=oracledatabase.ListAutonomousDatabasesRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_autonomous_databases._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_autonomous_databases._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListAutonomousDatabasesResponse()
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
            return_value = oracledatabase.ListAutonomousDatabasesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_autonomous_databases(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_autonomous_databases_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_autonomous_databases._get_unset_required_fields({})
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


def test_list_autonomous_databases_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabasesResponse()

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
        return_value = oracledatabase.ListAutonomousDatabasesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_autonomous_databases(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/autonomousDatabases"
            % client.transport._host,
            args[1],
        )


def test_list_autonomous_databases_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_databases(
            oracledatabase.ListAutonomousDatabasesRequest(),
            parent="parent_value",
        )


def test_list_autonomous_databases_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabasesResponse(
                autonomous_databases=[
                    autonomous_database.AutonomousDatabase(),
                    autonomous_database.AutonomousDatabase(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListAutonomousDatabasesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_autonomous_databases(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_database.AutonomousDatabase) for i in results
        )

        pages = list(client.list_autonomous_databases(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_autonomous_database
        ] = mock_rpc

        request = {}
        client.get_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_autonomous_database_rest_required_fields(
    request_type=oracledatabase.GetAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).get_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = autonomous_database.AutonomousDatabase()
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
            return_value = autonomous_database.AutonomousDatabase.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = autonomous_database.AutonomousDatabase()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        return_value = autonomous_database.AutonomousDatabase.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}"
            % client.transport._host,
            args[1],
        )


def test_get_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_autonomous_database(
            oracledatabase.GetAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_create_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_autonomous_database
        ] = mock_rpc

        request = {}
        client.create_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_autonomous_database_rest_required_fields(
    request_type=oracledatabase.CreateAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["autonomous_database_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "autonomousDatabaseId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "autonomousDatabaseId" in jsonified_request
    assert (
        jsonified_request["autonomousDatabaseId"]
        == request_init["autonomous_database_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["autonomousDatabaseId"] = "autonomous_database_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_autonomous_database._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "autonomous_database_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "autonomousDatabaseId" in jsonified_request
    assert jsonified_request["autonomousDatabaseId"] == "autonomous_database_id_value"

    client = OracleDatabaseClient(
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

            response = client.create_autonomous_database(request)

            expected_params = [
                (
                    "autonomousDatabaseId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "autonomousDatabaseId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "autonomousDatabaseId",
                "autonomousDatabase",
            )
        )
    )


def test_create_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
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
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/autonomousDatabases"
            % client.transport._host,
            args[1],
        )


def test_create_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_autonomous_database(
            oracledatabase.CreateAutonomousDatabaseRequest(),
            parent="parent_value",
            autonomous_database=gco_autonomous_database.AutonomousDatabase(
                name="name_value"
            ),
            autonomous_database_id="autonomous_database_id_value",
        )


def test_delete_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_autonomous_database
        ] = mock_rpc

        request = {}
        client.delete_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_autonomous_database_rest_required_fields(
    request_type=oracledatabase.DeleteAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).delete_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_autonomous_database._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.delete_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


def test_delete_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.delete_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_autonomous_database(
            oracledatabase.DeleteAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_restore_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restore_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restore_autonomous_database
        ] = mock_rpc

        request = {}
        client.restore_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.restore_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_restore_autonomous_database_rest_required_fields(
    request_type=oracledatabase.RestoreAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).restore_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).restore_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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

            response = client.restore_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_restore_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.restore_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "restoreTime",
            )
        )
    )


def test_restore_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.restore_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}:restore"
            % client.transport._host,
            args[1],
        )


def test_restore_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_autonomous_database(
            oracledatabase.RestoreAutonomousDatabaseRequest(),
            name="name_value",
            restore_time=timestamp_pb2.Timestamp(seconds=751),
        )


def test_generate_autonomous_database_wallet_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_autonomous_database_wallet
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_autonomous_database_wallet
        ] = mock_rpc

        request = {}
        client.generate_autonomous_database_wallet(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_autonomous_database_wallet(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_autonomous_database_wallet_rest_required_fields(
    request_type=oracledatabase.GenerateAutonomousDatabaseWalletRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["password"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_autonomous_database_wallet._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["password"] = "password_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_autonomous_database_wallet._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "password" in jsonified_request
    assert jsonified_request["password"] == "password_value"

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
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
            return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.generate_autonomous_database_wallet(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_generate_autonomous_database_wallet_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.generate_autonomous_database_wallet._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "password",
            )
        )
    )


def test_generate_autonomous_database_wallet_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.generate_autonomous_database_wallet(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}:generateWallet"
            % client.transport._host,
            args[1],
        )


def test_generate_autonomous_database_wallet_rest_flattened_error(
    transport: str = "rest",
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_autonomous_database_wallet(
            oracledatabase.GenerateAutonomousDatabaseWalletRequest(),
            name="name_value",
            type_=autonomous_database.GenerateType.ALL,
            is_regional=True,
            password="password_value",
        )


def test_list_autonomous_db_versions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_db_versions
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_db_versions
        ] = mock_rpc

        request = {}
        client.list_autonomous_db_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_db_versions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_autonomous_db_versions_rest_required_fields(
    request_type=oracledatabase.ListAutonomousDbVersionsRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_autonomous_db_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_autonomous_db_versions._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListAutonomousDbVersionsResponse()
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
            return_value = oracledatabase.ListAutonomousDbVersionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_autonomous_db_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_autonomous_db_versions_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_autonomous_db_versions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_autonomous_db_versions_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDbVersionsResponse()

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
        return_value = oracledatabase.ListAutonomousDbVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_autonomous_db_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/autonomousDbVersions"
            % client.transport._host,
            args[1],
        )


def test_list_autonomous_db_versions_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_db_versions(
            oracledatabase.ListAutonomousDbVersionsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_db_versions_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDbVersionsResponse(
                autonomous_db_versions=[
                    autonomous_db_version.AutonomousDbVersion(),
                    autonomous_db_version.AutonomousDbVersion(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListAutonomousDbVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_autonomous_db_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_db_version.AutonomousDbVersion) for i in results
        )

        pages = list(client.list_autonomous_db_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_autonomous_database_character_sets_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_database_character_sets
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_database_character_sets
        ] = mock_rpc

        request = {}
        client.list_autonomous_database_character_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_database_character_sets(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_autonomous_database_character_sets_rest_required_fields(
    request_type=oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_autonomous_database_character_sets._get_unset_required_fields(
        jsonified_request
    )
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_autonomous_database_character_sets._get_unset_required_fields(
        jsonified_request
    )
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
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
                oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_autonomous_database_character_sets(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_autonomous_database_character_sets_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_autonomous_database_character_sets._get_unset_required_fields({})
    )
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


def test_list_autonomous_database_character_sets_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()

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
        return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_autonomous_database_character_sets(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/autonomousDatabaseCharacterSets"
            % client.transport._host,
            args[1],
        )


def test_list_autonomous_database_character_sets_rest_flattened_error(
    transport: str = "rest",
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_database_character_sets(
            oracledatabase.ListAutonomousDatabaseCharacterSetsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_database_character_sets_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                autonomous_database_character_sets=[
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                    autonomous_database_character_set.AutonomousDatabaseCharacterSet(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_autonomous_database_character_sets(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, autonomous_database_character_set.AutonomousDatabaseCharacterSet
            )
            for i in results
        )

        pages = list(
            client.list_autonomous_database_character_sets(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_autonomous_database_backups_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_autonomous_database_backups
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_autonomous_database_backups
        ] = mock_rpc

        request = {}
        client.list_autonomous_database_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_autonomous_database_backups(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_autonomous_database_backups_rest_required_fields(
    request_type=oracledatabase.ListAutonomousDatabaseBackupsRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).list_autonomous_database_backups._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_autonomous_database_backups._get_unset_required_fields(jsonified_request)
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

    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()
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
            return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_autonomous_database_backups(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_autonomous_database_backups_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_autonomous_database_backups._get_unset_required_fields({})
    )
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


def test_list_autonomous_database_backups_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()

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
        return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_autonomous_database_backups(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/autonomousDatabaseBackups"
            % client.transport._host,
            args[1],
        )


def test_list_autonomous_database_backups_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_autonomous_database_backups(
            oracledatabase.ListAutonomousDatabaseBackupsRequest(),
            parent="parent_value",
        )


def test_list_autonomous_database_backups_rest_pager(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="abc",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[],
                next_page_token="def",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
                next_page_token="ghi",
            ),
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                autonomous_database_backups=[
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                    autonomous_db_backup.AutonomousDatabaseBackup(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            oracledatabase.ListAutonomousDatabaseBackupsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_autonomous_database_backups(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, autonomous_db_backup.AutonomousDatabaseBackup)
            for i in results
        )

        pages = list(
            client.list_autonomous_database_backups(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_stop_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.stop_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.stop_autonomous_database
        ] = mock_rpc

        request = {}
        client.stop_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.stop_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_stop_autonomous_database_rest_required_fields(
    request_type=oracledatabase.StopAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).stop_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).stop_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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

            response = client.stop_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_stop_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.stop_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_stop_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.stop_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}:stop"
            % client.transport._host,
            args[1],
        )


def test_stop_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_autonomous_database(
            oracledatabase.StopAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_start_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.start_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.start_autonomous_database
        ] = mock_rpc

        request = {}
        client.start_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.start_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_start_autonomous_database_rest_required_fields(
    request_type=oracledatabase.StartAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).start_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).start_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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

            response = client.start_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_start_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.start_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_start_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.start_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}:start"
            % client.transport._host,
            args[1],
        )


def test_start_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_autonomous_database(
            oracledatabase.StartAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_restart_autonomous_database_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.restart_autonomous_database
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.restart_autonomous_database
        ] = mock_rpc

        request = {}
        client.restart_autonomous_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.restart_autonomous_database(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_restart_autonomous_database_rest_required_fields(
    request_type=oracledatabase.RestartAutonomousDatabaseRequest,
):
    transport_class = transports.OracleDatabaseRestTransport

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
    ).restart_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).restart_autonomous_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OracleDatabaseClient(
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

            response = client.restart_autonomous_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_restart_autonomous_database_rest_unset_required_fields():
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.restart_autonomous_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_restart_autonomous_database_rest_flattened():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.restart_autonomous_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/autonomousDatabases/*}:restart"
            % client.transport._host,
            args[1],
        )


def test_restart_autonomous_database_rest_flattened_error(transport: str = "rest"):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restart_autonomous_database(
            oracledatabase.RestartAutonomousDatabaseRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OracleDatabaseClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OracleDatabaseClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OracleDatabaseClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OracleDatabaseClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OracleDatabaseClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OracleDatabaseGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OracleDatabaseGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
        transports.OracleDatabaseRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = OracleDatabaseClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_cloud_exadata_infrastructures_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()
        client.list_cloud_exadata_infrastructures(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudExadataInfrastructuresRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_cloud_exadata_infrastructure_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = exadata_infra.CloudExadataInfrastructure()
        client.get_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_cloud_exadata_infrastructure_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_cloud_exadata_infrastructure_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_cloud_vm_clusters_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListCloudVmClustersResponse()
        client.list_cloud_vm_clusters(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudVmClustersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_cloud_vm_cluster_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = vm_cluster.CloudVmCluster()
        client.get_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_cloud_vm_cluster_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_cloud_vm_cluster_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_entitlements_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListEntitlementsResponse()
        client.list_entitlements(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListEntitlementsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_servers_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        call.return_value = oracledatabase.ListDbServersResponse()
        client.list_db_servers(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbServersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_nodes_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        call.return_value = oracledatabase.ListDbNodesResponse()
        client.list_db_nodes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbNodesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_gi_versions_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        call.return_value = oracledatabase.ListGiVersionsResponse()
        client.list_gi_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListGiVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_system_shapes_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListDbSystemShapesResponse()
        client.list_db_system_shapes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbSystemShapesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_databases_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabasesResponse()
        client.list_autonomous_databases(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabasesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        call.return_value = autonomous_database.AutonomousDatabase()
        client.get_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restore_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestoreAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_generate_autonomous_database_wallet_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        call.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        client.generate_autonomous_database_wallet(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GenerateAutonomousDatabaseWalletRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_db_versions_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDbVersionsResponse()
        client.list_autonomous_db_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDbVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_database_character_sets_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        client.list_autonomous_database_character_sets(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_database_backups_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        call.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()
        client.list_autonomous_database_backups(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseBackupsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_stop_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.stop_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StopAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_start_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StartAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restart_autonomous_database_empty_call_grpc():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restart_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestartAutonomousDatabaseRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = OracleDatabaseAsyncClient.get_transport_class("grpc_asyncio")(
        credentials=async_anonymous_credentials()
    )
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_cloud_exadata_infrastructures_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudExadataInfrastructuresResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_cloud_exadata_infrastructures(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudExadataInfrastructuresRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_cloud_exadata_infrastructure_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            exadata_infra.CloudExadataInfrastructure(
                name="name_value",
                display_name="display_name_value",
                gcp_oracle_zone="gcp_oracle_zone_value",
                entitlement_id="entitlement_id_value",
            )
        )
        await client.get_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_cloud_exadata_infrastructure_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_cloud_exadata_infrastructure_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.delete_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_cloud_vm_clusters_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListCloudVmClustersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_cloud_vm_clusters(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudVmClustersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_cloud_vm_cluster_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vm_cluster.CloudVmCluster(
                name="name_value",
                exadata_infrastructure="exadata_infrastructure_value",
                display_name="display_name_value",
                gcp_oracle_zone="gcp_oracle_zone_value",
                cidr="cidr_value",
                backup_subnet_cidr="backup_subnet_cidr_value",
                network="network_value",
            )
        )
        await client.get_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_cloud_vm_cluster_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_cloud_vm_cluster_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.delete_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_entitlements_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListEntitlementsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_entitlements(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListEntitlementsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_db_servers_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbServersResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_db_servers(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbServersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_db_nodes_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbNodesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_db_nodes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbNodesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_gi_versions_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListGiVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_gi_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListGiVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_db_system_shapes_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListDbSystemShapesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_db_system_shapes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbSystemShapesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_autonomous_databases_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabasesResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_autonomous_databases(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabasesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            autonomous_database.AutonomousDatabase(
                name="name_value",
                database="database_value",
                display_name="display_name_value",
                entitlement_id="entitlement_id_value",
                admin_password="admin_password_value",
                network="network_value",
                cidr="cidr_value",
            )
        )
        await client.get_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.create_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_delete_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.delete_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_restore_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.restore_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestoreAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_generate_autonomous_database_wallet_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.GenerateAutonomousDatabaseWalletResponse(
                archive_content=b"archive_content_blob",
            )
        )
        await client.generate_autonomous_database_wallet(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GenerateAutonomousDatabaseWalletRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_autonomous_db_versions_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDbVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_autonomous_db_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDbVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_autonomous_database_character_sets_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_autonomous_database_character_sets(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_autonomous_database_backups_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oracledatabase.ListAutonomousDatabaseBackupsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_autonomous_database_backups(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseBackupsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_stop_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.stop_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StopAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_start_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.start_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StartAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_restart_autonomous_database_empty_call_grpc_asyncio():
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        await client.restart_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestartAutonomousDatabaseRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = OracleDatabaseClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_list_cloud_exadata_infrastructures_rest_bad_request(
    request_type=oracledatabase.ListCloudExadataInfrastructuresRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_cloud_exadata_infrastructures(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListCloudExadataInfrastructuresRequest,
        dict,
    ],
)
def test_list_cloud_exadata_infrastructures_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListCloudExadataInfrastructuresResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListCloudExadataInfrastructuresResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_cloud_exadata_infrastructures(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudExadataInfrastructuresPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_cloud_exadata_infrastructures_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_cloud_exadata_infrastructures",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_cloud_exadata_infrastructures_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "pre_list_cloud_exadata_infrastructures",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListCloudExadataInfrastructuresRequest.pb(
            oracledatabase.ListCloudExadataInfrastructuresRequest()
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
        return_value = oracledatabase.ListCloudExadataInfrastructuresResponse.to_json(
            oracledatabase.ListCloudExadataInfrastructuresResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListCloudExadataInfrastructuresRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListCloudExadataInfrastructuresResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListCloudExadataInfrastructuresResponse(),
            metadata,
        )

        client.list_cloud_exadata_infrastructures(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_cloud_exadata_infrastructure_rest_bad_request(
    request_type=oracledatabase.GetCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        client.get_cloud_exadata_infrastructure(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_get_cloud_exadata_infrastructure_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = exadata_infra.CloudExadataInfrastructure(
            name="name_value",
            display_name="display_name_value",
            gcp_oracle_zone="gcp_oracle_zone_value",
            entitlement_id="entitlement_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = exadata_infra.CloudExadataInfrastructure.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_cloud_exadata_infrastructure(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, exadata_infra.CloudExadataInfrastructure)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.entitlement_id == "entitlement_id_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_cloud_exadata_infrastructure_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_get_cloud_exadata_infrastructure",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_get_cloud_exadata_infrastructure_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_get_cloud_exadata_infrastructure"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.GetCloudExadataInfrastructureRequest.pb(
            oracledatabase.GetCloudExadataInfrastructureRequest()
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
        return_value = exadata_infra.CloudExadataInfrastructure.to_json(
            exadata_infra.CloudExadataInfrastructure()
        )
        req.return_value.content = return_value

        request = oracledatabase.GetCloudExadataInfrastructureRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = exadata_infra.CloudExadataInfrastructure()
        post_with_metadata.return_value = (
            exadata_infra.CloudExadataInfrastructure(),
            metadata,
        )

        client.get_cloud_exadata_infrastructure(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_cloud_exadata_infrastructure_rest_bad_request(
    request_type=oracledatabase.CreateCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_cloud_exadata_infrastructure(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_create_cloud_exadata_infrastructure_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["cloud_exadata_infrastructure"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "gcp_oracle_zone": "gcp_oracle_zone_value",
        "entitlement_id": "entitlement_id_value",
        "properties": {
            "ocid": "ocid_value",
            "compute_count": 1413,
            "storage_count": 1405,
            "total_storage_size_gb": 2234,
            "available_storage_size_gb": 2615,
            "maintenance_window": {
                "preference": 1,
                "months": [1],
                "weeks_of_month": [1497, 1498],
                "days_of_week": [1],
                "hours_of_day": [1283, 1284],
                "lead_time_week": 1455,
                "patching_mode": 1,
                "custom_action_timeout_mins": 2804,
                "is_custom_action_timeout_enabled": True,
            },
            "state": 1,
            "shape": "shape_value",
            "oci_url": "oci_url_value",
            "cpu_count": 976,
            "max_cpu_count": 1397,
            "memory_size_gb": 1499,
            "max_memory_gb": 1382,
            "db_node_storage_size_gb": 2401,
            "max_db_node_storage_size_gb": 2822,
            "data_storage_size_tb": 0.2109,
            "max_data_storage_tb": 0.19920000000000002,
            "activated_storage_count": 2449,
            "additional_storage_count": 2549,
            "db_server_version": "db_server_version_value",
            "storage_server_version": "storage_server_version_value",
            "next_maintenance_run_id": "next_maintenance_run_id_value",
            "next_maintenance_run_time": {"seconds": 751, "nanos": 543},
            "next_security_maintenance_run_time": {},
            "customer_contacts": [{"email": "email_value"}],
            "monthly_storage_server_version": "monthly_storage_server_version_value",
            "monthly_db_server_version": "monthly_db_server_version_value",
        },
        "labels": {},
        "create_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = oracledatabase.CreateCloudExadataInfrastructureRequest.meta.fields[
        "cloud_exadata_infrastructure"
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
    for field, value in request_init[
        "cloud_exadata_infrastructure"
    ].items():  # pragma: NO COVER
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
                for i in range(
                    0, len(request_init["cloud_exadata_infrastructure"][field])
                ):
                    del request_init["cloud_exadata_infrastructure"][field][i][subfield]
            else:
                del request_init["cloud_exadata_infrastructure"][field][subfield]
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
        response = client.create_cloud_exadata_infrastructure(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_cloud_exadata_infrastructure_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_create_cloud_exadata_infrastructure",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_create_cloud_exadata_infrastructure_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "pre_create_cloud_exadata_infrastructure",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.CreateCloudExadataInfrastructureRequest.pb(
            oracledatabase.CreateCloudExadataInfrastructureRequest()
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

        request = oracledatabase.CreateCloudExadataInfrastructureRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.create_cloud_exadata_infrastructure(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_cloud_exadata_infrastructure_rest_bad_request(
    request_type=oracledatabase.DeleteCloudExadataInfrastructureRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        client.delete_cloud_exadata_infrastructure(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteCloudExadataInfrastructureRequest,
        dict,
    ],
)
def test_delete_cloud_exadata_infrastructure_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        response = client.delete_cloud_exadata_infrastructure(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_cloud_exadata_infrastructure_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_delete_cloud_exadata_infrastructure",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_delete_cloud_exadata_infrastructure_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "pre_delete_cloud_exadata_infrastructure",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.DeleteCloudExadataInfrastructureRequest.pb(
            oracledatabase.DeleteCloudExadataInfrastructureRequest()
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

        request = oracledatabase.DeleteCloudExadataInfrastructureRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.delete_cloud_exadata_infrastructure(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_cloud_vm_clusters_rest_bad_request(
    request_type=oracledatabase.ListCloudVmClustersRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_cloud_vm_clusters(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListCloudVmClustersRequest,
        dict,
    ],
)
def test_list_cloud_vm_clusters_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListCloudVmClustersResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListCloudVmClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_cloud_vm_clusters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloudVmClustersPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_cloud_vm_clusters_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_cloud_vm_clusters"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_cloud_vm_clusters_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_cloud_vm_clusters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListCloudVmClustersRequest.pb(
            oracledatabase.ListCloudVmClustersRequest()
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
        return_value = oracledatabase.ListCloudVmClustersResponse.to_json(
            oracledatabase.ListCloudVmClustersResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListCloudVmClustersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListCloudVmClustersResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListCloudVmClustersResponse(),
            metadata,
        )

        client.list_cloud_vm_clusters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_cloud_vm_cluster_rest_bad_request(
    request_type=oracledatabase.GetCloudVmClusterRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        client.get_cloud_vm_cluster(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetCloudVmClusterRequest,
        dict,
    ],
)
def test_get_cloud_vm_cluster_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = vm_cluster.CloudVmCluster(
            name="name_value",
            exadata_infrastructure="exadata_infrastructure_value",
            display_name="display_name_value",
            gcp_oracle_zone="gcp_oracle_zone_value",
            cidr="cidr_value",
            backup_subnet_cidr="backup_subnet_cidr_value",
            network="network_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = vm_cluster.CloudVmCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_cloud_vm_cluster(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, vm_cluster.CloudVmCluster)
    assert response.name == "name_value"
    assert response.exadata_infrastructure == "exadata_infrastructure_value"
    assert response.display_name == "display_name_value"
    assert response.gcp_oracle_zone == "gcp_oracle_zone_value"
    assert response.cidr == "cidr_value"
    assert response.backup_subnet_cidr == "backup_subnet_cidr_value"
    assert response.network == "network_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_cloud_vm_cluster_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_get_cloud_vm_cluster"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_get_cloud_vm_cluster_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_get_cloud_vm_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.GetCloudVmClusterRequest.pb(
            oracledatabase.GetCloudVmClusterRequest()
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
        return_value = vm_cluster.CloudVmCluster.to_json(vm_cluster.CloudVmCluster())
        req.return_value.content = return_value

        request = oracledatabase.GetCloudVmClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = vm_cluster.CloudVmCluster()
        post_with_metadata.return_value = vm_cluster.CloudVmCluster(), metadata

        client.get_cloud_vm_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_cloud_vm_cluster_rest_bad_request(
    request_type=oracledatabase.CreateCloudVmClusterRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_cloud_vm_cluster(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateCloudVmClusterRequest,
        dict,
    ],
)
def test_create_cloud_vm_cluster_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["cloud_vm_cluster"] = {
        "name": "name_value",
        "exadata_infrastructure": "exadata_infrastructure_value",
        "display_name": "display_name_value",
        "gcp_oracle_zone": "gcp_oracle_zone_value",
        "properties": {
            "ocid": "ocid_value",
            "license_type": 1,
            "gi_version": "gi_version_value",
            "time_zone": {"id": "id_value", "version": "version_value"},
            "ssh_public_keys": ["ssh_public_keys_value1", "ssh_public_keys_value2"],
            "node_count": 1070,
            "shape": "shape_value",
            "ocpu_count": 0.1087,
            "memory_size_gb": 1499,
            "db_node_storage_size_gb": 2401,
            "storage_size_gb": 1591,
            "data_storage_size_tb": 0.2109,
            "disk_redundancy": 1,
            "sparse_diskgroup_enabled": True,
            "local_backup_enabled": True,
            "hostname_prefix": "hostname_prefix_value",
            "diagnostics_data_collection_options": {
                "diagnostics_events_enabled": True,
                "health_monitoring_enabled": True,
                "incident_logs_enabled": True,
            },
            "state": 1,
            "scan_listener_port_tcp": 2356,
            "scan_listener_port_tcp_ssl": 2789,
            "domain": "domain_value",
            "scan_dns": "scan_dns_value",
            "hostname": "hostname_value",
            "cpu_core_count": 1496,
            "system_version": "system_version_value",
            "scan_ip_ids": ["scan_ip_ids_value1", "scan_ip_ids_value2"],
            "scan_dns_record_id": "scan_dns_record_id_value",
            "oci_url": "oci_url_value",
            "db_server_ocids": ["db_server_ocids_value1", "db_server_ocids_value2"],
            "compartment_id": "compartment_id_value",
            "dns_listener_ip": "dns_listener_ip_value",
            "cluster_name": "cluster_name_value",
        },
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "cidr": "cidr_value",
        "backup_subnet_cidr": "backup_subnet_cidr_value",
        "network": "network_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = oracledatabase.CreateCloudVmClusterRequest.meta.fields[
        "cloud_vm_cluster"
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
    for field, value in request_init["cloud_vm_cluster"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["cloud_vm_cluster"][field])):
                    del request_init["cloud_vm_cluster"][field][i][subfield]
            else:
                del request_init["cloud_vm_cluster"][field][subfield]
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
        response = client.create_cloud_vm_cluster(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_cloud_vm_cluster_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_create_cloud_vm_cluster"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_create_cloud_vm_cluster_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_create_cloud_vm_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.CreateCloudVmClusterRequest.pb(
            oracledatabase.CreateCloudVmClusterRequest()
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

        request = oracledatabase.CreateCloudVmClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.create_cloud_vm_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_cloud_vm_cluster_rest_bad_request(
    request_type=oracledatabase.DeleteCloudVmClusterRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        client.delete_cloud_vm_cluster(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteCloudVmClusterRequest,
        dict,
    ],
)
def test_delete_cloud_vm_cluster_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        response = client.delete_cloud_vm_cluster(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_cloud_vm_cluster_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_delete_cloud_vm_cluster"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_delete_cloud_vm_cluster_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_delete_cloud_vm_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.DeleteCloudVmClusterRequest.pb(
            oracledatabase.DeleteCloudVmClusterRequest()
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

        request = oracledatabase.DeleteCloudVmClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.delete_cloud_vm_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_entitlements_rest_bad_request(
    request_type=oracledatabase.ListEntitlementsRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_entitlements(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListEntitlementsRequest,
        dict,
    ],
)
def test_list_entitlements_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListEntitlementsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListEntitlementsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_entitlements(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntitlementsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_entitlements_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_entitlements"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_entitlements_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_entitlements"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListEntitlementsRequest.pb(
            oracledatabase.ListEntitlementsRequest()
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
        return_value = oracledatabase.ListEntitlementsResponse.to_json(
            oracledatabase.ListEntitlementsResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListEntitlementsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListEntitlementsResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListEntitlementsResponse(),
            metadata,
        )

        client.list_entitlements(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_db_servers_rest_bad_request(
    request_type=oracledatabase.ListDbServersRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
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
        client.list_db_servers(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbServersRequest,
        dict,
    ],
)
def test_list_db_servers_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/cloudExadataInfrastructures/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbServersResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListDbServersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_db_servers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbServersPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_db_servers_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_db_servers"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_db_servers_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_db_servers"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListDbServersRequest.pb(
            oracledatabase.ListDbServersRequest()
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
        return_value = oracledatabase.ListDbServersResponse.to_json(
            oracledatabase.ListDbServersResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListDbServersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListDbServersResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListDbServersResponse(),
            metadata,
        )

        client.list_db_servers(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_db_nodes_rest_bad_request(request_type=oracledatabase.ListDbNodesRequest):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
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
        client.list_db_nodes(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbNodesRequest,
        dict,
    ],
)
def test_list_db_nodes_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/cloudVmClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbNodesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListDbNodesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_db_nodes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbNodesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_db_nodes_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_db_nodes"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_db_nodes_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_db_nodes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListDbNodesRequest.pb(
            oracledatabase.ListDbNodesRequest()
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
        return_value = oracledatabase.ListDbNodesResponse.to_json(
            oracledatabase.ListDbNodesResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListDbNodesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListDbNodesResponse()
        post_with_metadata.return_value = oracledatabase.ListDbNodesResponse(), metadata

        client.list_db_nodes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_gi_versions_rest_bad_request(
    request_type=oracledatabase.ListGiVersionsRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_gi_versions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListGiVersionsRequest,
        dict,
    ],
)
def test_list_gi_versions_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListGiVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListGiVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_gi_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGiVersionsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_gi_versions_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_gi_versions"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_gi_versions_with_metadata"
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_gi_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListGiVersionsRequest.pb(
            oracledatabase.ListGiVersionsRequest()
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
        return_value = oracledatabase.ListGiVersionsResponse.to_json(
            oracledatabase.ListGiVersionsResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListGiVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListGiVersionsResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListGiVersionsResponse(),
            metadata,
        )

        client.list_gi_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_db_system_shapes_rest_bad_request(
    request_type=oracledatabase.ListDbSystemShapesRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_db_system_shapes(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListDbSystemShapesRequest,
        dict,
    ],
)
def test_list_db_system_shapes_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListDbSystemShapesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListDbSystemShapesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_db_system_shapes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDbSystemShapesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_db_system_shapes_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_db_system_shapes"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_db_system_shapes_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_db_system_shapes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListDbSystemShapesRequest.pb(
            oracledatabase.ListDbSystemShapesRequest()
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
        return_value = oracledatabase.ListDbSystemShapesResponse.to_json(
            oracledatabase.ListDbSystemShapesResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListDbSystemShapesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListDbSystemShapesResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListDbSystemShapesResponse(),
            metadata,
        )

        client.list_db_system_shapes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_autonomous_databases_rest_bad_request(
    request_type=oracledatabase.ListAutonomousDatabasesRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_autonomous_databases(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabasesRequest,
        dict,
    ],
)
def test_list_autonomous_databases_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabasesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListAutonomousDatabasesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_autonomous_databases(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabasesPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_autonomous_databases_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_autonomous_databases"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_databases_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_autonomous_databases"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListAutonomousDatabasesRequest.pb(
            oracledatabase.ListAutonomousDatabasesRequest()
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
        return_value = oracledatabase.ListAutonomousDatabasesResponse.to_json(
            oracledatabase.ListAutonomousDatabasesResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListAutonomousDatabasesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListAutonomousDatabasesResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListAutonomousDatabasesResponse(),
            metadata,
        )

        client.list_autonomous_databases(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_autonomous_database_rest_bad_request(
    request_type=oracledatabase.GetAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.get_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GetAutonomousDatabaseRequest,
        dict,
    ],
)
def test_get_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = autonomous_database.AutonomousDatabase(
            name="name_value",
            database="database_value",
            display_name="display_name_value",
            entitlement_id="entitlement_id_value",
            admin_password="admin_password_value",
            network="network_value",
            cidr="cidr_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = autonomous_database.AutonomousDatabase.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_autonomous_database(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, autonomous_database.AutonomousDatabase)
    assert response.name == "name_value"
    assert response.database == "database_value"
    assert response.display_name == "display_name_value"
    assert response.entitlement_id == "entitlement_id_value"
    assert response.admin_password == "admin_password_value"
    assert response.network == "network_value"
    assert response.cidr == "cidr_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_get_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_get_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_get_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.GetAutonomousDatabaseRequest.pb(
            oracledatabase.GetAutonomousDatabaseRequest()
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
        return_value = autonomous_database.AutonomousDatabase.to_json(
            autonomous_database.AutonomousDatabase()
        )
        req.return_value.content = return_value

        request = oracledatabase.GetAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = autonomous_database.AutonomousDatabase()
        post_with_metadata.return_value = (
            autonomous_database.AutonomousDatabase(),
            metadata,
        )

        client.get_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_autonomous_database_rest_bad_request(
    request_type=oracledatabase.CreateAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.CreateAutonomousDatabaseRequest,
        dict,
    ],
)
def test_create_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["autonomous_database"] = {
        "name": "name_value",
        "database": "database_value",
        "display_name": "display_name_value",
        "entitlement_id": "entitlement_id_value",
        "admin_password": "admin_password_value",
        "properties": {
            "ocid": "ocid_value",
            "compute_count": 0.1413,
            "cpu_core_count": 1496,
            "data_storage_size_tb": 2109,
            "data_storage_size_gb": 2096,
            "db_workload": 1,
            "db_edition": 1,
            "character_set": "character_set_value",
            "n_character_set": "n_character_set_value",
            "private_endpoint_ip": "private_endpoint_ip_value",
            "private_endpoint_label": "private_endpoint_label_value",
            "db_version": "db_version_value",
            "is_auto_scaling_enabled": True,
            "is_storage_auto_scaling_enabled": True,
            "license_type": 1,
            "customer_contacts": [{"email": "email_value"}],
            "secret_id": "secret_id_value",
            "vault_id": "vault_id_value",
            "maintenance_schedule_type": 1,
            "mtls_connection_required": True,
            "backup_retention_period_days": 2975,
            "actual_used_data_storage_size_tb": 0.3366,
            "allocated_storage_size_tb": 0.2636,
            "apex_details": {
                "apex_version": "apex_version_value",
                "ords_version": "ords_version_value",
            },
            "are_primary_allowlisted_ips_used": True,
            "lifecycle_details": "lifecycle_details_value",
            "state": 1,
            "autonomous_container_database_id": "autonomous_container_database_id_value",
            "available_upgrade_versions": [
                "available_upgrade_versions_value1",
                "available_upgrade_versions_value2",
            ],
            "connection_strings": {
                "all_connection_strings": {
                    "high": "high_value",
                    "low": "low_value",
                    "medium": "medium_value",
                },
                "dedicated": "dedicated_value",
                "high": "high_value",
                "low": "low_value",
                "medium": "medium_value",
                "profiles": [
                    {
                        "consumer_group": 1,
                        "display_name": "display_name_value",
                        "host_format": 1,
                        "is_regional": True,
                        "protocol": 1,
                        "session_mode": 1,
                        "syntax_format": 1,
                        "tls_authentication": 1,
                        "value": "value_value",
                    }
                ],
            },
            "connection_urls": {
                "apex_uri": "apex_uri_value",
                "database_transforms_uri": "database_transforms_uri_value",
                "graph_studio_uri": "graph_studio_uri_value",
                "machine_learning_notebook_uri": "machine_learning_notebook_uri_value",
                "machine_learning_user_management_uri": "machine_learning_user_management_uri_value",
                "mongo_db_uri": "mongo_db_uri_value",
                "ords_uri": "ords_uri_value",
                "sql_dev_web_uri": "sql_dev_web_uri_value",
            },
            "failed_data_recovery_duration": {"seconds": 751, "nanos": 543},
            "memory_table_gbs": 1691,
            "is_local_data_guard_enabled": True,
            "local_adg_auto_failover_max_data_loss_limit": 4513,
            "local_standby_db": {
                "lag_time_duration": {},
                "lifecycle_details": "lifecycle_details_value",
                "state": 1,
                "data_guard_role_changed_time": {"seconds": 751, "nanos": 543},
                "disaster_recovery_role_changed_time": {},
            },
            "memory_per_oracle_compute_unit_gbs": 3626,
            "local_disaster_recovery_type": 1,
            "data_safe_state": 1,
            "database_management_state": 1,
            "open_mode": 1,
            "operations_insights_state": 1,
            "peer_db_ids": ["peer_db_ids_value1", "peer_db_ids_value2"],
            "permission_level": 1,
            "private_endpoint": "private_endpoint_value",
            "refreshable_mode": 1,
            "refreshable_state": 1,
            "role": 1,
            "scheduled_operation_details": [
                {
                    "day_of_week": 1,
                    "start_time": {
                        "hours": 561,
                        "minutes": 773,
                        "seconds": 751,
                        "nanos": 543,
                    },
                    "stop_time": {},
                }
            ],
            "sql_web_developer_url": "sql_web_developer_url_value",
            "supported_clone_regions": [
                "supported_clone_regions_value1",
                "supported_clone_regions_value2",
            ],
            "used_data_storage_size_tbs": 2752,
            "oci_url": "oci_url_value",
            "total_auto_backup_storage_size_gbs": 0.36100000000000004,
            "next_long_term_backup_time": {},
            "maintenance_begin_time": {},
            "maintenance_end_time": {},
        },
        "labels": {},
        "network": "network_value",
        "cidr": "cidr_value",
        "create_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = oracledatabase.CreateAutonomousDatabaseRequest.meta.fields[
        "autonomous_database"
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
    for field, value in request_init["autonomous_database"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["autonomous_database"][field])):
                    del request_init["autonomous_database"][field][i][subfield]
            else:
                del request_init["autonomous_database"][field][subfield]
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
        response = client.create_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_create_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_create_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_create_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.CreateAutonomousDatabaseRequest.pb(
            oracledatabase.CreateAutonomousDatabaseRequest()
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

        request = oracledatabase.CreateAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.create_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_delete_autonomous_database_rest_bad_request(
    request_type=oracledatabase.DeleteAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.delete_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.DeleteAutonomousDatabaseRequest,
        dict,
    ],
)
def test_delete_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        response = client.delete_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_delete_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_delete_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_delete_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.DeleteAutonomousDatabaseRequest.pb(
            oracledatabase.DeleteAutonomousDatabaseRequest()
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

        request = oracledatabase.DeleteAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.delete_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_restore_autonomous_database_rest_bad_request(
    request_type=oracledatabase.RestoreAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.restore_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.RestoreAutonomousDatabaseRequest,
        dict,
    ],
)
def test_restore_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        response = client.restore_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_restore_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_restore_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_restore_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_restore_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.RestoreAutonomousDatabaseRequest.pb(
            oracledatabase.RestoreAutonomousDatabaseRequest()
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

        request = oracledatabase.RestoreAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.restore_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_generate_autonomous_database_wallet_rest_bad_request(
    request_type=oracledatabase.GenerateAutonomousDatabaseWalletRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.generate_autonomous_database_wallet(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.GenerateAutonomousDatabaseWalletRequest,
        dict,
    ],
)
def test_generate_autonomous_database_wallet_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse(
            archive_content=b"archive_content_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.generate_autonomous_database_wallet(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, oracledatabase.GenerateAutonomousDatabaseWalletResponse)
    assert response.archive_content == b"archive_content_blob"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_autonomous_database_wallet_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_generate_autonomous_database_wallet",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_generate_autonomous_database_wallet_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "pre_generate_autonomous_database_wallet",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.GenerateAutonomousDatabaseWalletRequest.pb(
            oracledatabase.GenerateAutonomousDatabaseWalletRequest()
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
        return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse.to_json(
            oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.GenerateAutonomousDatabaseWalletRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.GenerateAutonomousDatabaseWalletResponse()
        post_with_metadata.return_value = (
            oracledatabase.GenerateAutonomousDatabaseWalletResponse(),
            metadata,
        )

        client.generate_autonomous_database_wallet(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_autonomous_db_versions_rest_bad_request(
    request_type=oracledatabase.ListAutonomousDbVersionsRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_autonomous_db_versions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDbVersionsRequest,
        dict,
    ],
)
def test_list_autonomous_db_versions_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDbVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListAutonomousDbVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_autonomous_db_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDbVersionsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_autonomous_db_versions_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_list_autonomous_db_versions"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_db_versions_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_autonomous_db_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListAutonomousDbVersionsRequest.pb(
            oracledatabase.ListAutonomousDbVersionsRequest()
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
        return_value = oracledatabase.ListAutonomousDbVersionsResponse.to_json(
            oracledatabase.ListAutonomousDbVersionsResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListAutonomousDbVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListAutonomousDbVersionsResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListAutonomousDbVersionsResponse(),
            metadata,
        )

        client.list_autonomous_db_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_autonomous_database_character_sets_rest_bad_request(
    request_type=oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_autonomous_database_character_sets(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabaseCharacterSetsRequest,
        dict,
    ],
)
def test_list_autonomous_database_character_sets_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_autonomous_database_character_sets(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseCharacterSetsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_autonomous_database_character_sets_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_database_character_sets",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_database_character_sets_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "pre_list_autonomous_database_character_sets",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest.pb(
            oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()
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
        return_value = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse.to_json(
                oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
            )
        )
        req.return_value.content = return_value

        request = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListAutonomousDatabaseCharacterSetsResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListAutonomousDatabaseCharacterSetsResponse(),
            metadata,
        )

        client.list_autonomous_database_character_sets(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_autonomous_database_backups_rest_bad_request(
    request_type=oracledatabase.ListAutonomousDatabaseBackupsRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_autonomous_database_backups(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.ListAutonomousDatabaseBackupsRequest,
        dict,
    ],
)
def test_list_autonomous_database_backups_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_autonomous_database_backups(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAutonomousDatabaseBackupsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_autonomous_database_backups_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_database_backups",
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_list_autonomous_database_backups_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_list_autonomous_database_backups"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.ListAutonomousDatabaseBackupsRequest.pb(
            oracledatabase.ListAutonomousDatabaseBackupsRequest()
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
        return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse.to_json(
            oracledatabase.ListAutonomousDatabaseBackupsResponse()
        )
        req.return_value.content = return_value

        request = oracledatabase.ListAutonomousDatabaseBackupsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = oracledatabase.ListAutonomousDatabaseBackupsResponse()
        post_with_metadata.return_value = (
            oracledatabase.ListAutonomousDatabaseBackupsResponse(),
            metadata,
        )

        client.list_autonomous_database_backups(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_stop_autonomous_database_rest_bad_request(
    request_type=oracledatabase.StopAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.stop_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.StopAutonomousDatabaseRequest,
        dict,
    ],
)
def test_stop_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        response = client.stop_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_stop_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_stop_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_stop_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_stop_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.StopAutonomousDatabaseRequest.pb(
            oracledatabase.StopAutonomousDatabaseRequest()
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

        request = oracledatabase.StopAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.stop_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_start_autonomous_database_rest_bad_request(
    request_type=oracledatabase.StartAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.start_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.StartAutonomousDatabaseRequest,
        dict,
    ],
)
def test_start_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        response = client.start_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_start_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_start_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_start_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_start_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.StartAutonomousDatabaseRequest.pb(
            oracledatabase.StartAutonomousDatabaseRequest()
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

        request = oracledatabase.StartAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.start_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_restart_autonomous_database_rest_bad_request(
    request_type=oracledatabase.RestartAutonomousDatabaseRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        client.restart_autonomous_database(request)


@pytest.mark.parametrize(
    "request_type",
    [
        oracledatabase.RestartAutonomousDatabaseRequest,
        dict,
    ],
)
def test_restart_autonomous_database_rest_call_success(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/autonomousDatabases/sample3"
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
        response = client.restart_autonomous_database(request)

    # Establish that the response is the type that we expect.
    json_return_value = json_format.MessageToJson(return_value)


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_restart_autonomous_database_rest_interceptors(null_interceptor):
    transport = transports.OracleDatabaseRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OracleDatabaseRestInterceptor(),
    )
    client = OracleDatabaseClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "post_restart_autonomous_database"
    ) as post, mock.patch.object(
        transports.OracleDatabaseRestInterceptor,
        "post_restart_autonomous_database_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OracleDatabaseRestInterceptor, "pre_restart_autonomous_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = oracledatabase.RestartAutonomousDatabaseRequest.pb(
            oracledatabase.RestartAutonomousDatabaseRequest()
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

        request = oracledatabase.RestartAutonomousDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()
        post_with_metadata.return_value = operations_pb2.Operation(), metadata

        client.restart_autonomous_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_location_rest_bad_request(request_type=locations_pb2.GetLocationRequest):
    client = OracleDatabaseClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
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
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
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


def test_delete_operation_rest_bad_request(
    request_type=operations_pb2.DeleteOperationRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
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
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
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

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
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
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
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
    client = OracleDatabaseClient(
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
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "projects/sample1/locations/sample2"}
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
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_cloud_exadata_infrastructures_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_exadata_infrastructures), "__call__"
    ) as call:
        client.list_cloud_exadata_infrastructures(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudExadataInfrastructuresRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_cloud_exadata_infrastructure_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_exadata_infrastructure), "__call__"
    ) as call:
        client.get_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_cloud_exadata_infrastructure_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_exadata_infrastructure), "__call__"
    ) as call:
        client.create_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_cloud_exadata_infrastructure_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_exadata_infrastructure), "__call__"
    ) as call:
        client.delete_cloud_exadata_infrastructure(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudExadataInfrastructureRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_cloud_vm_clusters_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cloud_vm_clusters), "__call__"
    ) as call:
        client.list_cloud_vm_clusters(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListCloudVmClustersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_cloud_vm_cluster_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_cloud_vm_cluster), "__call__"
    ) as call:
        client.get_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_cloud_vm_cluster_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cloud_vm_cluster), "__call__"
    ) as call:
        client.create_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_cloud_vm_cluster_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_cloud_vm_cluster), "__call__"
    ) as call:
        client.delete_cloud_vm_cluster(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteCloudVmClusterRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_entitlements_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entitlements), "__call__"
    ) as call:
        client.list_entitlements(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListEntitlementsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_servers_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_servers), "__call__") as call:
        client.list_db_servers(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbServersRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_nodes_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_db_nodes), "__call__") as call:
        client.list_db_nodes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbNodesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_gi_versions_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(type(client.transport.list_gi_versions), "__call__") as call:
        client.list_gi_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListGiVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_db_system_shapes_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_db_system_shapes), "__call__"
    ) as call:
        client.list_db_system_shapes(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListDbSystemShapesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_databases_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_databases), "__call__"
    ) as call:
        client.list_autonomous_databases(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabasesRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_autonomous_database), "__call__"
    ) as call:
        client.get_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GetAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_autonomous_database), "__call__"
    ) as call:
        client.create_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.CreateAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_delete_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_autonomous_database), "__call__"
    ) as call:
        client.delete_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.DeleteAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restore_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restore_autonomous_database), "__call__"
    ) as call:
        client.restore_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestoreAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_generate_autonomous_database_wallet_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_autonomous_database_wallet), "__call__"
    ) as call:
        client.generate_autonomous_database_wallet(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.GenerateAutonomousDatabaseWalletRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_db_versions_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_db_versions), "__call__"
    ) as call:
        client.list_autonomous_db_versions(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDbVersionsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_database_character_sets_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_character_sets), "__call__"
    ) as call:
        client.list_autonomous_database_character_sets(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseCharacterSetsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_autonomous_database_backups_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_autonomous_database_backups), "__call__"
    ) as call:
        client.list_autonomous_database_backups(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.ListAutonomousDatabaseBackupsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_stop_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_autonomous_database), "__call__"
    ) as call:
        client.stop_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StopAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_start_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.start_autonomous_database), "__call__"
    ) as call:
        client.start_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.StartAutonomousDatabaseRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_restart_autonomous_database_empty_call_rest():
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_autonomous_database), "__call__"
    ) as call:
        client.restart_autonomous_database(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = oracledatabase.RestartAutonomousDatabaseRequest()

        assert args[0] == request_msg


def test_oracle_database_rest_lro_client():
    client = OracleDatabaseClient(
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
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.OracleDatabaseGrpcTransport,
    )


def test_oracle_database_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OracleDatabaseTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_oracle_database_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.oracledatabase_v1.services.oracle_database.transports.OracleDatabaseTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OracleDatabaseTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_cloud_exadata_infrastructures",
        "get_cloud_exadata_infrastructure",
        "create_cloud_exadata_infrastructure",
        "delete_cloud_exadata_infrastructure",
        "list_cloud_vm_clusters",
        "get_cloud_vm_cluster",
        "create_cloud_vm_cluster",
        "delete_cloud_vm_cluster",
        "list_entitlements",
        "list_db_servers",
        "list_db_nodes",
        "list_gi_versions",
        "list_db_system_shapes",
        "list_autonomous_databases",
        "get_autonomous_database",
        "create_autonomous_database",
        "delete_autonomous_database",
        "restore_autonomous_database",
        "generate_autonomous_database_wallet",
        "list_autonomous_db_versions",
        "list_autonomous_database_character_sets",
        "list_autonomous_database_backups",
        "stop_autonomous_database",
        "start_autonomous_database",
        "restart_autonomous_database",
        "get_location",
        "list_locations",
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


def test_oracle_database_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.oracledatabase_v1.services.oracle_database.transports.OracleDatabaseTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OracleDatabaseTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_oracle_database_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.oracledatabase_v1.services.oracle_database.transports.OracleDatabaseTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OracleDatabaseTransport()
        adc.assert_called_once()


def test_oracle_database_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OracleDatabaseClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
    ],
)
def test_oracle_database_transport_auth_adc(transport_class):
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
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
        transports.OracleDatabaseRestTransport,
    ],
)
def test_oracle_database_transport_auth_gdch_credentials(transport_class):
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
        (transports.OracleDatabaseGrpcTransport, grpc_helpers),
        (transports.OracleDatabaseGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_oracle_database_transport_create_channel(transport_class, grpc_helpers):
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
            "oracledatabase.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="oracledatabase.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
    ],
)
def test_oracle_database_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_oracle_database_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.OracleDatabaseRestTransport(
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
def test_oracle_database_host_no_port(transport_name):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="oracledatabase.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "oracledatabase.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://oracledatabase.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_oracle_database_host_with_port(transport_name):
    client = OracleDatabaseClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="oracledatabase.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "oracledatabase.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://oracledatabase.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_oracle_database_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = OracleDatabaseClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = OracleDatabaseClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_cloud_exadata_infrastructures._session
    session2 = client2.transport.list_cloud_exadata_infrastructures._session
    assert session1 != session2
    session1 = client1.transport.get_cloud_exadata_infrastructure._session
    session2 = client2.transport.get_cloud_exadata_infrastructure._session
    assert session1 != session2
    session1 = client1.transport.create_cloud_exadata_infrastructure._session
    session2 = client2.transport.create_cloud_exadata_infrastructure._session
    assert session1 != session2
    session1 = client1.transport.delete_cloud_exadata_infrastructure._session
    session2 = client2.transport.delete_cloud_exadata_infrastructure._session
    assert session1 != session2
    session1 = client1.transport.list_cloud_vm_clusters._session
    session2 = client2.transport.list_cloud_vm_clusters._session
    assert session1 != session2
    session1 = client1.transport.get_cloud_vm_cluster._session
    session2 = client2.transport.get_cloud_vm_cluster._session
    assert session1 != session2
    session1 = client1.transport.create_cloud_vm_cluster._session
    session2 = client2.transport.create_cloud_vm_cluster._session
    assert session1 != session2
    session1 = client1.transport.delete_cloud_vm_cluster._session
    session2 = client2.transport.delete_cloud_vm_cluster._session
    assert session1 != session2
    session1 = client1.transport.list_entitlements._session
    session2 = client2.transport.list_entitlements._session
    assert session1 != session2
    session1 = client1.transport.list_db_servers._session
    session2 = client2.transport.list_db_servers._session
    assert session1 != session2
    session1 = client1.transport.list_db_nodes._session
    session2 = client2.transport.list_db_nodes._session
    assert session1 != session2
    session1 = client1.transport.list_gi_versions._session
    session2 = client2.transport.list_gi_versions._session
    assert session1 != session2
    session1 = client1.transport.list_db_system_shapes._session
    session2 = client2.transport.list_db_system_shapes._session
    assert session1 != session2
    session1 = client1.transport.list_autonomous_databases._session
    session2 = client2.transport.list_autonomous_databases._session
    assert session1 != session2
    session1 = client1.transport.get_autonomous_database._session
    session2 = client2.transport.get_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.create_autonomous_database._session
    session2 = client2.transport.create_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.delete_autonomous_database._session
    session2 = client2.transport.delete_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.restore_autonomous_database._session
    session2 = client2.transport.restore_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.generate_autonomous_database_wallet._session
    session2 = client2.transport.generate_autonomous_database_wallet._session
    assert session1 != session2
    session1 = client1.transport.list_autonomous_db_versions._session
    session2 = client2.transport.list_autonomous_db_versions._session
    assert session1 != session2
    session1 = client1.transport.list_autonomous_database_character_sets._session
    session2 = client2.transport.list_autonomous_database_character_sets._session
    assert session1 != session2
    session1 = client1.transport.list_autonomous_database_backups._session
    session2 = client2.transport.list_autonomous_database_backups._session
    assert session1 != session2
    session1 = client1.transport.stop_autonomous_database._session
    session2 = client2.transport.stop_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.start_autonomous_database._session
    session2 = client2.transport.start_autonomous_database._session
    assert session1 != session2
    session1 = client1.transport.restart_autonomous_database._session
    session2 = client2.transport.restart_autonomous_database._session
    assert session1 != session2


def test_oracle_database_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OracleDatabaseGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_oracle_database_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OracleDatabaseGrpcAsyncIOTransport(
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
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
    ],
)
def test_oracle_database_transport_channel_mtls_with_client_cert_source(
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
        transports.OracleDatabaseGrpcTransport,
        transports.OracleDatabaseGrpcAsyncIOTransport,
    ],
)
def test_oracle_database_transport_channel_mtls_with_adc(transport_class):
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


def test_oracle_database_grpc_lro_client():
    client = OracleDatabaseClient(
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


def test_oracle_database_grpc_lro_async_client():
    client = OracleDatabaseAsyncClient(
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


def test_autonomous_database_path():
    project = "squid"
    location = "clam"
    autonomous_database = "whelk"
    expected = "projects/{project}/locations/{location}/autonomousDatabases/{autonomous_database}".format(
        project=project,
        location=location,
        autonomous_database=autonomous_database,
    )
    actual = OracleDatabaseClient.autonomous_database_path(
        project, location, autonomous_database
    )
    assert expected == actual


def test_parse_autonomous_database_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "autonomous_database": "nudibranch",
    }
    path = OracleDatabaseClient.autonomous_database_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_autonomous_database_path(path)
    assert expected == actual


def test_autonomous_database_backup_path():
    project = "cuttlefish"
    location = "mussel"
    autonomous_database_backup = "winkle"
    expected = "projects/{project}/locations/{location}/autonomousDatabaseBackups/{autonomous_database_backup}".format(
        project=project,
        location=location,
        autonomous_database_backup=autonomous_database_backup,
    )
    actual = OracleDatabaseClient.autonomous_database_backup_path(
        project, location, autonomous_database_backup
    )
    assert expected == actual


def test_parse_autonomous_database_backup_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "autonomous_database_backup": "abalone",
    }
    path = OracleDatabaseClient.autonomous_database_backup_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_autonomous_database_backup_path(path)
    assert expected == actual


def test_autonomous_database_character_set_path():
    project = "squid"
    location = "clam"
    autonomous_database_character_set = "whelk"
    expected = "projects/{project}/locations/{location}/autonomousDatabaseCharacterSets/{autonomous_database_character_set}".format(
        project=project,
        location=location,
        autonomous_database_character_set=autonomous_database_character_set,
    )
    actual = OracleDatabaseClient.autonomous_database_character_set_path(
        project, location, autonomous_database_character_set
    )
    assert expected == actual


def test_parse_autonomous_database_character_set_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "autonomous_database_character_set": "nudibranch",
    }
    path = OracleDatabaseClient.autonomous_database_character_set_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_autonomous_database_character_set_path(path)
    assert expected == actual


def test_autonomous_db_version_path():
    project = "cuttlefish"
    location = "mussel"
    autonomous_db_version = "winkle"
    expected = "projects/{project}/locations/{location}/autonomousDbVersions/{autonomous_db_version}".format(
        project=project,
        location=location,
        autonomous_db_version=autonomous_db_version,
    )
    actual = OracleDatabaseClient.autonomous_db_version_path(
        project, location, autonomous_db_version
    )
    assert expected == actual


def test_parse_autonomous_db_version_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "autonomous_db_version": "abalone",
    }
    path = OracleDatabaseClient.autonomous_db_version_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_autonomous_db_version_path(path)
    assert expected == actual


def test_cloud_exadata_infrastructure_path():
    project = "squid"
    location = "clam"
    cloud_exadata_infrastructure = "whelk"
    expected = "projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}".format(
        project=project,
        location=location,
        cloud_exadata_infrastructure=cloud_exadata_infrastructure,
    )
    actual = OracleDatabaseClient.cloud_exadata_infrastructure_path(
        project, location, cloud_exadata_infrastructure
    )
    assert expected == actual


def test_parse_cloud_exadata_infrastructure_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "cloud_exadata_infrastructure": "nudibranch",
    }
    path = OracleDatabaseClient.cloud_exadata_infrastructure_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_cloud_exadata_infrastructure_path(path)
    assert expected == actual


def test_cloud_vm_cluster_path():
    project = "cuttlefish"
    location = "mussel"
    cloud_vm_cluster = "winkle"
    expected = "projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}".format(
        project=project,
        location=location,
        cloud_vm_cluster=cloud_vm_cluster,
    )
    actual = OracleDatabaseClient.cloud_vm_cluster_path(
        project, location, cloud_vm_cluster
    )
    assert expected == actual


def test_parse_cloud_vm_cluster_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "cloud_vm_cluster": "abalone",
    }
    path = OracleDatabaseClient.cloud_vm_cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_cloud_vm_cluster_path(path)
    assert expected == actual


def test_db_node_path():
    project = "squid"
    location = "clam"
    cloud_vm_cluster = "whelk"
    db_node = "octopus"
    expected = "projects/{project}/locations/{location}/cloudVmClusters/{cloud_vm_cluster}/dbNodes/{db_node}".format(
        project=project,
        location=location,
        cloud_vm_cluster=cloud_vm_cluster,
        db_node=db_node,
    )
    actual = OracleDatabaseClient.db_node_path(
        project, location, cloud_vm_cluster, db_node
    )
    assert expected == actual


def test_parse_db_node_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "cloud_vm_cluster": "cuttlefish",
        "db_node": "mussel",
    }
    path = OracleDatabaseClient.db_node_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_db_node_path(path)
    assert expected == actual


def test_db_server_path():
    project = "winkle"
    location = "nautilus"
    cloud_exadata_infrastructure = "scallop"
    db_server = "abalone"
    expected = "projects/{project}/locations/{location}/cloudExadataInfrastructures/{cloud_exadata_infrastructure}/dbServers/{db_server}".format(
        project=project,
        location=location,
        cloud_exadata_infrastructure=cloud_exadata_infrastructure,
        db_server=db_server,
    )
    actual = OracleDatabaseClient.db_server_path(
        project, location, cloud_exadata_infrastructure, db_server
    )
    assert expected == actual


def test_parse_db_server_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "cloud_exadata_infrastructure": "whelk",
        "db_server": "octopus",
    }
    path = OracleDatabaseClient.db_server_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_db_server_path(path)
    assert expected == actual


def test_db_system_shape_path():
    project = "oyster"
    location = "nudibranch"
    db_system_shape = "cuttlefish"
    expected = "projects/{project}/locations/{location}/dbSystemShapes/{db_system_shape}".format(
        project=project,
        location=location,
        db_system_shape=db_system_shape,
    )
    actual = OracleDatabaseClient.db_system_shape_path(
        project, location, db_system_shape
    )
    assert expected == actual


def test_parse_db_system_shape_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "db_system_shape": "nautilus",
    }
    path = OracleDatabaseClient.db_system_shape_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_db_system_shape_path(path)
    assert expected == actual


def test_entitlement_path():
    project = "scallop"
    location = "abalone"
    entitlement = "squid"
    expected = (
        "projects/{project}/locations/{location}/entitlements/{entitlement}".format(
            project=project,
            location=location,
            entitlement=entitlement,
        )
    )
    actual = OracleDatabaseClient.entitlement_path(project, location, entitlement)
    assert expected == actual


def test_parse_entitlement_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "entitlement": "octopus",
    }
    path = OracleDatabaseClient.entitlement_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_entitlement_path(path)
    assert expected == actual


def test_gi_version_path():
    project = "oyster"
    location = "nudibranch"
    gi_version = "cuttlefish"
    expected = "projects/{project}/locations/{location}/giVersions/{gi_version}".format(
        project=project,
        location=location,
        gi_version=gi_version,
    )
    actual = OracleDatabaseClient.gi_version_path(project, location, gi_version)
    assert expected == actual


def test_parse_gi_version_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "gi_version": "nautilus",
    }
    path = OracleDatabaseClient.gi_version_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_gi_version_path(path)
    assert expected == actual


def test_network_path():
    project = "scallop"
    network = "abalone"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project,
        network=network,
    )
    actual = OracleDatabaseClient.network_path(project, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "squid",
        "network": "clam",
    }
    path = OracleDatabaseClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_network_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OracleDatabaseClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = OracleDatabaseClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = OracleDatabaseClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = OracleDatabaseClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = OracleDatabaseClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = OracleDatabaseClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = OracleDatabaseClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = OracleDatabaseClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = OracleDatabaseClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = OracleDatabaseClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OracleDatabaseClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OracleDatabaseTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OracleDatabaseClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OracleDatabaseTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OracleDatabaseClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_delete_operation(transport: str = "grpc"):
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(),
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = OracleDatabaseAsyncClient(credentials=async_anonymous_credentials())

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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
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
    client = OracleDatabaseClient(
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
    client = OracleDatabaseAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = OracleDatabaseClient(
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
        client = OracleDatabaseClient(
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
        (OracleDatabaseClient, transports.OracleDatabaseGrpcTransport),
        (OracleDatabaseAsyncClient, transports.OracleDatabaseGrpcAsyncIOTransport),
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
