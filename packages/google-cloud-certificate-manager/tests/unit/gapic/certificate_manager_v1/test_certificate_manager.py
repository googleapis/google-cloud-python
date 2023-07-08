# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2
from google.oauth2 import service_account
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

from google.cloud.certificate_manager_v1.services.certificate_manager import (
    CertificateManagerAsyncClient,
    CertificateManagerClient,
    pagers,
    transports,
)
from google.cloud.certificate_manager_v1.types import certificate_issuance_config
from google.cloud.certificate_manager_v1.types import (
    certificate_issuance_config as gcc_certificate_issuance_config,
)
from google.cloud.certificate_manager_v1.types import certificate_manager


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


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CertificateManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CertificateManagerClient, "grpc"),
        (CertificateManagerAsyncClient, "grpc_asyncio"),
        (CertificateManagerClient, "rest"),
    ],
)
def test_certificate_manager_client_from_service_account_info(
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
            "certificatemanager.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://certificatemanager.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CertificateManagerGrpcTransport, "grpc"),
        (transports.CertificateManagerGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CertificateManagerRestTransport, "rest"),
    ],
)
def test_certificate_manager_client_service_account_always_use_jwt(
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
        (CertificateManagerClient, "grpc"),
        (CertificateManagerAsyncClient, "grpc_asyncio"),
        (CertificateManagerClient, "rest"),
    ],
)
def test_certificate_manager_client_from_service_account_file(
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
            "certificatemanager.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://certificatemanager.googleapis.com"
        )


def test_certificate_manager_client_get_transport_class():
    transport = CertificateManagerClient.get_transport_class()
    available_transports = [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerRestTransport,
    ]
    assert transport in available_transports

    transport = CertificateManagerClient.get_transport_class("grpc")
    assert transport == transports.CertificateManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport, "grpc"),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CertificateManagerClient, transports.CertificateManagerRestTransport, "rest"),
    ],
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
def test_certificate_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CertificateManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CertificateManagerClient, "get_transport_class") as gtc:
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
                host=client.DEFAULT_ENDPOINT,
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
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
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
            host=client.DEFAULT_ENDPOINT,
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
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            "true",
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            "false",
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            CertificateManagerClient,
            transports.CertificateManagerRestTransport,
            "rest",
            "true",
        ),
        (
            CertificateManagerClient,
            transports.CertificateManagerRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_certificate_manager_client_mtls_env_auto(
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
                expected_host = client.DEFAULT_ENDPOINT
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
                        expected_host = client.DEFAULT_ENDPOINT
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
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [CertificateManagerClient, CertificateManagerAsyncClient]
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
def test_certificate_manager_client_get_mtls_endpoint_and_cert_source(client_class):
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


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport, "grpc"),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CertificateManagerClient, transports.CertificateManagerRestTransport, "rest"),
    ],
)
def test_certificate_manager_client_client_options_scopes(
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
            host=client.DEFAULT_ENDPOINT,
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
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            CertificateManagerClient,
            transports.CertificateManagerRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_certificate_manager_client_client_options_credentials_file(
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
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_certificate_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CertificateManagerClient(
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
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_certificate_manager_client_create_channel_credentials_file(
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
            host=client.DEFAULT_ENDPOINT,
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
            "certificatemanager.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="certificatemanager.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificatesRequest,
        dict,
    ],
)
def test_list_certificates(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        client.list_certificates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()


@pytest.mark.asyncio
async def test_list_certificates_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificatesRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificates_async_from_dict():
    await test_list_certificates_async(request_type=dict)


def test_list_certificates_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificatesResponse()
        client.list_certificates(request)

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
async def test_list_certificates_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse()
        )
        await client.list_certificates(request)

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


def test_list_certificates_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificates(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificates_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificates(
            certificate_manager.ListCertificatesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificates_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificates(
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
async def test_list_certificates_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificates(
            certificate_manager.ListCertificatesRequest(),
            parent="parent_value",
        )


def test_list_certificates_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificates(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.Certificate) for i in results)


def test_list_certificates_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificates_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificates(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, certificate_manager.Certificate) for i in responses)


@pytest.mark.asyncio
async def test_list_certificates_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_certificates(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateRequest,
        dict,
    ],
)
def test_get_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate(
            name="name_value",
            description="description_value",
            san_dnsnames=["san_dnsnames_value"],
            pem_certificate="pem_certificate_value",
            scope=certificate_manager.Certificate.Scope.EDGE_CACHE,
        )
        response = client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.Certificate)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.san_dnsnames == ["san_dnsnames_value"]
    assert response.pem_certificate == "pem_certificate_value"
    assert response.scope == certificate_manager.Certificate.Scope.EDGE_CACHE


def test_get_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        client.get_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()


@pytest.mark.asyncio
async def test_get_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate(
                name="name_value",
                description="description_value",
                san_dnsnames=["san_dnsnames_value"],
                pem_certificate="pem_certificate_value",
                scope=certificate_manager.Certificate.Scope.EDGE_CACHE,
            )
        )
        response = await client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.Certificate)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.san_dnsnames == ["san_dnsnames_value"]
    assert response.pem_certificate == "pem_certificate_value"
    assert response.scope == certificate_manager.Certificate.Scope.EDGE_CACHE


@pytest.mark.asyncio
async def test_get_certificate_async_from_dict():
    await test_get_certificate_async(request_type=dict)


def test_get_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = certificate_manager.Certificate()
        client.get_certificate(request)

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
async def test_get_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate()
        )
        await client.get_certificate(request)

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


