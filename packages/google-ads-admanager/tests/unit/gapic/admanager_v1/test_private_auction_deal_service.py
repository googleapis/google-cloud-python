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

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import money_pb2  # type: ignore

from google.ads.admanager_v1.services.private_auction_deal_service import (
    PrivateAuctionDealServiceClient,
    pagers,
    transports,
)
from google.ads.admanager_v1.types import (
    deal_buyer_permission_type_enum,
    private_auction_deal_messages,
    private_auction_deal_service,
    private_marketplace_enums,
    request_platform_enum,
    size,
    size_type_enum,
    targeted_video_bumper_type_enum,
    targeting,
    video_position_enum,
)

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

    assert PrivateAuctionDealServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        PrivateAuctionDealServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert PrivateAuctionDealServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            PrivateAuctionDealServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            PrivateAuctionDealServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert PrivateAuctionDealServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert PrivateAuctionDealServiceClient._get_client_cert_source(None, False) is None
    assert (
        PrivateAuctionDealServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        PrivateAuctionDealServiceClient._get_client_cert_source(
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
                PrivateAuctionDealServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                PrivateAuctionDealServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    PrivateAuctionDealServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PrivateAuctionDealServiceClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = PrivateAuctionDealServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        PrivateAuctionDealServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = PrivateAuctionDealServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == PrivateAuctionDealServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == PrivateAuctionDealServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == PrivateAuctionDealServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        PrivateAuctionDealServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        PrivateAuctionDealServiceClient._get_api_endpoint(
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
        PrivateAuctionDealServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        PrivateAuctionDealServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        PrivateAuctionDealServiceClient._get_universe_domain(None, None)
        == PrivateAuctionDealServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        PrivateAuctionDealServiceClient._get_universe_domain("", None)
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
    client = PrivateAuctionDealServiceClient(credentials=cred)
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
    client = PrivateAuctionDealServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (PrivateAuctionDealServiceClient, "rest"),
    ],
)
def test_private_auction_deal_service_client_from_service_account_info(
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
            "admanager.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://admanager.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.PrivateAuctionDealServiceRestTransport, "rest"),
    ],
)
def test_private_auction_deal_service_client_service_account_always_use_jwt(
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
        (PrivateAuctionDealServiceClient, "rest"),
    ],
)
def test_private_auction_deal_service_client_from_service_account_file(
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
            "admanager.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://admanager.googleapis.com"
        )


def test_private_auction_deal_service_client_get_transport_class():
    transport = PrivateAuctionDealServiceClient.get_transport_class()
    available_transports = [
        transports.PrivateAuctionDealServiceRestTransport,
    ]
    assert transport in available_transports

    transport = PrivateAuctionDealServiceClient.get_transport_class("rest")
    assert transport == transports.PrivateAuctionDealServiceRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    PrivateAuctionDealServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PrivateAuctionDealServiceClient),
)
def test_private_auction_deal_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        PrivateAuctionDealServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        PrivateAuctionDealServiceClient, "get_transport_class"
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
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
            "rest",
            "true",
        ),
        (
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    PrivateAuctionDealServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PrivateAuctionDealServiceClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_private_auction_deal_service_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [PrivateAuctionDealServiceClient])
@mock.patch.object(
    PrivateAuctionDealServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateAuctionDealServiceClient),
)
def test_private_auction_deal_service_client_get_mtls_endpoint_and_cert_source(
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


@pytest.mark.parametrize("client_class", [PrivateAuctionDealServiceClient])
@mock.patch.object(
    PrivateAuctionDealServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(PrivateAuctionDealServiceClient),
)
def test_private_auction_deal_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = PrivateAuctionDealServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        PrivateAuctionDealServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = PrivateAuctionDealServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
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
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
            "rest",
        ),
    ],
)
def test_private_auction_deal_service_client_client_options_scopes(
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
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_private_auction_deal_service_client_client_options_credentials_file(
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


def test_get_private_auction_deal_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_private_auction_deal
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_private_auction_deal
        ] = mock_rpc

        request = {}
        client.get_private_auction_deal(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_private_auction_deal(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_private_auction_deal_rest_required_fields(
    request_type=private_auction_deal_service.GetPrivateAuctionDealRequest,
):
    transport_class = transports.PrivateAuctionDealServiceRestTransport

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
    ).get_private_auction_deal._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_private_auction_deal._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_auction_deal_messages.PrivateAuctionDeal()
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
            return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_private_auction_deal(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_private_auction_deal_rest_unset_required_fields():
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_private_auction_deal._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_private_auction_deal_rest_flattened():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "networks/sample1/privateAuctionDeals/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_private_auction_deal(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=networks/*/privateAuctionDeals/*}" % client.transport._host,
            args[1],
        )


def test_get_private_auction_deal_rest_flattened_error(transport: str = "rest"):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_private_auction_deal(
            private_auction_deal_service.GetPrivateAuctionDealRequest(),
            name="name_value",
        )


def test_list_private_auction_deals_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_private_auction_deals
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_private_auction_deals
        ] = mock_rpc

        request = {}
        client.list_private_auction_deals(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_private_auction_deals(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_private_auction_deals_rest_required_fields(
    request_type=private_auction_deal_service.ListPrivateAuctionDealsRequest,
):
    transport_class = transports.PrivateAuctionDealServiceRestTransport

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
    ).list_private_auction_deals._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_private_auction_deals._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
            "skip",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_auction_deal_service.ListPrivateAuctionDealsResponse()
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
                private_auction_deal_service.ListPrivateAuctionDealsResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_private_auction_deals(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_private_auction_deals_rest_unset_required_fields():
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_private_auction_deals._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
                "skip",
            )
        )
        & set(("parent",))
    )