def test_get_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate(
            certificate_manager.GetCertificateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate(
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
async def test_get_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate(
            certificate_manager.GetCertificateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateRequest,
        dict,
    ],
)
def test_create_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        client.create_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()


@pytest.mark.asyncio
async def test_create_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_async_from_dict():
    await test_create_certificate_async(request_type=dict)


def test_create_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate(request)

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
async def test_create_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate(request)

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


def test_create_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate(
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_id
        mock_val = "certificate_id_value"
        assert arg == mock_val


def test_create_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate(
            certificate_manager.CreateCertificateRequest(),
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate(
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_id
        mock_val = "certificate_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate(
            certificate_manager.CreateCertificateRequest(),
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateRequest,
        dict,
    ],
)
def test_update_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        client.update_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()


@pytest.mark.asyncio
async def test_update_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_async_from_dict():
    await test_update_certificate_async(request_type=dict)


def test_update_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateRequest()

    request.certificate.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateRequest()

    request.certificate.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate.name=name_value",
    ) in kw["metadata"]


def test_update_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate(
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate(
            certificate_manager.UpdateCertificateRequest(),
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate(
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate(
            certificate_manager.UpdateCertificateRequest(),
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateRequest,
        dict,
    ],
)
def test_delete_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        client.delete_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()


@pytest.mark.asyncio
async def test_delete_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_async_from_dict():
    await test_delete_certificate_async(request_type=dict)


def test_delete_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate(request)

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
async def test_delete_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate(request)

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


def test_delete_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate(
            certificate_manager.DeleteCertificateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate(
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
async def test_delete_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate(
            certificate_manager.DeleteCertificateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapsRequest,
        dict,
    ],
)
def test_list_certificate_maps(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificate_maps(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_maps_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        client.list_certificate_maps()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()


@pytest.mark.asyncio
async def test_list_certificate_maps_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificateMapsRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_maps(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_maps_async_from_dict():
    await test_list_certificate_maps_async(request_type=dict)


def test_list_certificate_maps_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificateMapsResponse()
        client.list_certificate_maps(request)

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
async def test_list_certificate_maps_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse()
        )
        await client.list_certificate_maps(request)

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


def test_list_certificate_maps_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_maps(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificate_maps_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_maps(
            certificate_manager.ListCertificateMapsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_maps_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_maps(
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
async def test_list_certificate_maps_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_maps(
            certificate_manager.ListCertificateMapsRequest(),
            parent="parent_value",
        )


def test_list_certificate_maps_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_maps(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.CertificateMap) for i in results)


def test_list_certificate_maps_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_maps(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_maps_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_maps(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, certificate_manager.CertificateMap) for i in responses)


@pytest.mark.asyncio
async def test_list_certificate_maps_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_certificate_maps(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapRequest,
        dict,
    ],
)
def test_get_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap(
            name="name_value",
            description="description_value",
        )
        response = client.get_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMap)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        client.get_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()


@pytest.mark.asyncio
async def test_get_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.get_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMap)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_certificate_map_async_from_dict():
    await test_get_certificate_map_async(request_type=dict)


def test_get_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        call.return_value = certificate_manager.CertificateMap()
        client.get_certificate_map(request)

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
async def test_get_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap()
        )
        await client.get_certificate_map(request)

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


def test_get_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_map(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map(
            certificate_manager.GetCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_map(
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
async def test_get_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_map(
            certificate_manager.GetCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapRequest,
        dict,
    ],
)
def test_create_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        client.create_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()


@pytest.mark.asyncio
async def test_create_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_map_async_from_dict():
    await test_create_certificate_map_async(request_type=dict)


def test_create_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_map(request)

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
async def test_create_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_map(request)

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


def test_create_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_map(
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_id
        mock_val = "certificate_map_id_value"
        assert arg == mock_val


def test_create_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map(
            certificate_manager.CreateCertificateMapRequest(),
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_map(
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_id
        mock_val = "certificate_map_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_map(
            certificate_manager.CreateCertificateMapRequest(),
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapRequest,
        dict,
    ],
)
def test_update_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        client.update_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()


@pytest.mark.asyncio
async def test_update_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_map_async_from_dict():
    await test_update_certificate_map_async(request_type=dict)


def test_update_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapRequest()

    request.certificate_map.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapRequest()

    request.certificate_map.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map.name=name_value",
    ) in kw["metadata"]


def test_update_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_map(
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map(
            certificate_manager.UpdateCertificateMapRequest(),
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_map(
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_map(
            certificate_manager.UpdateCertificateMapRequest(),
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapRequest,
        dict,
    ],
)
def test_delete_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        client.delete_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()


@pytest.mark.asyncio
async def test_delete_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_map_async_from_dict():
    await test_delete_certificate_map_async(request_type=dict)


def test_delete_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_map(request)

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
async def test_delete_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_map(request)

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


def test_delete_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_map(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map(
            certificate_manager.DeleteCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_map(
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
async def test_delete_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_map(
            certificate_manager.DeleteCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapEntriesRequest,
        dict,
    ],
)
def test_list_certificate_map_entries(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificate_map_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapEntriesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_map_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        client.list_certificate_map_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificateMapEntriesRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_map_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapEntriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_from_dict():
    await test_list_certificate_map_entries_async(request_type=dict)


def test_list_certificate_map_entries_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()
        client.list_certificate_map_entries(request)

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
async def test_list_certificate_map_entries_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse()
        )
        await client.list_certificate_map_entries(request)

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


def test_list_certificate_map_entries_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_map_entries(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificate_map_entries_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_map_entries(
            certificate_manager.ListCertificateMapEntriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_map_entries_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_map_entries(
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
async def test_list_certificate_map_entries_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_map_entries(
            certificate_manager.ListCertificateMapEntriesRequest(),
            parent="parent_value",
        )


def test_list_certificate_map_entries_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_map_entries(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, certificate_manager.CertificateMapEntry) for i in results
        )


def test_list_certificate_map_entries_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_map_entries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_map_entries(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, certificate_manager.CertificateMapEntry) for i in responses
        )


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_certificate_map_entries(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapEntryRequest,
        dict,
    ],
)
def test_get_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry(
            name="name_value",
            description="description_value",
            certificates=["certificates_value"],
            state=certificate_manager.ServingState.ACTIVE,
            hostname="hostname_value",
        )
        response = client.get_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMapEntry)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.certificates == ["certificates_value"]
    assert response.state == certificate_manager.ServingState.ACTIVE


def test_get_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        client.get_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_get_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry(
                name="name_value",
                description="description_value",
                certificates=["certificates_value"],
                state=certificate_manager.ServingState.ACTIVE,
            )
        )
        response = await client.get_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMapEntry)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.certificates == ["certificates_value"]
    assert response.state == certificate_manager.ServingState.ACTIVE


@pytest.mark.asyncio
async def test_get_certificate_map_entry_async_from_dict():
    await test_get_certificate_map_entry_async(request_type=dict)


def test_get_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = certificate_manager.CertificateMapEntry()
        client.get_certificate_map_entry(request)

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
async def test_get_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry()
        )
        await client.get_certificate_map_entry(request)

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


def test_get_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_map_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map_entry(
            certificate_manager.GetCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_map_entry(
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
async def test_get_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_map_entry(
            certificate_manager.GetCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapEntryRequest,
        dict,
    ],
)
def test_create_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        client.create_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_create_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_map_entry_async_from_dict():
    await test_create_certificate_map_entry_async(request_type=dict)


def test_create_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapEntryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_map_entry(request)

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
async def test_create_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapEntryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_map_entry(request)

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


def test_create_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_map_entry(
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_entry_id
        mock_val = "certificate_map_entry_id_value"
        assert arg == mock_val


def test_create_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map_entry(
            certificate_manager.CreateCertificateMapEntryRequest(),
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_map_entry(
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_entry_id
        mock_val = "certificate_map_entry_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_map_entry(
            certificate_manager.CreateCertificateMapEntryRequest(),
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapEntryRequest,
        dict,
    ],
)
def test_update_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        client.update_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_update_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_map_entry_async_from_dict():
    await test_update_certificate_map_entry_async(request_type=dict)


def test_update_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapEntryRequest()

    request.certificate_map_entry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map_entry.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapEntryRequest()

    request.certificate_map_entry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map_entry.name=name_value",
    ) in kw["metadata"]


def test_update_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_map_entry(
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map_entry(
            certificate_manager.UpdateCertificateMapEntryRequest(),
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_map_entry(
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_map_entry(
            certificate_manager.UpdateCertificateMapEntryRequest(),
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapEntryRequest,
        dict,
    ],
)
def test_delete_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        client.delete_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_async_from_dict():
    await test_delete_certificate_map_entry_async(request_type=dict)


def test_delete_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_map_entry(request)

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
async def test_delete_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_map_entry(request)

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


def test_delete_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_map_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map_entry(
            certificate_manager.DeleteCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_map_entry(
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
async def test_delete_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_map_entry(
            certificate_manager.DeleteCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListDnsAuthorizationsRequest,
        dict,
    ],
)
def test_list_dns_authorizations(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_dns_authorizations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDnsAuthorizationsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_dns_authorizations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        client.list_dns_authorizations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()


@pytest.mark.asyncio
async def test_list_dns_authorizations_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListDnsAuthorizationsRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_dns_authorizations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDnsAuthorizationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_from_dict():
    await test_list_dns_authorizations_async(request_type=dict)


def test_list_dns_authorizations_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListDnsAuthorizationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()
        client.list_dns_authorizations(request)

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
async def test_list_dns_authorizations_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListDnsAuthorizationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse()
        )
        await client.list_dns_authorizations(request)

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


def test_list_dns_authorizations_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_dns_authorizations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_dns_authorizations_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dns_authorizations(
            certificate_manager.ListDnsAuthorizationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_dns_authorizations_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_dns_authorizations(
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
async def test_list_dns_authorizations_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_dns_authorizations(
            certificate_manager.ListDnsAuthorizationsRequest(),
            parent="parent_value",
        )


def test_list_dns_authorizations_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_dns_authorizations(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.DnsAuthorization) for i in results)


def test_list_dns_authorizations_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_dns_authorizations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_dns_authorizations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, certificate_manager.DnsAuthorization) for i in responses
        )


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_dns_authorizations(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetDnsAuthorizationRequest,
        dict,
    ],
)
def test_get_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization(
            name="name_value",
            description="description_value",
            domain="domain_value",
        )
        response = client.get_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.DnsAuthorization)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.domain == "domain_value"


def test_get_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        client.get_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_get_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization(
                name="name_value",
                description="description_value",
                domain="domain_value",
            )
        )
        response = await client.get_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.DnsAuthorization)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.domain == "domain_value"


@pytest.mark.asyncio
async def test_get_dns_authorization_async_from_dict():
    await test_get_dns_authorization_async(request_type=dict)


def test_get_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetDnsAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        call.return_value = certificate_manager.DnsAuthorization()
        client.get_dns_authorization(request)

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
async def test_get_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetDnsAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization()
        )
        await client.get_dns_authorization(request)

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


def test_get_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dns_authorization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dns_authorization(
            certificate_manager.GetDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dns_authorization(
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
async def test_get_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dns_authorization(
            certificate_manager.GetDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateDnsAuthorizationRequest,
        dict,
    ],
)
def test_create_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        client.create_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_create_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_dns_authorization_async_from_dict():
    await test_create_dns_authorization_async(request_type=dict)


def test_create_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateDnsAuthorizationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_dns_authorization(request)

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
async def test_create_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateDnsAuthorizationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_dns_authorization(request)

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


def test_create_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dns_authorization(
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].dns_authorization_id
        mock_val = "dns_authorization_id_value"
        assert arg == mock_val


def test_create_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dns_authorization(
            certificate_manager.CreateDnsAuthorizationRequest(),
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )


@pytest.mark.asyncio
async def test_create_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dns_authorization(
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].dns_authorization_id
        mock_val = "dns_authorization_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dns_authorization(
            certificate_manager.CreateDnsAuthorizationRequest(),
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateDnsAuthorizationRequest,
        dict,
    ],
)
def test_update_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        client.update_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_update_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_dns_authorization_async_from_dict():
    await test_update_dns_authorization_async(request_type=dict)


def test_update_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateDnsAuthorizationRequest()

    request.dns_authorization.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dns_authorization.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateDnsAuthorizationRequest()

    request.dns_authorization.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dns_authorization.name=name_value",
    ) in kw["metadata"]


def test_update_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_dns_authorization(
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dns_authorization(
            certificate_manager.UpdateDnsAuthorizationRequest(),
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_dns_authorization(
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_dns_authorization(
            certificate_manager.UpdateDnsAuthorizationRequest(),
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteDnsAuthorizationRequest,
        dict,
    ],
)
def test_delete_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        client.delete_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_delete_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_dns_authorization_async_from_dict():
    await test_delete_dns_authorization_async(request_type=dict)


def test_delete_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteDnsAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_dns_authorization(request)

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
async def test_delete_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteDnsAuthorizationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_dns_authorization(request)

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


def test_delete_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dns_authorization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dns_authorization(
            certificate_manager.DeleteDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dns_authorization(
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
async def test_delete_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dns_authorization(
            certificate_manager.DeleteDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.ListCertificateIssuanceConfigsRequest,
        dict,
    ],
)
def test_list_certificate_issuance_configs(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = client.list_certificate_issuance_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.ListCertificateIssuanceConfigsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateIssuanceConfigsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_issuance_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        client.list_certificate_issuance_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.ListCertificateIssuanceConfigsRequest()
        )


@pytest.mark.asyncio
async def test_list_certificate_issuance_configs_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_issuance_config.ListCertificateIssuanceConfigsRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_issuance_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.ListCertificateIssuanceConfigsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateIssuanceConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_issuance_configs_async_from_dict():
    await test_list_certificate_issuance_configs_async(request_type=dict)


def test_list_certificate_issuance_configs_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.ListCertificateIssuanceConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        call.return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )
        client.list_certificate_issuance_configs(request)

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
async def test_list_certificate_issuance_configs_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.ListCertificateIssuanceConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )
        await client.list_certificate_issuance_configs(request)

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


def test_list_certificate_issuance_configs_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_issuance_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificate_issuance_configs_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_issuance_configs(
            certificate_issuance_config.ListCertificateIssuanceConfigsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_issuance_configs_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_issuance_configs(
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
async def test_list_certificate_issuance_configs_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_issuance_configs(
            certificate_issuance_config.ListCertificateIssuanceConfigsRequest(),
            parent="parent_value",
        )


def test_list_certificate_issuance_configs_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="abc",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[],
                next_page_token="def",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="ghi",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_issuance_configs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, certificate_issuance_config.CertificateIssuanceConfig)
            for i in results
        )


def test_list_certificate_issuance_configs_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="abc",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[],
                next_page_token="def",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="ghi",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_issuance_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_issuance_configs_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="abc",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[],
                next_page_token="def",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="ghi",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_issuance_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, certificate_issuance_config.CertificateIssuanceConfig)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_certificate_issuance_configs_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_issuance_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="abc",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[],
                next_page_token="def",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="ghi",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_certificate_issuance_configs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.GetCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_get_certificate_issuance_config(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_issuance_config.CertificateIssuanceConfig(
            name="name_value",
            description="description_value",
            rotation_window_percentage=2788,
            key_algorithm=certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048,
        )
        response = client.get_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == certificate_issuance_config.GetCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_issuance_config.CertificateIssuanceConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.rotation_window_percentage == 2788
    assert (
        response.key_algorithm
        == certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048
    )


def test_get_certificate_issuance_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        client.get_certificate_issuance_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == certificate_issuance_config.GetCertificateIssuanceConfigRequest()
        )


@pytest.mark.asyncio
async def test_get_certificate_issuance_config_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_issuance_config.GetCertificateIssuanceConfigRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value",
                description="description_value",
                rotation_window_percentage=2788,
                key_algorithm=certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048,
            )
        )
        response = await client.get_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == certificate_issuance_config.GetCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_issuance_config.CertificateIssuanceConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.rotation_window_percentage == 2788
    assert (
        response.key_algorithm
        == certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048
    )


@pytest.mark.asyncio
async def test_get_certificate_issuance_config_async_from_dict():
    await test_get_certificate_issuance_config_async(request_type=dict)


def test_get_certificate_issuance_config_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.GetCertificateIssuanceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = certificate_issuance_config.CertificateIssuanceConfig()
        client.get_certificate_issuance_config(request)

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
async def test_get_certificate_issuance_config_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.GetCertificateIssuanceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.CertificateIssuanceConfig()
        )
        await client.get_certificate_issuance_config(request)

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


def test_get_certificate_issuance_config_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_issuance_config.CertificateIssuanceConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_issuance_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_issuance_config_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_issuance_config(
            certificate_issuance_config.GetCertificateIssuanceConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_issuance_config_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_issuance_config.CertificateIssuanceConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_issuance_config.CertificateIssuanceConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_issuance_config(
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
async def test_get_certificate_issuance_config_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_issuance_config(
            certificate_issuance_config.GetCertificateIssuanceConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_create_certificate_issuance_config(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_issuance_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        client.create_certificate_issuance_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()
        )


@pytest.mark.asyncio
async def test_create_certificate_issuance_config_async(
    transport: str = "grpc_asyncio",
    request_type=gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_issuance_config_async_from_dict():
    await test_create_certificate_issuance_config_async(request_type=dict)


def test_create_certificate_issuance_config_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_issuance_config(request)

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
async def test_create_certificate_issuance_config_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_issuance_config(request)

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


def test_create_certificate_issuance_config_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_issuance_config(
            parent="parent_value",
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_issuance_config
        mock_val = gcc_certificate_issuance_config.CertificateIssuanceConfig(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].certificate_issuance_config_id
        mock_val = "certificate_issuance_config_id_value"
        assert arg == mock_val


def test_create_certificate_issuance_config_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_issuance_config(
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest(),
            parent="parent_value",
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_issuance_config_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_issuance_config(
            parent="parent_value",
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_issuance_config
        mock_val = gcc_certificate_issuance_config.CertificateIssuanceConfig(
            name="name_value"
        )
        assert arg == mock_val
        arg = args[0].certificate_issuance_config_id
        mock_val = "certificate_issuance_config_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_issuance_config_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_issuance_config(
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest(),
            parent="parent_value",
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.DeleteCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_delete_certificate_issuance_config(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_issuance_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        client.delete_certificate_issuance_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()
        )


@pytest.mark.asyncio
async def test_delete_certificate_issuance_config_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_issuance_config.DeleteCertificateIssuanceConfigRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_issuance_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_issuance_config_async_from_dict():
    await test_delete_certificate_issuance_config_async(request_type=dict)


def test_delete_certificate_issuance_config_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_issuance_config(request)

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
async def test_delete_certificate_issuance_config_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_issuance_config(request)

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


def test_delete_certificate_issuance_config_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_issuance_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_issuance_config_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_issuance_config(
            certificate_issuance_config.DeleteCertificateIssuanceConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_issuance_config_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_issuance_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_issuance_config(
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
async def test_delete_certificate_issuance_config_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_issuance_config(
            certificate_issuance_config.DeleteCertificateIssuanceConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificatesRequest,
        dict,
    ],
)
def test_list_certificates_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificatesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.ListCertificatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_certificates(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificates_rest_required_fields(
    request_type=certificate_manager.ListCertificatesRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificates._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificates._get_unset_required_fields(jsonified_request)
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

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.ListCertificatesResponse()
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

            pb_return_value = certificate_manager.ListCertificatesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_certificates(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_certificates_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_certificates._get_unset_required_fields({})
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
def test_list_certificates_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_list_certificates"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_list_certificates"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.ListCertificatesRequest.pb(
            certificate_manager.ListCertificatesRequest()
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
            certificate_manager.ListCertificatesResponse.to_json(
                certificate_manager.ListCertificatesResponse()
            )
        )

        request = certificate_manager.ListCertificatesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.ListCertificatesResponse()

        client.list_certificates(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_certificates_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.ListCertificatesRequest
):
    client = CertificateManagerClient(
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
        client.list_certificates(request)


def test_list_certificates_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificatesResponse()

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
        pb_return_value = certificate_manager.ListCertificatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_certificates(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificates"
            % client.transport._host,
            args[1],
        )


def test_list_certificates_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificates(
            certificate_manager.ListCertificatesRequest(),
            parent="parent_value",
        )


def test_list_certificates_rest_pager(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            certificate_manager.ListCertificatesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_certificates(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.Certificate) for i in results)

        pages = list(client.list_certificates(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateRequest,
        dict,
    ],
)
def test_get_certificate_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/certificates/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.Certificate(
            name="name_value",
            description="description_value",
            san_dnsnames=["san_dnsnames_value"],
            pem_certificate="pem_certificate_value",
            scope=certificate_manager.Certificate.Scope.EDGE_CACHE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.Certificate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_certificate(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.Certificate)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.san_dnsnames == ["san_dnsnames_value"]
    assert response.pem_certificate == "pem_certificate_value"
    assert response.scope == certificate_manager.Certificate.Scope.EDGE_CACHE


def test_get_certificate_rest_required_fields(
    request_type=certificate_manager.GetCertificateRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.Certificate()
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

            pb_return_value = certificate_manager.Certificate.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_certificate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_certificate_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_certificate._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_certificate_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_get_certificate"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_get_certificate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.GetCertificateRequest.pb(
            certificate_manager.GetCertificateRequest()
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
        req.return_value._content = certificate_manager.Certificate.to_json(
            certificate_manager.Certificate()
        )

        request = certificate_manager.GetCertificateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.Certificate()

        client.get_certificate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_certificate_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.GetCertificateRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/certificates/sample3"}
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
        client.get_certificate(request)


def test_get_certificate_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.Certificate()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificates/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.Certificate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_certificate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificates/*}"
            % client.transport._host,
            args[1],
        )


def test_get_certificate_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate(
            certificate_manager.GetCertificateRequest(),
            name="name_value",
        )


def test_get_certificate_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateRequest,
        dict,
    ],
)
def test_create_certificate_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "self_managed": {
            "pem_certificate": "pem_certificate_value",
            "pem_private_key": "pem_private_key_value",
        },
        "managed": {
            "domains": ["domains_value1", "domains_value2"],
            "dns_authorizations": [
                "dns_authorizations_value1",
                "dns_authorizations_value2",
            ],
            "issuance_config": "issuance_config_value",
            "state": 1,
            "provisioning_issue": {"reason": 1, "details": "details_value"},
            "authorization_attempt_info": [
                {
                    "domain": "domain_value",
                    "state": 1,
                    "failure_reason": 1,
                    "details": "details_value",
                }
            ],
        },
        "san_dnsnames": ["san_dnsnames_value1", "san_dnsnames_value2"],
        "pem_certificate": "pem_certificate_value",
        "expire_time": {},
        "scope": 1,
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
        response = client.create_certificate(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_certificate_rest_required_fields(
    request_type=certificate_manager.CreateCertificateRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["certificate_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "certificateId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "certificateId" in jsonified_request
    assert jsonified_request["certificateId"] == request_init["certificate_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["certificateId"] = "certificate_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("certificate_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "certificateId" in jsonified_request
    assert jsonified_request["certificateId"] == "certificate_id_value"

    client = CertificateManagerClient(
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

            response = client.create_certificate(request)

            expected_params = [
                (
                    "certificateId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_certificate_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_certificate._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("certificateId",))
        & set(
            (
                "parent",
                "certificateId",
                "certificate",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_certificate_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_create_certificate"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_create_certificate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.CreateCertificateRequest.pb(
            certificate_manager.CreateCertificateRequest()
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

        request = certificate_manager.CreateCertificateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_certificate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_certificate_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.CreateCertificateRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "self_managed": {
            "pem_certificate": "pem_certificate_value",
            "pem_private_key": "pem_private_key_value",
        },
        "managed": {
            "domains": ["domains_value1", "domains_value2"],
            "dns_authorizations": [
                "dns_authorizations_value1",
                "dns_authorizations_value2",
            ],
            "issuance_config": "issuance_config_value",
            "state": 1,
            "provisioning_issue": {"reason": 1, "details": "details_value"},
            "authorization_attempt_info": [
                {
                    "domain": "domain_value",
                    "state": 1,
                    "failure_reason": 1,
                    "details": "details_value",
                }
            ],
        },
        "san_dnsnames": ["san_dnsnames_value1", "san_dnsnames_value2"],
        "pem_certificate": "pem_certificate_value",
        "expire_time": {},
        "scope": 1,
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
        client.create_certificate(request)


def test_create_certificate_rest_flattened():
    client = CertificateManagerClient(
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
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_certificate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificates"
            % client.transport._host,
            args[1],
        )


def test_create_certificate_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate(
            certificate_manager.CreateCertificateRequest(),
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


def test_create_certificate_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateRequest,
        dict,
    ],
)
def test_update_certificate_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate": {
            "name": "projects/sample1/locations/sample2/certificates/sample3"
        }
    }
    request_init["certificate"] = {
        "name": "projects/sample1/locations/sample2/certificates/sample3",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "self_managed": {
            "pem_certificate": "pem_certificate_value",
            "pem_private_key": "pem_private_key_value",
        },
        "managed": {
            "domains": ["domains_value1", "domains_value2"],
            "dns_authorizations": [
                "dns_authorizations_value1",
                "dns_authorizations_value2",
            ],
            "issuance_config": "issuance_config_value",
            "state": 1,
            "provisioning_issue": {"reason": 1, "details": "details_value"},
            "authorization_attempt_info": [
                {
                    "domain": "domain_value",
                    "state": 1,
                    "failure_reason": 1,
                    "details": "details_value",
                }
            ],
        },
        "san_dnsnames": ["san_dnsnames_value1", "san_dnsnames_value2"],
        "pem_certificate": "pem_certificate_value",
        "expire_time": {},
        "scope": 1,
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
        response = client.update_certificate(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_certificate_rest_required_fields(
    request_type=certificate_manager.UpdateCertificateRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CertificateManagerClient(
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

            response = client.update_certificate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_certificate_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_certificate._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "certificate",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_certificate_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_update_certificate"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_update_certificate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.UpdateCertificateRequest.pb(
            certificate_manager.UpdateCertificateRequest()
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

        request = certificate_manager.UpdateCertificateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_certificate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_certificate_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.UpdateCertificateRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate": {
            "name": "projects/sample1/locations/sample2/certificates/sample3"
        }
    }
    request_init["certificate"] = {
        "name": "projects/sample1/locations/sample2/certificates/sample3",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "self_managed": {
            "pem_certificate": "pem_certificate_value",
            "pem_private_key": "pem_private_key_value",
        },
        "managed": {
            "domains": ["domains_value1", "domains_value2"],
            "dns_authorizations": [
                "dns_authorizations_value1",
                "dns_authorizations_value2",
            ],
            "issuance_config": "issuance_config_value",
            "state": 1,
            "provisioning_issue": {"reason": 1, "details": "details_value"},
            "authorization_attempt_info": [
                {
                    "domain": "domain_value",
                    "state": 1,
                    "failure_reason": 1,
                    "details": "details_value",
                }
            ],
        },
        "san_dnsnames": ["san_dnsnames_value1", "san_dnsnames_value2"],
        "pem_certificate": "pem_certificate_value",
        "expire_time": {},
        "scope": 1,
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
        client.update_certificate(request)


def test_update_certificate_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "certificate": {
                "name": "projects/sample1/locations/sample2/certificates/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_certificate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{certificate.name=projects/*/locations/*/certificates/*}"
            % client.transport._host,
            args[1],
        )


def test_update_certificate_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate(
            certificate_manager.UpdateCertificateRequest(),
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_certificate_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateRequest,
        dict,
    ],
)
def test_delete_certificate_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/certificates/sample3"}
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
        response = client.delete_certificate(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_certificate_rest_required_fields(
    request_type=certificate_manager.DeleteCertificateRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
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

            response = client.delete_certificate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_certificate_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_certificate._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_certificate_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_delete_certificate"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_delete_certificate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.DeleteCertificateRequest.pb(
            certificate_manager.DeleteCertificateRequest()
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

        request = certificate_manager.DeleteCertificateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_certificate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_certificate_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.DeleteCertificateRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/certificates/sample3"}
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
        client.delete_certificate(request)


def test_delete_certificate_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificates/sample3"
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

        client.delete_certificate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificates/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_certificate_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate(
            certificate_manager.DeleteCertificateRequest(),
            name="name_value",
        )


def test_delete_certificate_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapsRequest,
        dict,
    ],
)
def test_list_certificate_maps_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificateMapsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.ListCertificateMapsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_certificate_maps(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_maps_rest_required_fields(
    request_type=certificate_manager.ListCertificateMapsRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_maps._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_maps._get_unset_required_fields(jsonified_request)
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

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.ListCertificateMapsResponse()
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

            pb_return_value = certificate_manager.ListCertificateMapsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_certificate_maps(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_certificate_maps_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_certificate_maps._get_unset_required_fields({})
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
def test_list_certificate_maps_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_list_certificate_maps"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_list_certificate_maps"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.ListCertificateMapsRequest.pb(
            certificate_manager.ListCertificateMapsRequest()
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
            certificate_manager.ListCertificateMapsResponse.to_json(
                certificate_manager.ListCertificateMapsResponse()
            )
        )

        request = certificate_manager.ListCertificateMapsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.ListCertificateMapsResponse()

        client.list_certificate_maps(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_certificate_maps_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.ListCertificateMapsRequest
):
    client = CertificateManagerClient(
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
        client.list_certificate_maps(request)


def test_list_certificate_maps_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificateMapsResponse()

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
        pb_return_value = certificate_manager.ListCertificateMapsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_certificate_maps(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificateMaps"
            % client.transport._host,
            args[1],
        )


def test_list_certificate_maps_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_maps(
            certificate_manager.ListCertificateMapsRequest(),
            parent="parent_value",
        )


def test_list_certificate_maps_rest_pager(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            certificate_manager.ListCertificateMapsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_certificate_maps(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.CertificateMap) for i in results)

        pages = list(client.list_certificate_maps(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapRequest,
        dict,
    ],
)
def test_get_certificate_map_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.CertificateMap(
            name="name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.CertificateMap.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_certificate_map(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMap)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_certificate_map_rest_required_fields(
    request_type=certificate_manager.GetCertificateMapRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.CertificateMap()
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

            pb_return_value = certificate_manager.CertificateMap.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_certificate_map(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_certificate_map_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_certificate_map._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_certificate_map_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_get_certificate_map"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_get_certificate_map"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.GetCertificateMapRequest.pb(
            certificate_manager.GetCertificateMapRequest()
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
        req.return_value._content = certificate_manager.CertificateMap.to_json(
            certificate_manager.CertificateMap()
        )

        request = certificate_manager.GetCertificateMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.CertificateMap()

        client.get_certificate_map(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_certificate_map_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.GetCertificateMapRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
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
        client.get_certificate_map(request)


def test_get_certificate_map_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.CertificateMap()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.CertificateMap.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_certificate_map(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateMaps/*}"
            % client.transport._host,
            args[1],
        )


def test_get_certificate_map_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map(
            certificate_manager.GetCertificateMapRequest(),
            name="name_value",
        )


def test_get_certificate_map_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapRequest,
        dict,
    ],
)
def test_create_certificate_map_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate_map"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "gclb_targets": [
            {
                "target_https_proxy": "target_https_proxy_value",
                "target_ssl_proxy": "target_ssl_proxy_value",
                "ip_configs": [{"ip_address": "ip_address_value", "ports": [569, 570]}],
            }
        ],
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
        response = client.create_certificate_map(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_certificate_map_rest_required_fields(
    request_type=certificate_manager.CreateCertificateMapRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["certificate_map_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "certificateMapId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "certificateMapId" in jsonified_request
    assert jsonified_request["certificateMapId"] == request_init["certificate_map_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["certificateMapId"] = "certificate_map_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_map._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("certificate_map_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "certificateMapId" in jsonified_request
    assert jsonified_request["certificateMapId"] == "certificate_map_id_value"

    client = CertificateManagerClient(
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

            response = client.create_certificate_map(request)

            expected_params = [
                (
                    "certificateMapId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_certificate_map_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_certificate_map._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("certificateMapId",))
        & set(
            (
                "parent",
                "certificateMapId",
                "certificateMap",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_certificate_map_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_create_certificate_map"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_create_certificate_map"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.CreateCertificateMapRequest.pb(
            certificate_manager.CreateCertificateMapRequest()
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

        request = certificate_manager.CreateCertificateMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_certificate_map(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_certificate_map_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.CreateCertificateMapRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate_map"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "gclb_targets": [
            {
                "target_https_proxy": "target_https_proxy_value",
                "target_ssl_proxy": "target_ssl_proxy_value",
                "ip_configs": [{"ip_address": "ip_address_value", "ports": [569, 570]}],
            }
        ],
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
        client.create_certificate_map(request)


def test_create_certificate_map_rest_flattened():
    client = CertificateManagerClient(
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
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_certificate_map(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificateMaps"
            % client.transport._host,
            args[1],
        )


def test_create_certificate_map_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map(
            certificate_manager.CreateCertificateMapRequest(),
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )


def test_create_certificate_map_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapRequest,
        dict,
    ],
)
def test_update_certificate_map_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate_map": {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }
    }
    request_init["certificate_map"] = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "gclb_targets": [
            {
                "target_https_proxy": "target_https_proxy_value",
                "target_ssl_proxy": "target_ssl_proxy_value",
                "ip_configs": [{"ip_address": "ip_address_value", "ports": [569, 570]}],
            }
        ],
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
        response = client.update_certificate_map(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_certificate_map_rest_required_fields(
    request_type=certificate_manager.UpdateCertificateMapRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate_map._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CertificateManagerClient(
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

            response = client.update_certificate_map(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_certificate_map_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_certificate_map._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "certificateMap",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_certificate_map_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_update_certificate_map"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_update_certificate_map"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.UpdateCertificateMapRequest.pb(
            certificate_manager.UpdateCertificateMapRequest()
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

        request = certificate_manager.UpdateCertificateMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_certificate_map(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_certificate_map_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.UpdateCertificateMapRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate_map": {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }
    }
    request_init["certificate_map"] = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "gclb_targets": [
            {
                "target_https_proxy": "target_https_proxy_value",
                "target_ssl_proxy": "target_ssl_proxy_value",
                "ip_configs": [{"ip_address": "ip_address_value", "ports": [569, 570]}],
            }
        ],
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
        client.update_certificate_map(request)


def test_update_certificate_map_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "certificate_map": {
                "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_certificate_map(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{certificate_map.name=projects/*/locations/*/certificateMaps/*}"
            % client.transport._host,
            args[1],
        )


def test_update_certificate_map_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map(
            certificate_manager.UpdateCertificateMapRequest(),
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_certificate_map_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapRequest,
        dict,
    ],
)
def test_delete_certificate_map_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
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
        response = client.delete_certificate_map(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_certificate_map_rest_required_fields(
    request_type=certificate_manager.DeleteCertificateMapRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_map._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
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

            response = client.delete_certificate_map(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_certificate_map_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_certificate_map._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_certificate_map_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_delete_certificate_map"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_delete_certificate_map"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.DeleteCertificateMapRequest.pb(
            certificate_manager.DeleteCertificateMapRequest()
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

        request = certificate_manager.DeleteCertificateMapRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_certificate_map(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_certificate_map_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.DeleteCertificateMapRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
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
        client.delete_certificate_map(request)


def test_delete_certificate_map_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3"
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

        client.delete_certificate_map(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateMaps/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_certificate_map_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map(
            certificate_manager.DeleteCertificateMapRequest(),
            name="name_value",
        )


def test_delete_certificate_map_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapEntriesRequest,
        dict,
    ],
)
def test_list_certificate_map_entries_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificateMapEntriesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.ListCertificateMapEntriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_certificate_map_entries(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapEntriesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_map_entries_rest_required_fields(
    request_type=certificate_manager.ListCertificateMapEntriesRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_map_entries._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_map_entries._get_unset_required_fields(jsonified_request)
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

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.ListCertificateMapEntriesResponse()
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

            pb_return_value = certificate_manager.ListCertificateMapEntriesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_certificate_map_entries(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_certificate_map_entries_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_certificate_map_entries._get_unset_required_fields({})
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
def test_list_certificate_map_entries_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_list_certificate_map_entries",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_list_certificate_map_entries"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.ListCertificateMapEntriesRequest.pb(
            certificate_manager.ListCertificateMapEntriesRequest()
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
            certificate_manager.ListCertificateMapEntriesResponse.to_json(
                certificate_manager.ListCertificateMapEntriesResponse()
            )
        )

        request = certificate_manager.ListCertificateMapEntriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.ListCertificateMapEntriesResponse()

        client.list_certificate_map_entries(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_certificate_map_entries_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.ListCertificateMapEntriesRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
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
        client.list_certificate_map_entries(request)


def test_list_certificate_map_entries_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListCertificateMapEntriesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.ListCertificateMapEntriesResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_certificate_map_entries(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/certificateMaps/*}/certificateMapEntries"
            % client.transport._host,
            args[1],
        )


def test_list_certificate_map_entries_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_map_entries(
            certificate_manager.ListCertificateMapEntriesRequest(),
            parent="parent_value",
        )


def test_list_certificate_map_entries_rest_pager(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            certificate_manager.ListCertificateMapEntriesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }

        pager = client.list_certificate_map_entries(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, certificate_manager.CertificateMapEntry) for i in results
        )

        pages = list(client.list_certificate_map_entries(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapEntryRequest,
        dict,
    ],
)
def test_get_certificate_map_entry_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.CertificateMapEntry(
            name="name_value",
            description="description_value",
            certificates=["certificates_value"],
            state=certificate_manager.ServingState.ACTIVE,
            hostname="hostname_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.CertificateMapEntry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_certificate_map_entry(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMapEntry)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.certificates == ["certificates_value"]
    assert response.state == certificate_manager.ServingState.ACTIVE


def test_get_certificate_map_entry_rest_required_fields(
    request_type=certificate_manager.GetCertificateMapEntryRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.CertificateMapEntry()
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

            pb_return_value = certificate_manager.CertificateMapEntry.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_certificate_map_entry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_certificate_map_entry_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_certificate_map_entry._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_certificate_map_entry_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_get_certificate_map_entry"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_get_certificate_map_entry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.GetCertificateMapEntryRequest.pb(
            certificate_manager.GetCertificateMapEntryRequest()
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
        req.return_value._content = certificate_manager.CertificateMapEntry.to_json(
            certificate_manager.CertificateMapEntry()
        )

        request = certificate_manager.GetCertificateMapEntryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.CertificateMapEntry()

        client.get_certificate_map_entry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_certificate_map_entry_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.GetCertificateMapEntryRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
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
        client.get_certificate_map_entry(request)


def test_get_certificate_map_entry_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.CertificateMapEntry()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.CertificateMapEntry.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_certificate_map_entry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateMaps/*/certificateMapEntries/*}"
            % client.transport._host,
            args[1],
        )


def test_get_certificate_map_entry_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map_entry(
            certificate_manager.GetCertificateMapEntryRequest(),
            name="name_value",
        )


def test_get_certificate_map_entry_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapEntryRequest,
        dict,
    ],
)
def test_create_certificate_map_entry_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
    }
    request_init["certificate_map_entry"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "hostname": "hostname_value",
        "matcher": 1,
        "certificates": ["certificates_value1", "certificates_value2"],
        "state": 1,
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
        response = client.create_certificate_map_entry(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_certificate_map_entry_rest_required_fields(
    request_type=certificate_manager.CreateCertificateMapEntryRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["certificate_map_entry_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "certificateMapEntryId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "certificateMapEntryId" in jsonified_request
    assert (
        jsonified_request["certificateMapEntryId"]
        == request_init["certificate_map_entry_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["certificateMapEntryId"] = "certificate_map_entry_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_map_entry._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("certificate_map_entry_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "certificateMapEntryId" in jsonified_request
    assert (
        jsonified_request["certificateMapEntryId"] == "certificate_map_entry_id_value"
    )

    client = CertificateManagerClient(
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

            response = client.create_certificate_map_entry(request)

            expected_params = [
                (
                    "certificateMapEntryId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_certificate_map_entry_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_certificate_map_entry._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("certificateMapEntryId",))
        & set(
            (
                "parent",
                "certificateMapEntryId",
                "certificateMapEntry",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_certificate_map_entry_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_create_certificate_map_entry",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_create_certificate_map_entry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.CreateCertificateMapEntryRequest.pb(
            certificate_manager.CreateCertificateMapEntryRequest()
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

        request = certificate_manager.CreateCertificateMapEntryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_certificate_map_entry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_certificate_map_entry_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.CreateCertificateMapEntryRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
    }
    request_init["certificate_map_entry"] = {
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "hostname": "hostname_value",
        "matcher": 1,
        "certificates": ["certificates_value1", "certificates_value2"],
        "state": 1,
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
        client.create_certificate_map_entry(request)


def test_create_certificate_map_entry_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/certificateMaps/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_certificate_map_entry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/certificateMaps/*}/certificateMapEntries"
            % client.transport._host,
            args[1],
        )


def test_create_certificate_map_entry_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map_entry(
            certificate_manager.CreateCertificateMapEntryRequest(),
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )


def test_create_certificate_map_entry_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapEntryRequest,
        dict,
    ],
)
def test_update_certificate_map_entry_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate_map_entry": {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
        }
    }
    request_init["certificate_map_entry"] = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "hostname": "hostname_value",
        "matcher": 1,
        "certificates": ["certificates_value1", "certificates_value2"],
        "state": 1,
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
        response = client.update_certificate_map_entry(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_certificate_map_entry_rest_required_fields(
    request_type=certificate_manager.UpdateCertificateMapEntryRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_certificate_map_entry._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CertificateManagerClient(
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

            response = client.update_certificate_map_entry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_certificate_map_entry_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_certificate_map_entry._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "certificateMapEntry",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_certificate_map_entry_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_update_certificate_map_entry",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_update_certificate_map_entry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.UpdateCertificateMapEntryRequest.pb(
            certificate_manager.UpdateCertificateMapEntryRequest()
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

        request = certificate_manager.UpdateCertificateMapEntryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_certificate_map_entry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_certificate_map_entry_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.UpdateCertificateMapEntryRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "certificate_map_entry": {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
        }
    }
    request_init["certificate_map_entry"] = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "hostname": "hostname_value",
        "matcher": 1,
        "certificates": ["certificates_value1", "certificates_value2"],
        "state": 1,
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
        client.update_certificate_map_entry(request)


def test_update_certificate_map_entry_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "certificate_map_entry": {
                "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_certificate_map_entry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{certificate_map_entry.name=projects/*/locations/*/certificateMaps/*/certificateMapEntries/*}"
            % client.transport._host,
            args[1],
        )


def test_update_certificate_map_entry_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map_entry(
            certificate_manager.UpdateCertificateMapEntryRequest(),
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_certificate_map_entry_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapEntryRequest,
        dict,
    ],
)
def test_delete_certificate_map_entry_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
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
        response = client.delete_certificate_map_entry(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_certificate_map_entry_rest_required_fields(
    request_type=certificate_manager.DeleteCertificateMapEntryRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_map_entry._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
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

            response = client.delete_certificate_map_entry(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_certificate_map_entry_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_certificate_map_entry._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_certificate_map_entry_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_delete_certificate_map_entry",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_delete_certificate_map_entry"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.DeleteCertificateMapEntryRequest.pb(
            certificate_manager.DeleteCertificateMapEntryRequest()
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

        request = certificate_manager.DeleteCertificateMapEntryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_certificate_map_entry(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_certificate_map_entry_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.DeleteCertificateMapEntryRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
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
        client.delete_certificate_map_entry(request)


def test_delete_certificate_map_entry_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateMaps/sample3/certificateMapEntries/sample4"
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

        client.delete_certificate_map_entry(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateMaps/*/certificateMapEntries/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_certificate_map_entry_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map_entry(
            certificate_manager.DeleteCertificateMapEntryRequest(),
            name="name_value",
        )


def test_delete_certificate_map_entry_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListDnsAuthorizationsRequest,
        dict,
    ],
)
def test_list_dns_authorizations_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListDnsAuthorizationsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.ListDnsAuthorizationsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_dns_authorizations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDnsAuthorizationsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_dns_authorizations_rest_required_fields(
    request_type=certificate_manager.ListDnsAuthorizationsRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_dns_authorizations._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_dns_authorizations._get_unset_required_fields(jsonified_request)
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

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.ListDnsAuthorizationsResponse()
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

            pb_return_value = certificate_manager.ListDnsAuthorizationsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_dns_authorizations(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_dns_authorizations_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_dns_authorizations._get_unset_required_fields({})
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
def test_list_dns_authorizations_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_list_dns_authorizations"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_list_dns_authorizations"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.ListDnsAuthorizationsRequest.pb(
            certificate_manager.ListDnsAuthorizationsRequest()
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
            certificate_manager.ListDnsAuthorizationsResponse.to_json(
                certificate_manager.ListDnsAuthorizationsResponse()
            )
        )

        request = certificate_manager.ListDnsAuthorizationsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.ListDnsAuthorizationsResponse()

        client.list_dns_authorizations(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_dns_authorizations_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.ListDnsAuthorizationsRequest,
):
    client = CertificateManagerClient(
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
        client.list_dns_authorizations(request)


def test_list_dns_authorizations_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.ListDnsAuthorizationsResponse()

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
        pb_return_value = certificate_manager.ListDnsAuthorizationsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_dns_authorizations(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/dnsAuthorizations"
            % client.transport._host,
            args[1],
        )


def test_list_dns_authorizations_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dns_authorizations(
            certificate_manager.ListDnsAuthorizationsRequest(),
            parent="parent_value",
        )


def test_list_dns_authorizations_rest_pager(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            certificate_manager.ListDnsAuthorizationsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_dns_authorizations(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.DnsAuthorization) for i in results)

        pages = list(client.list_dns_authorizations(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetDnsAuthorizationRequest,
        dict,
    ],
)
def test_get_dns_authorization_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.DnsAuthorization(
            name="name_value",
            description="description_value",
            domain="domain_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.DnsAuthorization.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_dns_authorization(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.DnsAuthorization)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.domain == "domain_value"


def test_get_dns_authorization_rest_required_fields(
    request_type=certificate_manager.GetDnsAuthorizationRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_manager.DnsAuthorization()
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

            pb_return_value = certificate_manager.DnsAuthorization.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_dns_authorization(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_dns_authorization_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_dns_authorization._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_dns_authorization_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_get_dns_authorization"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_get_dns_authorization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.GetDnsAuthorizationRequest.pb(
            certificate_manager.GetDnsAuthorizationRequest()
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
        req.return_value._content = certificate_manager.DnsAuthorization.to_json(
            certificate_manager.DnsAuthorization()
        )

        request = certificate_manager.GetDnsAuthorizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_manager.DnsAuthorization()

        client.get_dns_authorization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_dns_authorization_rest_bad_request(
    transport: str = "rest", request_type=certificate_manager.GetDnsAuthorizationRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
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
        client.get_dns_authorization(request)


def test_get_dns_authorization_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_manager.DnsAuthorization()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_manager.DnsAuthorization.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_dns_authorization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/dnsAuthorizations/*}"
            % client.transport._host,
            args[1],
        )


def test_get_dns_authorization_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dns_authorization(
            certificate_manager.GetDnsAuthorizationRequest(),
            name="name_value",
        )


def test_get_dns_authorization_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateDnsAuthorizationRequest,
        dict,
    ],
)
def test_create_dns_authorization_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["dns_authorization"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "domain": "domain_value",
        "dns_resource_record": {
            "name": "name_value",
            "type_": "type__value",
            "data": "data_value",
        },
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
        response = client.create_dns_authorization(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_dns_authorization_rest_required_fields(
    request_type=certificate_manager.CreateDnsAuthorizationRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["dns_authorization_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "dnsAuthorizationId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "dnsAuthorizationId" in jsonified_request
    assert (
        jsonified_request["dnsAuthorizationId"] == request_init["dns_authorization_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["dnsAuthorizationId"] = "dns_authorization_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_dns_authorization._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("dns_authorization_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "dnsAuthorizationId" in jsonified_request
    assert jsonified_request["dnsAuthorizationId"] == "dns_authorization_id_value"

    client = CertificateManagerClient(
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

            response = client.create_dns_authorization(request)

            expected_params = [
                (
                    "dnsAuthorizationId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_dns_authorization_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_dns_authorization._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("dnsAuthorizationId",))
        & set(
            (
                "parent",
                "dnsAuthorizationId",
                "dnsAuthorization",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_dns_authorization_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_create_dns_authorization"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_create_dns_authorization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.CreateDnsAuthorizationRequest.pb(
            certificate_manager.CreateDnsAuthorizationRequest()
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

        request = certificate_manager.CreateDnsAuthorizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_dns_authorization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_dns_authorization_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.CreateDnsAuthorizationRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["dns_authorization"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "domain": "domain_value",
        "dns_resource_record": {
            "name": "name_value",
            "type_": "type__value",
            "data": "data_value",
        },
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
        client.create_dns_authorization(request)


def test_create_dns_authorization_rest_flattened():
    client = CertificateManagerClient(
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
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_dns_authorization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/dnsAuthorizations"
            % client.transport._host,
            args[1],
        )


def test_create_dns_authorization_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dns_authorization(
            certificate_manager.CreateDnsAuthorizationRequest(),
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )


def test_create_dns_authorization_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateDnsAuthorizationRequest,
        dict,
    ],
)
def test_update_dns_authorization_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "dns_authorization": {
            "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
        }
    }
    request_init["dns_authorization"] = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "domain": "domain_value",
        "dns_resource_record": {
            "name": "name_value",
            "type_": "type__value",
            "data": "data_value",
        },
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
        response = client.update_dns_authorization(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_dns_authorization_rest_required_fields(
    request_type=certificate_manager.UpdateDnsAuthorizationRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_dns_authorization._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CertificateManagerClient(
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

            response = client.update_dns_authorization(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_dns_authorization_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_dns_authorization._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "dnsAuthorization",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_dns_authorization_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_update_dns_authorization"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_update_dns_authorization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.UpdateDnsAuthorizationRequest.pb(
            certificate_manager.UpdateDnsAuthorizationRequest()
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

        request = certificate_manager.UpdateDnsAuthorizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_dns_authorization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_dns_authorization_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.UpdateDnsAuthorizationRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "dns_authorization": {
            "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
        }
    }
    request_init["dns_authorization"] = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "domain": "domain_value",
        "dns_resource_record": {
            "name": "name_value",
            "type_": "type__value",
            "data": "data_value",
        },
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
        client.update_dns_authorization(request)


def test_update_dns_authorization_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "dns_authorization": {
                "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_dns_authorization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{dns_authorization.name=projects/*/locations/*/dnsAuthorizations/*}"
            % client.transport._host,
            args[1],
        )


def test_update_dns_authorization_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dns_authorization(
            certificate_manager.UpdateDnsAuthorizationRequest(),
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_dns_authorization_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteDnsAuthorizationRequest,
        dict,
    ],
)
def test_delete_dns_authorization_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
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
        response = client.delete_dns_authorization(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_dns_authorization_rest_required_fields(
    request_type=certificate_manager.DeleteDnsAuthorizationRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_dns_authorization._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
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

            response = client.delete_dns_authorization(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_dns_authorization_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_dns_authorization._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_dns_authorization_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor, "post_delete_dns_authorization"
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor, "pre_delete_dns_authorization"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_manager.DeleteDnsAuthorizationRequest.pb(
            certificate_manager.DeleteDnsAuthorizationRequest()
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

        request = certificate_manager.DeleteDnsAuthorizationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_dns_authorization(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_dns_authorization_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_manager.DeleteDnsAuthorizationRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
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
        client.delete_dns_authorization(request)


def test_delete_dns_authorization_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/dnsAuthorizations/sample3"
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

        client.delete_dns_authorization(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/dnsAuthorizations/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_dns_authorization_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dns_authorization(
            certificate_manager.DeleteDnsAuthorizationRequest(),
            name="name_value",
        )


def test_delete_dns_authorization_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.ListCertificateIssuanceConfigsRequest,
        dict,
    ],
)
def test_list_certificate_issuance_configs_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_certificate_issuance_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateIssuanceConfigsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_issuance_configs_rest_required_fields(
    request_type=certificate_issuance_config.ListCertificateIssuanceConfigsRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_issuance_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_certificate_issuance_configs._get_unset_required_fields(jsonified_request)
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

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
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

            pb_return_value = (
                certificate_issuance_config.ListCertificateIssuanceConfigsResponse.pb(
                    return_value
                )
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_certificate_issuance_configs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_certificate_issuance_configs_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.list_certificate_issuance_configs._get_unset_required_fields({})
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
def test_list_certificate_issuance_configs_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_list_certificate_issuance_configs",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "pre_list_certificate_issuance_configs",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = (
            certificate_issuance_config.ListCertificateIssuanceConfigsRequest.pb(
                certificate_issuance_config.ListCertificateIssuanceConfigsRequest()
            )
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
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse.to_json(
                certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
            )
        )

        request = certificate_issuance_config.ListCertificateIssuanceConfigsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )

        client.list_certificate_issuance_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_certificate_issuance_configs_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_issuance_config.ListCertificateIssuanceConfigsRequest,
):
    client = CertificateManagerClient(
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
        client.list_certificate_issuance_configs(request)


def test_list_certificate_issuance_configs_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse()
        )

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
        pb_return_value = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse.pb(
                return_value
            )
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_certificate_issuance_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificateIssuanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_list_certificate_issuance_configs_rest_flattened_error(
    transport: str = "rest",
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_issuance_configs(
            certificate_issuance_config.ListCertificateIssuanceConfigsRequest(),
            parent="parent_value",
        )


def test_list_certificate_issuance_configs_rest_pager(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="abc",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[],
                next_page_token="def",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
                next_page_token="ghi",
            ),
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse(
                certificate_issuance_configs=[
                    certificate_issuance_config.CertificateIssuanceConfig(),
                    certificate_issuance_config.CertificateIssuanceConfig(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            certificate_issuance_config.ListCertificateIssuanceConfigsResponse.to_json(
                x
            )
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_certificate_issuance_configs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, certificate_issuance_config.CertificateIssuanceConfig)
            for i in results
        )

        pages = list(
            client.list_certificate_issuance_configs(request=sample_request).pages
        )
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.GetCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_get_certificate_issuance_config_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_issuance_config.CertificateIssuanceConfig(
            name="name_value",
            description="description_value",
            rotation_window_percentage=2788,
            key_algorithm=certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_issuance_config.CertificateIssuanceConfig.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_certificate_issuance_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_issuance_config.CertificateIssuanceConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.rotation_window_percentage == 2788
    assert (
        response.key_algorithm
        == certificate_issuance_config.CertificateIssuanceConfig.KeyAlgorithm.RSA_2048
    )


def test_get_certificate_issuance_config_rest_required_fields(
    request_type=certificate_issuance_config.GetCertificateIssuanceConfigRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = certificate_issuance_config.CertificateIssuanceConfig()
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

            pb_return_value = certificate_issuance_config.CertificateIssuanceConfig.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_certificate_issuance_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_certificate_issuance_config_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_certificate_issuance_config._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_certificate_issuance_config_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_get_certificate_issuance_config",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "pre_get_certificate_issuance_config",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = certificate_issuance_config.GetCertificateIssuanceConfigRequest.pb(
            certificate_issuance_config.GetCertificateIssuanceConfigRequest()
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
            certificate_issuance_config.CertificateIssuanceConfig.to_json(
                certificate_issuance_config.CertificateIssuanceConfig()
            )
        )

        request = certificate_issuance_config.GetCertificateIssuanceConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = certificate_issuance_config.CertificateIssuanceConfig()

        client.get_certificate_issuance_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_certificate_issuance_config_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_issuance_config.GetCertificateIssuanceConfigRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
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
        client.get_certificate_issuance_config(request)


def test_get_certificate_issuance_config_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = certificate_issuance_config.CertificateIssuanceConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = certificate_issuance_config.CertificateIssuanceConfig.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_certificate_issuance_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateIssuanceConfigs/*}"
            % client.transport._host,
            args[1],
        )


def test_get_certificate_issuance_config_rest_flattened_error(transport: str = "rest"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_issuance_config(
            certificate_issuance_config.GetCertificateIssuanceConfigRequest(),
            name="name_value",
        )


def test_get_certificate_issuance_config_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_create_certificate_issuance_config_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate_issuance_config"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "certificate_authority_config": {
            "certificate_authority_service_config": {"ca_pool": "ca_pool_value"}
        },
        "lifetime": {"seconds": 751, "nanos": 543},
        "rotation_window_percentage": 2788,
        "key_algorithm": 1,
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
        response = client.create_certificate_issuance_config(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_certificate_issuance_config_rest_required_fields(
    request_type=gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["certificate_issuance_config_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "certificateIssuanceConfigId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "certificateIssuanceConfigId" in jsonified_request
    assert (
        jsonified_request["certificateIssuanceConfigId"]
        == request_init["certificate_issuance_config_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request[
        "certificateIssuanceConfigId"
    ] = "certificate_issuance_config_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("certificate_issuance_config_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "certificateIssuanceConfigId" in jsonified_request
    assert (
        jsonified_request["certificateIssuanceConfigId"]
        == "certificate_issuance_config_id_value"
    )

    client = CertificateManagerClient(
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

            response = client.create_certificate_issuance_config(request)

            expected_params = [
                (
                    "certificateIssuanceConfigId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_certificate_issuance_config_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.create_certificate_issuance_config._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(("certificateIssuanceConfigId",))
        & set(
            (
                "parent",
                "certificateIssuanceConfigId",
                "certificateIssuanceConfig",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_certificate_issuance_config_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_create_certificate_issuance_config",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "pre_create_certificate_issuance_config",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = (
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest.pb(
                gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()
            )
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

        request = (
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest()
        )
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_certificate_issuance_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_certificate_issuance_config_rest_bad_request(
    transport: str = "rest",
    request_type=gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["certificate_issuance_config"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "description": "description_value",
        "certificate_authority_config": {
            "certificate_authority_service_config": {"ca_pool": "ca_pool_value"}
        },
        "lifetime": {"seconds": 751, "nanos": 543},
        "rotation_window_percentage": 2788,
        "key_algorithm": 1,
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
        client.create_certificate_issuance_config(request)


def test_create_certificate_issuance_config_rest_flattened():
    client = CertificateManagerClient(
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
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_certificate_issuance_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/certificateIssuanceConfigs"
            % client.transport._host,
            args[1],
        )


def test_create_certificate_issuance_config_rest_flattened_error(
    transport: str = "rest",
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_issuance_config(
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest(),
            parent="parent_value",
            certificate_issuance_config=gcc_certificate_issuance_config.CertificateIssuanceConfig(
                name="name_value"
            ),
            certificate_issuance_config_id="certificate_issuance_config_id_value",
        )


def test_create_certificate_issuance_config_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_issuance_config.DeleteCertificateIssuanceConfigRequest,
        dict,
    ],
)
def test_delete_certificate_issuance_config_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
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
        response = client.delete_certificate_issuance_config(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_certificate_issuance_config_rest_required_fields(
    request_type=certificate_issuance_config.DeleteCertificateIssuanceConfigRequest,
):
    transport_class = transports.CertificateManagerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_certificate_issuance_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CertificateManagerClient(
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

            response = client.delete_certificate_issuance_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_certificate_issuance_config_rest_unset_required_fields():
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.delete_certificate_issuance_config._get_unset_required_fields({})
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_certificate_issuance_config_rest_interceptors(null_interceptor):
    transport = transports.CertificateManagerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CertificateManagerRestInterceptor(),
    )
    client = CertificateManagerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "post_delete_certificate_issuance_config",
    ) as post, mock.patch.object(
        transports.CertificateManagerRestInterceptor,
        "pre_delete_certificate_issuance_config",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = (
            certificate_issuance_config.DeleteCertificateIssuanceConfigRequest.pb(
                certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()
            )
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

        request = certificate_issuance_config.DeleteCertificateIssuanceConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_certificate_issuance_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_certificate_issuance_config_rest_bad_request(
    transport: str = "rest",
    request_type=certificate_issuance_config.DeleteCertificateIssuanceConfigRequest,
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
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
        client.delete_certificate_issuance_config(request)


def test_delete_certificate_issuance_config_rest_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/certificateIssuanceConfigs/sample3"
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

        client.delete_certificate_issuance_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/certificateIssuanceConfigs/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_certificate_issuance_config_rest_flattened_error(
    transport: str = "rest",
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_issuance_config(
            certificate_issuance_config.DeleteCertificateIssuanceConfigRequest(),
            name="name_value",
        )


def test_delete_certificate_issuance_config_rest_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CertificateManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CertificateManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
        transports.CertificateManagerRestTransport,
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
    transport = CertificateManagerClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CertificateManagerGrpcTransport,
    )


def test_certificate_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CertificateManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_certificate_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CertificateManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_certificates",
        "get_certificate",
        "create_certificate",
        "update_certificate",
        "delete_certificate",
        "list_certificate_maps",
        "get_certificate_map",
        "create_certificate_map",
        "update_certificate_map",
        "delete_certificate_map",
        "list_certificate_map_entries",
        "get_certificate_map_entry",
        "create_certificate_map_entry",
        "update_certificate_map_entry",
        "delete_certificate_map_entry",
        "list_dns_authorizations",
        "get_dns_authorization",
        "create_dns_authorization",
        "update_dns_authorization",
        "delete_dns_authorization",
        "list_certificate_issuance_configs",
        "get_certificate_issuance_config",
        "create_certificate_issuance_config",
        "delete_certificate_issuance_config",
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


def test_certificate_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateManagerTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_certificate_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateManagerTransport()
        adc.assert_called_once()


def test_certificate_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CertificateManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_auth_adc(transport_class):
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
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
        transports.CertificateManagerRestTransport,
    ],
)
def test_certificate_manager_transport_auth_gdch_credentials(transport_class):
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
        (transports.CertificateManagerGrpcTransport, grpc_helpers),
        (transports.CertificateManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_certificate_manager_transport_create_channel(transport_class, grpc_helpers):
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
            "certificatemanager.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="certificatemanager.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_grpc_transport_client_cert_source_for_mtls(
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


def test_certificate_manager_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CertificateManagerRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_certificate_manager_rest_lro_client():
    client = CertificateManagerClient(
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
def test_certificate_manager_host_no_port(transport_name):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="certificatemanager.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "certificatemanager.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://certificatemanager.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_certificate_manager_host_with_port(transport_name):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="certificatemanager.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "certificatemanager.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://certificatemanager.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_certificate_manager_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = CertificateManagerClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CertificateManagerClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_certificates._session
    session2 = client2.transport.list_certificates._session
    assert session1 != session2
    session1 = client1.transport.get_certificate._session
    session2 = client2.transport.get_certificate._session
    assert session1 != session2
    session1 = client1.transport.create_certificate._session
    session2 = client2.transport.create_certificate._session
    assert session1 != session2
    session1 = client1.transport.update_certificate._session
    session2 = client2.transport.update_certificate._session
    assert session1 != session2
    session1 = client1.transport.delete_certificate._session
    session2 = client2.transport.delete_certificate._session
    assert session1 != session2
    session1 = client1.transport.list_certificate_maps._session
    session2 = client2.transport.list_certificate_maps._session
    assert session1 != session2
    session1 = client1.transport.get_certificate_map._session
    session2 = client2.transport.get_certificate_map._session
    assert session1 != session2
    session1 = client1.transport.create_certificate_map._session
    session2 = client2.transport.create_certificate_map._session
    assert session1 != session2
    session1 = client1.transport.update_certificate_map._session
    session2 = client2.transport.update_certificate_map._session
    assert session1 != session2
    session1 = client1.transport.delete_certificate_map._session
    session2 = client2.transport.delete_certificate_map._session
    assert session1 != session2
    session1 = client1.transport.list_certificate_map_entries._session
    session2 = client2.transport.list_certificate_map_entries._session
    assert session1 != session2
    session1 = client1.transport.get_certificate_map_entry._session
    session2 = client2.transport.get_certificate_map_entry._session
    assert session1 != session2
    session1 = client1.transport.create_certificate_map_entry._session
    session2 = client2.transport.create_certificate_map_entry._session
    assert session1 != session2
    session1 = client1.transport.update_certificate_map_entry._session
    session2 = client2.transport.update_certificate_map_entry._session
    assert session1 != session2
    session1 = client1.transport.delete_certificate_map_entry._session
    session2 = client2.transport.delete_certificate_map_entry._session
    assert session1 != session2
    session1 = client1.transport.list_dns_authorizations._session
    session2 = client2.transport.list_dns_authorizations._session
    assert session1 != session2
    session1 = client1.transport.get_dns_authorization._session
    session2 = client2.transport.get_dns_authorization._session
    assert session1 != session2
    session1 = client1.transport.create_dns_authorization._session
    session2 = client2.transport.create_dns_authorization._session
    assert session1 != session2
    session1 = client1.transport.update_dns_authorization._session
    session2 = client2.transport.update_dns_authorization._session
    assert session1 != session2
    session1 = client1.transport.delete_dns_authorization._session
    session2 = client2.transport.delete_dns_authorization._session
    assert session1 != session2
    session1 = client1.transport.list_certificate_issuance_configs._session
    session2 = client2.transport.list_certificate_issuance_configs._session
    assert session1 != session2
    session1 = client1.transport.get_certificate_issuance_config._session
    session2 = client2.transport.get_certificate_issuance_config._session
    assert session1 != session2
    session1 = client1.transport.create_certificate_issuance_config._session
    session2 = client2.transport.create_certificate_issuance_config._session
    assert session1 != session2
    session1 = client1.transport.delete_certificate_issuance_config._session
    session2 = client2.transport.delete_certificate_issuance_config._session
    assert session1 != session2


def test_certificate_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_certificate_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateManagerGrpcAsyncIOTransport(
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
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_channel_mtls_with_client_cert_source(
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
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_channel_mtls_with_adc(transport_class):
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


def test_certificate_manager_grpc_lro_client():
    client = CertificateManagerClient(
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


def test_certificate_manager_grpc_lro_async_client():
    client = CertificateManagerAsyncClient(
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


def test_ca_pool_path():
    project = "squid"
    location = "clam"
    ca_pool = "whelk"
    expected = "projects/{project}/locations/{location}/caPools/{ca_pool}".format(
        project=project,
        location=location,
        ca_pool=ca_pool,
    )
    actual = CertificateManagerClient.ca_pool_path(project, location, ca_pool)
    assert expected == actual


def test_parse_ca_pool_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "ca_pool": "nudibranch",
    }
    path = CertificateManagerClient.ca_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_ca_pool_path(path)
    assert expected == actual


def test_certificate_path():
    project = "cuttlefish"
    location = "mussel"
    certificate = "winkle"
    expected = (
        "projects/{project}/locations/{location}/certificates/{certificate}".format(
            project=project,
            location=location,
            certificate=certificate,
        )
    )
    actual = CertificateManagerClient.certificate_path(project, location, certificate)
    assert expected == actual


def test_parse_certificate_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "certificate": "abalone",
    }
    path = CertificateManagerClient.certificate_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_path(path)
    assert expected == actual


def test_certificate_issuance_config_path():
    project = "squid"
    location = "clam"
    certificate_issuance_config = "whelk"
    expected = "projects/{project}/locations/{location}/certificateIssuanceConfigs/{certificate_issuance_config}".format(
        project=project,
        location=location,
        certificate_issuance_config=certificate_issuance_config,
    )
    actual = CertificateManagerClient.certificate_issuance_config_path(
        project, location, certificate_issuance_config
    )
    assert expected == actual


def test_parse_certificate_issuance_config_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "certificate_issuance_config": "nudibranch",
    }
    path = CertificateManagerClient.certificate_issuance_config_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_issuance_config_path(path)
    assert expected == actual


def test_certificate_map_path():
    project = "cuttlefish"
    location = "mussel"
    certificate_map = "winkle"
    expected = "projects/{project}/locations/{location}/certificateMaps/{certificate_map}".format(
        project=project,
        location=location,
        certificate_map=certificate_map,
    )
    actual = CertificateManagerClient.certificate_map_path(
        project, location, certificate_map
    )
    assert expected == actual


def test_parse_certificate_map_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "certificate_map": "abalone",
    }
    path = CertificateManagerClient.certificate_map_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_map_path(path)
    assert expected == actual


def test_certificate_map_entry_path():
    project = "squid"
    location = "clam"
    certificate_map = "whelk"
    certificate_map_entry = "octopus"
    expected = "projects/{project}/locations/{location}/certificateMaps/{certificate_map}/certificateMapEntries/{certificate_map_entry}".format(
        project=project,
        location=location,
        certificate_map=certificate_map,
        certificate_map_entry=certificate_map_entry,
    )
    actual = CertificateManagerClient.certificate_map_entry_path(
        project, location, certificate_map, certificate_map_entry
    )
    assert expected == actual


def test_parse_certificate_map_entry_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "certificate_map": "cuttlefish",
        "certificate_map_entry": "mussel",
    }
    path = CertificateManagerClient.certificate_map_entry_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_map_entry_path(path)
    assert expected == actual


def test_dns_authorization_path():
    project = "winkle"
    location = "nautilus"
    dns_authorization = "scallop"
    expected = "projects/{project}/locations/{location}/dnsAuthorizations/{dns_authorization}".format(
        project=project,
        location=location,
        dns_authorization=dns_authorization,
    )
    actual = CertificateManagerClient.dns_authorization_path(
        project, location, dns_authorization
    )
    assert expected == actual


def test_parse_dns_authorization_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "dns_authorization": "clam",
    }
    path = CertificateManagerClient.dns_authorization_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_dns_authorization_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CertificateManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CertificateManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CertificateManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CertificateManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CertificateManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CertificateManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CertificateManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CertificateManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CertificateManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CertificateManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CertificateManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CertificateManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CertificateManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CertificateManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = CertificateManagerClient(
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
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerClient(
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
async def test_delete_operation_async(transport: str = "grpc"):
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
async def test_cancel_operation_async(transport: str = "grpc"):
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
async def test_get_operation_async(transport: str = "grpc"):
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
async def test_list_operations_async(transport: str = "grpc"):
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
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


def test_list_locations(transport: str = "grpc"):
    client = CertificateManagerClient(
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
async def test_list_locations_async(transport: str = "grpc"):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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
    client = CertificateManagerClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

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
    client = CertificateManagerClient(
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
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
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


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CertificateManagerClient(
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
        client = CertificateManagerClient(
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
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
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
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