def test_list_private_auction_deals_rest_flattened():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_service.ListPrivateAuctionDealsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "networks/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = private_auction_deal_service.ListPrivateAuctionDealsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_private_auction_deals(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=networks/*}/privateAuctionDeals" % client.transport._host,
            args[1],
        )


def test_list_private_auction_deals_rest_flattened_error(transport: str = "rest"):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_private_auction_deals(
            private_auction_deal_service.ListPrivateAuctionDealsRequest(),
            parent="parent_value",
        )


def test_list_private_auction_deals_rest_pager(transport: str = "rest"):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            private_auction_deal_service.ListPrivateAuctionDealsResponse(
                private_auction_deals=[
                    private_auction_deal_messages.PrivateAuctionDeal(),
                    private_auction_deal_messages.PrivateAuctionDeal(),
                    private_auction_deal_messages.PrivateAuctionDeal(),
                ],
                next_page_token="abc",
            ),
            private_auction_deal_service.ListPrivateAuctionDealsResponse(
                private_auction_deals=[],
                next_page_token="def",
            ),
            private_auction_deal_service.ListPrivateAuctionDealsResponse(
                private_auction_deals=[
                    private_auction_deal_messages.PrivateAuctionDeal(),
                ],
                next_page_token="ghi",
            ),
            private_auction_deal_service.ListPrivateAuctionDealsResponse(
                private_auction_deals=[
                    private_auction_deal_messages.PrivateAuctionDeal(),
                    private_auction_deal_messages.PrivateAuctionDeal(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            private_auction_deal_service.ListPrivateAuctionDealsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "networks/sample1"}

        pager = client.list_private_auction_deals(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, private_auction_deal_messages.PrivateAuctionDeal)
            for i in results
        )

        pages = list(client.list_private_auction_deals(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_private_auction_deal_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_private_auction_deal
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_private_auction_deal
        ] = mock_rpc

        request = {}
        client.create_private_auction_deal(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_private_auction_deal(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_private_auction_deal_rest_required_fields(
    request_type=private_auction_deal_service.CreatePrivateAuctionDealRequest,
):
    transport_class = transports.PrivateAuctionDealServiceRestTransport

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
    ).create_private_auction_deal._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_private_auction_deal._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_auction_deal_messages.PrivateAuctionDeal()
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
            return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_private_auction_deal(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_private_auction_deal_rest_unset_required_fields():
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_private_auction_deal._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "privateAuctionDeal",
            )
        )
    )


def test_create_private_auction_deal_rest_flattened():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "networks/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            private_auction_deal=private_auction_deal_messages.PrivateAuctionDeal(
                name="name_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_private_auction_deal(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=networks/*}/privateAuctionDeals" % client.transport._host,
            args[1],
        )


def test_create_private_auction_deal_rest_flattened_error(transport: str = "rest"):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_private_auction_deal(
            private_auction_deal_service.CreatePrivateAuctionDealRequest(),
            parent="parent_value",
            private_auction_deal=private_auction_deal_messages.PrivateAuctionDeal(
                name="name_value"
            ),
        )


def test_update_private_auction_deal_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_private_auction_deal
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_private_auction_deal
        ] = mock_rpc

        request = {}
        client.update_private_auction_deal(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_private_auction_deal(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_private_auction_deal_rest_required_fields(
    request_type=private_auction_deal_service.UpdatePrivateAuctionDealRequest,
):
    transport_class = transports.PrivateAuctionDealServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_private_auction_deal._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_private_auction_deal._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_auction_deal_messages.PrivateAuctionDeal()
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
            return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_private_auction_deal(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_private_auction_deal_rest_unset_required_fields():
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_private_auction_deal._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "privateAuctionDeal",
                "updateMask",
            )
        )
    )


def test_update_private_auction_deal_rest_flattened():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "private_auction_deal": {
                "name": "networks/sample1/privateAuctionDeals/sample2"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            private_auction_deal=private_auction_deal_messages.PrivateAuctionDeal(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_private_auction_deal(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{private_auction_deal.name=networks/*/privateAuctionDeals/*}"
            % client.transport._host,
            args[1],
        )


def test_update_private_auction_deal_rest_flattened_error(transport: str = "rest"):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_private_auction_deal(
            private_auction_deal_service.UpdatePrivateAuctionDealRequest(),
            private_auction_deal=private_auction_deal_messages.PrivateAuctionDeal(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateAuctionDealServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PrivateAuctionDealServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PrivateAuctionDealServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateAuctionDealServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = PrivateAuctionDealServiceClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PrivateAuctionDealServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_rest():
    transport = PrivateAuctionDealServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_get_private_auction_deal_rest_bad_request(
    request_type=private_auction_deal_service.GetPrivateAuctionDealRequest,
):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "networks/sample1/privateAuctionDeals/sample2"}
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
        client.get_private_auction_deal(request)


@pytest.mark.parametrize(
    "request_type",
    [
        private_auction_deal_service.GetPrivateAuctionDealRequest,
        dict,
    ],
)
def test_get_private_auction_deal_rest_call_success(request_type):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "networks/sample1/privateAuctionDeals/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal(
            name="name_value",
            private_auction_deal_id=2414,
            private_auction_id=1913,
            private_auction_display_name="private_auction_display_name_value",
            buyer_account_id=1695,
            external_deal_id=1668,
            status=private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING,
            auction_priority_enabled=True,
            block_override_enabled=True,
            buyer_permission_type=deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_private_auction_deal(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, private_auction_deal_messages.PrivateAuctionDeal)
    assert response.name == "name_value"
    assert response.private_auction_deal_id == 2414
    assert response.private_auction_id == 1913
    assert response.private_auction_display_name == "private_auction_display_name_value"
    assert response.buyer_account_id == 1695
    assert response.external_deal_id == 1668
    assert (
        response.status
        == private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING
    )
    assert response.auction_priority_enabled is True
    assert response.block_override_enabled is True
    assert (
        response.buyer_permission_type
        == deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_private_auction_deal_rest_interceptors(null_interceptor):
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateAuctionDealServiceRestInterceptor(),
    )
    client = PrivateAuctionDealServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_get_private_auction_deal",
    ) as post, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_get_private_auction_deal_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "pre_get_private_auction_deal",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = private_auction_deal_service.GetPrivateAuctionDealRequest.pb(
            private_auction_deal_service.GetPrivateAuctionDealRequest()
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
        return_value = private_auction_deal_messages.PrivateAuctionDeal.to_json(
            private_auction_deal_messages.PrivateAuctionDeal()
        )
        req.return_value.content = return_value

        request = private_auction_deal_service.GetPrivateAuctionDealRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_auction_deal_messages.PrivateAuctionDeal()
        post_with_metadata.return_value = (
            private_auction_deal_messages.PrivateAuctionDeal(),
            metadata,
        )

        client.get_private_auction_deal(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_private_auction_deals_rest_bad_request(
    request_type=private_auction_deal_service.ListPrivateAuctionDealsRequest,
):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "networks/sample1"}
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
        client.list_private_auction_deals(request)


@pytest.mark.parametrize(
    "request_type",
    [
        private_auction_deal_service.ListPrivateAuctionDealsRequest,
        dict,
    ],
)
def test_list_private_auction_deals_rest_call_success(request_type):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "networks/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_service.ListPrivateAuctionDealsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = private_auction_deal_service.ListPrivateAuctionDealsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_private_auction_deals(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateAuctionDealsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_private_auction_deals_rest_interceptors(null_interceptor):
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateAuctionDealServiceRestInterceptor(),
    )
    client = PrivateAuctionDealServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_list_private_auction_deals",
    ) as post, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_list_private_auction_deals_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "pre_list_private_auction_deals",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = private_auction_deal_service.ListPrivateAuctionDealsRequest.pb(
            private_auction_deal_service.ListPrivateAuctionDealsRequest()
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
            private_auction_deal_service.ListPrivateAuctionDealsResponse.to_json(
                private_auction_deal_service.ListPrivateAuctionDealsResponse()
            )
        )
        req.return_value.content = return_value

        request = private_auction_deal_service.ListPrivateAuctionDealsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            private_auction_deal_service.ListPrivateAuctionDealsResponse()
        )
        post_with_metadata.return_value = (
            private_auction_deal_service.ListPrivateAuctionDealsResponse(),
            metadata,
        )

        client.list_private_auction_deals(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_private_auction_deal_rest_bad_request(
    request_type=private_auction_deal_service.CreatePrivateAuctionDealRequest,
):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "networks/sample1"}
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
        client.create_private_auction_deal(request)


@pytest.mark.parametrize(
    "request_type",
    [
        private_auction_deal_service.CreatePrivateAuctionDealRequest,
        dict,
    ],
)
def test_create_private_auction_deal_rest_call_success(request_type):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "networks/sample1"}
    request_init["private_auction_deal"] = {
        "name": "name_value",
        "private_auction_deal_id": 2414,
        "private_auction_id": 1913,
        "private_auction_display_name": "private_auction_display_name_value",
        "buyer_account_id": 1695,
        "external_deal_id": 1668,
        "targeting": {
            "geo_targeting": {
                "targeted_geos": ["targeted_geos_value1", "targeted_geos_value2"],
                "excluded_geos": ["excluded_geos_value1", "excluded_geos_value2"],
            },
            "technology_targeting": {
                "bandwidth_targeting": {
                    "targeted_bandwidth_groups": [
                        "targeted_bandwidth_groups_value1",
                        "targeted_bandwidth_groups_value2",
                    ],
                    "excluded_bandwidth_groups": [
                        "excluded_bandwidth_groups_value1",
                        "excluded_bandwidth_groups_value2",
                    ],
                },
                "device_category_targeting": {
                    "targeted_categories": [
                        "targeted_categories_value1",
                        "targeted_categories_value2",
                    ],
                    "excluded_categories": [
                        "excluded_categories_value1",
                        "excluded_categories_value2",
                    ],
                },
                "operating_system_targeting": {
                    "targeted_operating_systems": [
                        "targeted_operating_systems_value1",
                        "targeted_operating_systems_value2",
                    ],
                    "excluded_operating_systems": [
                        "excluded_operating_systems_value1",
                        "excluded_operating_systems_value2",
                    ],
                    "targeted_operating_system_versions": [
                        "targeted_operating_system_versions_value1",
                        "targeted_operating_system_versions_value2",
                    ],
                    "excluded_operating_system_versions": [
                        "excluded_operating_system_versions_value1",
                        "excluded_operating_system_versions_value2",
                    ],
                },
            },
            "inventory_targeting": {
                "targeted_ad_units": [
                    {"include_descendants": True, "ad_unit": "ad_unit_value"}
                ],
                "excluded_ad_units": {},
                "targeted_placements": [
                    "targeted_placements_value1",
                    "targeted_placements_value2",
                ],
            },
            "request_platform_targeting": {"request_platforms": [1]},
            "custom_targeting": {
                "custom_targeting_clauses": [
                    {
                        "custom_targeting_literals": [
                            {
                                "negative": True,
                                "custom_targeting_key": "custom_targeting_key_value",
                                "custom_targeting_values": [
                                    "custom_targeting_values_value1",
                                    "custom_targeting_values_value2",
                                ],
                            }
                        ]
                    }
                ]
            },
            "user_domain_targeting": {
                "targeted_user_domains": [
                    "targeted_user_domains_value1",
                    "targeted_user_domains_value2",
                ],
                "excluded_user_domains": [
                    "excluded_user_domains_value1",
                    "excluded_user_domains_value2",
                ],
            },
            "video_position_targeting": {
                "video_positions": [
                    {
                        "midroll_index": 1386,
                        "reverse_midroll_index": 2245,
                        "pod_position": 1303,
                        "position_type": 1,
                        "bumper_type": 1,
                    }
                ]
            },
            "data_segment_targeting": {"has_data_segment_targeting": True},
        },
        "end_time": {"seconds": 751, "nanos": 543},
        "floor_price": {
            "currency_code": "currency_code_value",
            "units": 563,
            "nanos": 543,
        },
        "creative_sizes": [{"width": 544, "height": 633, "size_type": 1}],
        "status": 1,
        "auction_priority_enabled": True,
        "block_override_enabled": True,
        "buyer_permission_type": 1,
        "buyer_data": {"buyer_emails": ["buyer_emails_value1", "buyer_emails_value2"]},
        "create_time": {},
        "update_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = (
        private_auction_deal_service.CreatePrivateAuctionDealRequest.meta.fields[
            "private_auction_deal"
        ]
    )

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
        "private_auction_deal"
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
                for i in range(0, len(request_init["private_auction_deal"][field])):
                    del request_init["private_auction_deal"][field][i][subfield]
            else:
                del request_init["private_auction_deal"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal(
            name="name_value",
            private_auction_deal_id=2414,
            private_auction_id=1913,
            private_auction_display_name="private_auction_display_name_value",
            buyer_account_id=1695,
            external_deal_id=1668,
            status=private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING,
            auction_priority_enabled=True,
            block_override_enabled=True,
            buyer_permission_type=deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_private_auction_deal(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, private_auction_deal_messages.PrivateAuctionDeal)
    assert response.name == "name_value"
    assert response.private_auction_deal_id == 2414
    assert response.private_auction_id == 1913
    assert response.private_auction_display_name == "private_auction_display_name_value"
    assert response.buyer_account_id == 1695
    assert response.external_deal_id == 1668
    assert (
        response.status
        == private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING
    )
    assert response.auction_priority_enabled is True
    assert response.block_override_enabled is True
    assert (
        response.buyer_permission_type
        == deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_private_auction_deal_rest_interceptors(null_interceptor):
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateAuctionDealServiceRestInterceptor(),
    )
    client = PrivateAuctionDealServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_create_private_auction_deal",
    ) as post, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_create_private_auction_deal_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "pre_create_private_auction_deal",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = private_auction_deal_service.CreatePrivateAuctionDealRequest.pb(
            private_auction_deal_service.CreatePrivateAuctionDealRequest()
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
        return_value = private_auction_deal_messages.PrivateAuctionDeal.to_json(
            private_auction_deal_messages.PrivateAuctionDeal()
        )
        req.return_value.content = return_value

        request = private_auction_deal_service.CreatePrivateAuctionDealRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_auction_deal_messages.PrivateAuctionDeal()
        post_with_metadata.return_value = (
            private_auction_deal_messages.PrivateAuctionDeal(),
            metadata,
        )

        client.create_private_auction_deal(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_update_private_auction_deal_rest_bad_request(
    request_type=private_auction_deal_service.UpdatePrivateAuctionDealRequest,
):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "private_auction_deal": {"name": "networks/sample1/privateAuctionDeals/sample2"}
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
        client.update_private_auction_deal(request)


@pytest.mark.parametrize(
    "request_type",
    [
        private_auction_deal_service.UpdatePrivateAuctionDealRequest,
        dict,
    ],
)
def test_update_private_auction_deal_rest_call_success(request_type):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "private_auction_deal": {"name": "networks/sample1/privateAuctionDeals/sample2"}
    }
    request_init["private_auction_deal"] = {
        "name": "networks/sample1/privateAuctionDeals/sample2",
        "private_auction_deal_id": 2414,
        "private_auction_id": 1913,
        "private_auction_display_name": "private_auction_display_name_value",
        "buyer_account_id": 1695,
        "external_deal_id": 1668,
        "targeting": {
            "geo_targeting": {
                "targeted_geos": ["targeted_geos_value1", "targeted_geos_value2"],
                "excluded_geos": ["excluded_geos_value1", "excluded_geos_value2"],
            },
            "technology_targeting": {
                "bandwidth_targeting": {
                    "targeted_bandwidth_groups": [
                        "targeted_bandwidth_groups_value1",
                        "targeted_bandwidth_groups_value2",
                    ],
                    "excluded_bandwidth_groups": [
                        "excluded_bandwidth_groups_value1",
                        "excluded_bandwidth_groups_value2",
                    ],
                },
                "device_category_targeting": {
                    "targeted_categories": [
                        "targeted_categories_value1",
                        "targeted_categories_value2",
                    ],
                    "excluded_categories": [
                        "excluded_categories_value1",
                        "excluded_categories_value2",
                    ],
                },
                "operating_system_targeting": {
                    "targeted_operating_systems": [
                        "targeted_operating_systems_value1",
                        "targeted_operating_systems_value2",
                    ],
                    "excluded_operating_systems": [
                        "excluded_operating_systems_value1",
                        "excluded_operating_systems_value2",
                    ],
                    "targeted_operating_system_versions": [
                        "targeted_operating_system_versions_value1",
                        "targeted_operating_system_versions_value2",
                    ],
                    "excluded_operating_system_versions": [
                        "excluded_operating_system_versions_value1",
                        "excluded_operating_system_versions_value2",
                    ],
                },
            },
            "inventory_targeting": {
                "targeted_ad_units": [
                    {"include_descendants": True, "ad_unit": "ad_unit_value"}
                ],
                "excluded_ad_units": {},
                "targeted_placements": [
                    "targeted_placements_value1",
                    "targeted_placements_value2",
                ],
            },
            "request_platform_targeting": {"request_platforms": [1]},
            "custom_targeting": {
                "custom_targeting_clauses": [
                    {
                        "custom_targeting_literals": [
                            {
                                "negative": True,
                                "custom_targeting_key": "custom_targeting_key_value",
                                "custom_targeting_values": [
                                    "custom_targeting_values_value1",
                                    "custom_targeting_values_value2",
                                ],
                            }
                        ]
                    }
                ]
            },
            "user_domain_targeting": {
                "targeted_user_domains": [
                    "targeted_user_domains_value1",
                    "targeted_user_domains_value2",
                ],
                "excluded_user_domains": [
                    "excluded_user_domains_value1",
                    "excluded_user_domains_value2",
                ],
            },
            "video_position_targeting": {
                "video_positions": [
                    {
                        "midroll_index": 1386,
                        "reverse_midroll_index": 2245,
                        "pod_position": 1303,
                        "position_type": 1,
                        "bumper_type": 1,
                    }
                ]
            },
            "data_segment_targeting": {"has_data_segment_targeting": True},
        },
        "end_time": {"seconds": 751, "nanos": 543},
        "floor_price": {
            "currency_code": "currency_code_value",
            "units": 563,
            "nanos": 543,
        },
        "creative_sizes": [{"width": 544, "height": 633, "size_type": 1}],
        "status": 1,
        "auction_priority_enabled": True,
        "block_override_enabled": True,
        "buyer_permission_type": 1,
        "buyer_data": {"buyer_emails": ["buyer_emails_value1", "buyer_emails_value2"]},
        "create_time": {},
        "update_time": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = (
        private_auction_deal_service.UpdatePrivateAuctionDealRequest.meta.fields[
            "private_auction_deal"
        ]
    )

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
        "private_auction_deal"
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
                for i in range(0, len(request_init["private_auction_deal"][field])):
                    del request_init["private_auction_deal"][field][i][subfield]
            else:
                del request_init["private_auction_deal"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_auction_deal_messages.PrivateAuctionDeal(
            name="name_value",
            private_auction_deal_id=2414,
            private_auction_id=1913,
            private_auction_display_name="private_auction_display_name_value",
            buyer_account_id=1695,
            external_deal_id=1668,
            status=private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING,
            auction_priority_enabled=True,
            block_override_enabled=True,
            buyer_permission_type=deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = private_auction_deal_messages.PrivateAuctionDeal.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_private_auction_deal(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, private_auction_deal_messages.PrivateAuctionDeal)
    assert response.name == "name_value"
    assert response.private_auction_deal_id == 2414
    assert response.private_auction_id == 1913
    assert response.private_auction_display_name == "private_auction_display_name_value"
    assert response.buyer_account_id == 1695
    assert response.external_deal_id == 1668
    assert (
        response.status
        == private_marketplace_enums.PrivateMarketplaceDealStatusEnum.PrivateMarketplaceDealStatus.PENDING
    )
    assert response.auction_priority_enabled is True
    assert response.block_override_enabled is True
    assert (
        response.buyer_permission_type
        == deal_buyer_permission_type_enum.DealBuyerPermissionTypeEnum.DealBuyerPermissionType.NEGOTIATOR_ONLY
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_private_auction_deal_rest_interceptors(null_interceptor):
    transport = transports.PrivateAuctionDealServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateAuctionDealServiceRestInterceptor(),
    )
    client = PrivateAuctionDealServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_update_private_auction_deal",
    ) as post, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "post_update_private_auction_deal_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.PrivateAuctionDealServiceRestInterceptor,
        "pre_update_private_auction_deal",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = private_auction_deal_service.UpdatePrivateAuctionDealRequest.pb(
            private_auction_deal_service.UpdatePrivateAuctionDealRequest()
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
        return_value = private_auction_deal_messages.PrivateAuctionDeal.to_json(
            private_auction_deal_messages.PrivateAuctionDeal()
        )
        req.return_value.content = return_value

        request = private_auction_deal_service.UpdatePrivateAuctionDealRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_auction_deal_messages.PrivateAuctionDeal()
        post_with_metadata.return_value = (
            private_auction_deal_messages.PrivateAuctionDeal(),
            metadata,
        )

        client.update_private_auction_deal(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_get_operation_rest_bad_request(
    request_type=operations_pb2.GetOperationRequest,
):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type()
    request = json_format.ParseDict(
        {"name": "networks/sample1/operations/reports/runs/sample2"}, request
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
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    request_init = {"name": "networks/sample1/operations/reports/runs/sample2"}
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


def test_initialize_client_w_rest():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_private_auction_deal_empty_call_rest():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_auction_deal), "__call__"
    ) as call:
        client.get_private_auction_deal(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = private_auction_deal_service.GetPrivateAuctionDealRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_private_auction_deals_empty_call_rest():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_auction_deals), "__call__"
    ) as call:
        client.list_private_auction_deals(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = private_auction_deal_service.ListPrivateAuctionDealsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_private_auction_deal_empty_call_rest():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_auction_deal), "__call__"
    ) as call:
        client.create_private_auction_deal(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = private_auction_deal_service.CreatePrivateAuctionDealRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_private_auction_deal_empty_call_rest():
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_private_auction_deal), "__call__"
    ) as call:
        client.update_private_auction_deal(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = private_auction_deal_service.UpdatePrivateAuctionDealRequest()

        assert args[0] == request_msg


def test_private_auction_deal_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.PrivateAuctionDealServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_private_auction_deal_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.ads.admanager_v1.services.private_auction_deal_service.transports.PrivateAuctionDealServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PrivateAuctionDealServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_private_auction_deal",
        "list_private_auction_deals",
        "create_private_auction_deal",
        "update_private_auction_deal",
        "get_operation",
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


def test_private_auction_deal_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.ads.admanager_v1.services.private_auction_deal_service.transports.PrivateAuctionDealServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PrivateAuctionDealServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/admanager",),
            quota_project_id="octopus",
        )


def test_private_auction_deal_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.ads.admanager_v1.services.private_auction_deal_service.transports.PrivateAuctionDealServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PrivateAuctionDealServiceTransport()
        adc.assert_called_once()


def test_private_auction_deal_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        PrivateAuctionDealServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/admanager",),
            quota_project_id=None,
        )


def test_private_auction_deal_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.PrivateAuctionDealServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_private_auction_deal_service_host_no_port(transport_name):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="admanager.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "admanager.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://admanager.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_private_auction_deal_service_host_with_port(transport_name):
    client = PrivateAuctionDealServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="admanager.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "admanager.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://admanager.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_private_auction_deal_service_client_transport_session_collision(
    transport_name,
):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = PrivateAuctionDealServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = PrivateAuctionDealServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_private_auction_deal._session
    session2 = client2.transport.get_private_auction_deal._session
    assert session1 != session2
    session1 = client1.transport.list_private_auction_deals._session
    session2 = client2.transport.list_private_auction_deals._session
    assert session1 != session2
    session1 = client1.transport.create_private_auction_deal._session
    session2 = client2.transport.create_private_auction_deal._session
    assert session1 != session2
    session1 = client1.transport.update_private_auction_deal._session
    session2 = client2.transport.update_private_auction_deal._session
    assert session1 != session2


def test_ad_unit_path():
    network_code = "squid"
    ad_unit = "clam"
    expected = "networks/{network_code}/adUnits/{ad_unit}".format(
        network_code=network_code,
        ad_unit=ad_unit,
    )
    actual = PrivateAuctionDealServiceClient.ad_unit_path(network_code, ad_unit)
    assert expected == actual


def test_parse_ad_unit_path():
    expected = {
        "network_code": "whelk",
        "ad_unit": "octopus",
    }
    path = PrivateAuctionDealServiceClient.ad_unit_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_ad_unit_path(path)
    assert expected == actual


def test_bandwidth_group_path():
    network_code = "oyster"
    bandwidth_group = "nudibranch"
    expected = "networks/{network_code}/bandwidthGroups/{bandwidth_group}".format(
        network_code=network_code,
        bandwidth_group=bandwidth_group,
    )
    actual = PrivateAuctionDealServiceClient.bandwidth_group_path(
        network_code, bandwidth_group
    )
    assert expected == actual


def test_parse_bandwidth_group_path():
    expected = {
        "network_code": "cuttlefish",
        "bandwidth_group": "mussel",
    }
    path = PrivateAuctionDealServiceClient.bandwidth_group_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_bandwidth_group_path(path)
    assert expected == actual


def test_custom_targeting_key_path():
    network_code = "winkle"
    custom_targeting_key = "nautilus"
    expected = (
        "networks/{network_code}/customTargetingKeys/{custom_targeting_key}".format(
            network_code=network_code,
            custom_targeting_key=custom_targeting_key,
        )
    )
    actual = PrivateAuctionDealServiceClient.custom_targeting_key_path(
        network_code, custom_targeting_key
    )
    assert expected == actual


def test_parse_custom_targeting_key_path():
    expected = {
        "network_code": "scallop",
        "custom_targeting_key": "abalone",
    }
    path = PrivateAuctionDealServiceClient.custom_targeting_key_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_custom_targeting_key_path(path)
    assert expected == actual


def test_custom_targeting_value_path():
    network_code = "squid"
    custom_targeting_value = "clam"
    expected = (
        "networks/{network_code}/customTargetingValues/{custom_targeting_value}".format(
            network_code=network_code,
            custom_targeting_value=custom_targeting_value,
        )
    )
    actual = PrivateAuctionDealServiceClient.custom_targeting_value_path(
        network_code, custom_targeting_value
    )
    assert expected == actual


def test_parse_custom_targeting_value_path():
    expected = {
        "network_code": "whelk",
        "custom_targeting_value": "octopus",
    }
    path = PrivateAuctionDealServiceClient.custom_targeting_value_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_custom_targeting_value_path(path)
    assert expected == actual


def test_device_category_path():
    network_code = "oyster"
    device_category = "nudibranch"
    expected = "networks/{network_code}/deviceCategories/{device_category}".format(
        network_code=network_code,
        device_category=device_category,
    )
    actual = PrivateAuctionDealServiceClient.device_category_path(
        network_code, device_category
    )
    assert expected == actual


def test_parse_device_category_path():
    expected = {
        "network_code": "cuttlefish",
        "device_category": "mussel",
    }
    path = PrivateAuctionDealServiceClient.device_category_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_device_category_path(path)
    assert expected == actual


def test_geo_target_path():
    network_code = "winkle"
    geo_target = "nautilus"
    expected = "networks/{network_code}/geoTargets/{geo_target}".format(
        network_code=network_code,
        geo_target=geo_target,
    )
    actual = PrivateAuctionDealServiceClient.geo_target_path(network_code, geo_target)
    assert expected == actual


def test_parse_geo_target_path():
    expected = {
        "network_code": "scallop",
        "geo_target": "abalone",
    }
    path = PrivateAuctionDealServiceClient.geo_target_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_geo_target_path(path)
    assert expected == actual


def test_network_path():
    network_code = "squid"
    expected = "networks/{network_code}".format(
        network_code=network_code,
    )
    actual = PrivateAuctionDealServiceClient.network_path(network_code)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "network_code": "clam",
    }
    path = PrivateAuctionDealServiceClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_network_path(path)
    assert expected == actual


def test_operating_system_path():
    network_code = "whelk"
    operating_system = "octopus"
    expected = "networks/{network_code}/operatingSystems/{operating_system}".format(
        network_code=network_code,
        operating_system=operating_system,
    )
    actual = PrivateAuctionDealServiceClient.operating_system_path(
        network_code, operating_system
    )
    assert expected == actual


def test_parse_operating_system_path():
    expected = {
        "network_code": "oyster",
        "operating_system": "nudibranch",
    }
    path = PrivateAuctionDealServiceClient.operating_system_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_operating_system_path(path)
    assert expected == actual


def test_operating_system_version_path():
    network_code = "cuttlefish"
    operating_system_version = "mussel"
    expected = "networks/{network_code}/operatingSystemVersions/{operating_system_version}".format(
        network_code=network_code,
        operating_system_version=operating_system_version,
    )
    actual = PrivateAuctionDealServiceClient.operating_system_version_path(
        network_code, operating_system_version
    )
    assert expected == actual


def test_parse_operating_system_version_path():
    expected = {
        "network_code": "winkle",
        "operating_system_version": "nautilus",
    }
    path = PrivateAuctionDealServiceClient.operating_system_version_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_operating_system_version_path(path)
    assert expected == actual


def test_placement_path():
    network_code = "scallop"
    placement = "abalone"
    expected = "networks/{network_code}/placements/{placement}".format(
        network_code=network_code,
        placement=placement,
    )
    actual = PrivateAuctionDealServiceClient.placement_path(network_code, placement)
    assert expected == actual


def test_parse_placement_path():
    expected = {
        "network_code": "squid",
        "placement": "clam",
    }
    path = PrivateAuctionDealServiceClient.placement_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_placement_path(path)
    assert expected == actual


def test_private_auction_deal_path():
    network_code = "whelk"
    private_auction_deal = "octopus"
    expected = (
        "networks/{network_code}/privateAuctionDeals/{private_auction_deal}".format(
            network_code=network_code,
            private_auction_deal=private_auction_deal,
        )
    )
    actual = PrivateAuctionDealServiceClient.private_auction_deal_path(
        network_code, private_auction_deal
    )
    assert expected == actual


def test_parse_private_auction_deal_path():
    expected = {
        "network_code": "oyster",
        "private_auction_deal": "nudibranch",
    }
    path = PrivateAuctionDealServiceClient.private_auction_deal_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_private_auction_deal_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = PrivateAuctionDealServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = PrivateAuctionDealServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = PrivateAuctionDealServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = PrivateAuctionDealServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = PrivateAuctionDealServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = PrivateAuctionDealServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = PrivateAuctionDealServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = PrivateAuctionDealServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = PrivateAuctionDealServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = PrivateAuctionDealServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateAuctionDealServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.PrivateAuctionDealServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = PrivateAuctionDealServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.PrivateAuctionDealServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = PrivateAuctionDealServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_rest():
    client = PrivateAuctionDealServiceClient(
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
    ]
    for transport in transports:
        client = PrivateAuctionDealServiceClient(
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
            PrivateAuctionDealServiceClient,
            transports.PrivateAuctionDealServiceRestTransport,
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
