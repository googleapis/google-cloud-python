# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2  # type: ignore
from google.pubsub_v1.services.schema_service import SchemaServiceAsyncClient
from google.pubsub_v1.services.schema_service import SchemaServiceClient
from google.pubsub_v1.services.schema_service import pagers
from google.pubsub_v1.services.schema_service import transports
from google.pubsub_v1.types import schema
from google.pubsub_v1.types import schema as gp_schema
import google.auth


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

    assert SchemaServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        SchemaServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SchemaServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SchemaServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SchemaServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SchemaServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (SchemaServiceClient, "grpc"),
        (SchemaServiceAsyncClient, "grpc_asyncio"),
        (SchemaServiceClient, "rest"),
    ],
)
def test_schema_service_client_from_service_account_info(client_class, transport_name):
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
            "pubsub.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://pubsub.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.SchemaServiceGrpcTransport, "grpc"),
        (transports.SchemaServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.SchemaServiceRestTransport, "rest"),
    ],
)
def test_schema_service_client_service_account_always_use_jwt(
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
        (SchemaServiceClient, "grpc"),
        (SchemaServiceAsyncClient, "grpc_asyncio"),
        (SchemaServiceClient, "rest"),
    ],
)
def test_schema_service_client_from_service_account_file(client_class, transport_name):
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
            "pubsub.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://pubsub.googleapis.com"
        )


def test_schema_service_client_get_transport_class():
    transport = SchemaServiceClient.get_transport_class()
    available_transports = [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceRestTransport,
    ]
    assert transport in available_transports

    transport = SchemaServiceClient.get_transport_class("grpc")
    assert transport == transports.SchemaServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SchemaServiceClient, transports.SchemaServiceGrpcTransport, "grpc"),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (SchemaServiceClient, transports.SchemaServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    SchemaServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceClient),
)
@mock.patch.object(
    SchemaServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceAsyncClient),
)
def test_schema_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SchemaServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SchemaServiceClient, "get_transport_class") as gtc:
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
        (SchemaServiceClient, transports.SchemaServiceGrpcTransport, "grpc", "true"),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SchemaServiceClient, transports.SchemaServiceGrpcTransport, "grpc", "false"),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (SchemaServiceClient, transports.SchemaServiceRestTransport, "rest", "true"),
        (SchemaServiceClient, transports.SchemaServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    SchemaServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceClient),
)
@mock.patch.object(
    SchemaServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_schema_service_client_mtls_env_auto(
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
    "client_class", [SchemaServiceClient, SchemaServiceAsyncClient]
)
@mock.patch.object(
    SchemaServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceClient),
)
@mock.patch.object(
    SchemaServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SchemaServiceAsyncClient),
)
def test_schema_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (SchemaServiceClient, transports.SchemaServiceGrpcTransport, "grpc"),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (SchemaServiceClient, transports.SchemaServiceRestTransport, "rest"),
    ],
)
def test_schema_service_client_client_options_scopes(
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
            SchemaServiceClient,
            transports.SchemaServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (SchemaServiceClient, transports.SchemaServiceRestTransport, "rest", None),
    ],
)
def test_schema_service_client_client_options_credentials_file(
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


def test_schema_service_client_client_options_from_dict():
    with mock.patch(
        "google.pubsub_v1.services.schema_service.transports.SchemaServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SchemaServiceClient(
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
            SchemaServiceClient,
            transports.SchemaServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SchemaServiceAsyncClient,
            transports.SchemaServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_schema_service_client_create_channel_credentials_file(
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
            "pubsub.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            scopes=None,
            default_host="pubsub.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
                ("grpc.max_metadata_size", 4 * 1024 * 1024),
                ("grpc.keepalive_time_ms", 30000),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.CreateSchemaRequest,
        dict,
    ],
)
def test_create_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema(
            name="name_value",
            type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )
        response = client.create_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CreateSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_create_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        client.create_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CreateSchemaRequest()


@pytest.mark.asyncio
async def test_create_schema_async(
    transport: str = "grpc_asyncio", request_type=gp_schema.CreateSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gp_schema.Schema(
                name="name_value",
                type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
                definition="definition_value",
                revision_id="revision_id_value",
            )
        )
        response = await client.create_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CreateSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_create_schema_async_from_dict():
    await test_create_schema_async(request_type=dict)


def test_create_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.CreateSchemaRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        call.return_value = gp_schema.Schema()
        client.create_schema(request)

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
async def test_create_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.CreateSchemaRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gp_schema.Schema())
        await client.create_schema(request)

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


def test_create_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_schema(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val
        arg = args[0].schema_id
        mock_val = "schema_id_value"
        assert arg == mock_val


def test_create_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_schema(
            gp_schema.CreateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )


@pytest.mark.asyncio
async def test_create_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gp_schema.Schema())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_schema(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val
        arg = args[0].schema_id
        mock_val = "schema_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_schema(
            gp_schema.CreateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.GetSchemaRequest,
        dict,
    ],
)
def test_get_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )
        response = client.get_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.GetSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_get_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        client.get_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.GetSchemaRequest()


@pytest.mark.asyncio
async def test_get_schema_async(
    transport: str = "grpc_asyncio", request_type=schema.GetSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.Schema(
                name="name_value",
                type_=schema.Schema.Type.PROTOCOL_BUFFER,
                definition="definition_value",
                revision_id="revision_id_value",
            )
        )
        response = await client.get_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.GetSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_get_schema_async_from_dict():
    await test_get_schema_async(request_type=dict)


def test_get_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.GetSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        call.return_value = schema.Schema()
        client.get_schema(request)

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
async def test_get_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.GetSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        await client.get_schema(request)

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


def test_get_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_schema(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_schema(
            schema.GetSchemaRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_schema(
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
async def test_get_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_schema(
            schema.GetSchemaRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ListSchemasRequest,
        dict,
    ],
)
def test_list_schemas(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemasResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_schemas(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemasRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemasPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_schemas_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        client.list_schemas()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemasRequest()


@pytest.mark.asyncio
async def test_list_schemas_async(
    transport: str = "grpc_asyncio", request_type=schema.ListSchemasRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemasResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_schemas(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemasRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemasAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_schemas_async_from_dict():
    await test_list_schemas_async(request_type=dict)


def test_list_schemas_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ListSchemasRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        call.return_value = schema.ListSchemasResponse()
        client.list_schemas(request)

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
async def test_list_schemas_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ListSchemasRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemasResponse()
        )
        await client.list_schemas(request)

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


def test_list_schemas_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemasResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_schemas(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_schemas_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_schemas(
            schema.ListSchemasRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_schemas_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemasResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemasResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_schemas(
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
async def test_list_schemas_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_schemas(
            schema.ListSchemasRequest(),
            parent="parent_value",
        )


def test_list_schemas_pager(transport_name: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemasResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_schemas(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, schema.Schema) for i in results)


def test_list_schemas_pages(transport_name: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_schemas), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemasResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_schemas(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_schemas_async_pager():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schemas), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemasResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_schemas(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, schema.Schema) for i in responses)


@pytest.mark.asyncio
async def test_list_schemas_async_pages():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schemas), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemasResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_schemas(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ListSchemaRevisionsRequest,
        dict,
    ],
)
def test_list_schema_revisions(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemaRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_schema_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemaRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemaRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_schema_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        client.list_schema_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemaRevisionsRequest()


@pytest.mark.asyncio
async def test_list_schema_revisions_async(
    transport: str = "grpc_asyncio", request_type=schema.ListSchemaRevisionsRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemaRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_schema_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ListSchemaRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemaRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_schema_revisions_async_from_dict():
    await test_list_schema_revisions_async(request_type=dict)


def test_list_schema_revisions_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ListSchemaRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        call.return_value = schema.ListSchemaRevisionsResponse()
        client.list_schema_revisions(request)

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
async def test_list_schema_revisions_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ListSchemaRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemaRevisionsResponse()
        )
        await client.list_schema_revisions(request)

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


def test_list_schema_revisions_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemaRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_schema_revisions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_schema_revisions_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_schema_revisions(
            schema.ListSchemaRevisionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_schema_revisions_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ListSchemaRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ListSchemaRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_schema_revisions(
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
async def test_list_schema_revisions_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_schema_revisions(
            schema.ListSchemaRevisionsRequest(),
            name="name_value",
        )


def test_list_schema_revisions_pager(transport_name: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_schema_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, schema.Schema) for i in results)


def test_list_schema_revisions_pages(transport_name: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_schema_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_schema_revisions_async_pager():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_schema_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, schema.Schema) for i in responses)


@pytest.mark.asyncio
async def test_list_schema_revisions_async_pages():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_schema_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_schema_revisions(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.CommitSchemaRequest,
        dict,
    ],
)
def test_commit_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema(
            name="name_value",
            type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )
        response = client.commit_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CommitSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_commit_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        client.commit_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CommitSchemaRequest()


@pytest.mark.asyncio
async def test_commit_schema_async(
    transport: str = "grpc_asyncio", request_type=gp_schema.CommitSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gp_schema.Schema(
                name="name_value",
                type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
                definition="definition_value",
                revision_id="revision_id_value",
            )
        )
        response = await client.commit_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.CommitSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_commit_schema_async_from_dict():
    await test_commit_schema_async(request_type=dict)


def test_commit_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.CommitSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        call.return_value = gp_schema.Schema()
        client.commit_schema(request)

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
async def test_commit_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.CommitSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gp_schema.Schema())
        await client.commit_schema(request)

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


def test_commit_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.commit_schema(
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val


def test_commit_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.commit_schema(
            gp_schema.CommitSchemaRequest(),
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )


@pytest.mark.asyncio
async def test_commit_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.commit_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.Schema()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gp_schema.Schema())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.commit_schema(
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_commit_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.commit_schema(
            gp_schema.CommitSchemaRequest(),
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.RollbackSchemaRequest,
        dict,
    ],
)
def test_rollback_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )
        response = client.rollback_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.RollbackSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_rollback_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        client.rollback_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.RollbackSchemaRequest()


@pytest.mark.asyncio
async def test_rollback_schema_async(
    transport: str = "grpc_asyncio", request_type=schema.RollbackSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.Schema(
                name="name_value",
                type_=schema.Schema.Type.PROTOCOL_BUFFER,
                definition="definition_value",
                revision_id="revision_id_value",
            )
        )
        response = await client.rollback_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.RollbackSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_rollback_schema_async_from_dict():
    await test_rollback_schema_async(request_type=dict)


def test_rollback_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.RollbackSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        call.return_value = schema.Schema()
        client.rollback_schema(request)

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
async def test_rollback_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.RollbackSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        await client.rollback_schema(request)

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


def test_rollback_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback_schema(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


def test_rollback_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_schema(
            schema.RollbackSchemaRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.asyncio
async def test_rollback_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rollback_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback_schema(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rollback_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback_schema(
            schema.RollbackSchemaRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.DeleteSchemaRevisionRequest,
        dict,
    ],
)
def test_delete_schema_revision(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )
        response = client.delete_schema_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_delete_schema_revision_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        client.delete_schema_revision()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRevisionRequest()


@pytest.mark.asyncio
async def test_delete_schema_revision_async(
    transport: str = "grpc_asyncio", request_type=schema.DeleteSchemaRevisionRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.Schema(
                name="name_value",
                type_=schema.Schema.Type.PROTOCOL_BUFFER,
                definition="definition_value",
                revision_id="revision_id_value",
            )
        )
        response = await client.delete_schema_revision(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRevisionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_delete_schema_revision_async_from_dict():
    await test_delete_schema_revision_async(request_type=dict)


def test_delete_schema_revision_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.DeleteSchemaRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        call.return_value = schema.Schema()
        client.delete_schema_revision(request)

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
async def test_delete_schema_revision_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.DeleteSchemaRevisionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        await client.delete_schema_revision(request)

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


def test_delete_schema_revision_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_schema_revision(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


def test_delete_schema_revision_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_schema_revision(
            schema.DeleteSchemaRevisionRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.asyncio
async def test_delete_schema_revision_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_schema_revision), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.Schema()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(schema.Schema())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_schema_revision(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_schema_revision_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_schema_revision(
            schema.DeleteSchemaRevisionRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.DeleteSchemaRequest,
        dict,
    ],
)
def test_delete_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        client.delete_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRequest()


@pytest.mark.asyncio
async def test_delete_schema_async(
    transport: str = "grpc_asyncio", request_type=schema.DeleteSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.DeleteSchemaRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_schema_async_from_dict():
    await test_delete_schema_async(request_type=dict)


def test_delete_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.DeleteSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        call.return_value = None
        client.delete_schema(request)

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
async def test_delete_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.DeleteSchemaRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_schema(request)

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


def test_delete_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_schema(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_schema(
            schema.DeleteSchemaRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_schema(
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
async def test_delete_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_schema(
            schema.DeleteSchemaRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.ValidateSchemaRequest,
        dict,
    ],
)
def test_validate_schema(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.ValidateSchemaResponse()
        response = client.validate_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.ValidateSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.ValidateSchemaResponse)


def test_validate_schema_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        client.validate_schema()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.ValidateSchemaRequest()


@pytest.mark.asyncio
async def test_validate_schema_async(
    transport: str = "grpc_asyncio", request_type=gp_schema.ValidateSchemaRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gp_schema.ValidateSchemaResponse()
        )
        response = await client.validate_schema(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gp_schema.ValidateSchemaRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.ValidateSchemaResponse)


@pytest.mark.asyncio
async def test_validate_schema_async_from_dict():
    await test_validate_schema_async(request_type=dict)


def test_validate_schema_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.ValidateSchemaRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        call.return_value = gp_schema.ValidateSchemaResponse()
        client.validate_schema(request)

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
async def test_validate_schema_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gp_schema.ValidateSchemaRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gp_schema.ValidateSchemaResponse()
        )
        await client.validate_schema(request)

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


def test_validate_schema_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.ValidateSchemaResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.validate_schema(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val


def test_validate_schema_flattened_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.validate_schema(
            gp_schema.ValidateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )


@pytest.mark.asyncio
async def test_validate_schema_flattened_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_schema), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gp_schema.ValidateSchemaResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gp_schema.ValidateSchemaResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.validate_schema(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].schema
        mock_val = gp_schema.Schema(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_validate_schema_flattened_error_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.validate_schema(
            gp_schema.ValidateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ValidateMessageRequest,
        dict,
    ],
)
def test_validate_message(request_type, transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = schema.ValidateMessageResponse()
        response = client.validate_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ValidateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.ValidateMessageResponse)


def test_validate_message_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_message), "__call__") as call:
        client.validate_message()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ValidateMessageRequest()


@pytest.mark.asyncio
async def test_validate_message_async(
    transport: str = "grpc_asyncio", request_type=schema.ValidateMessageRequest
):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_message), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ValidateMessageResponse()
        )
        response = await client.validate_message(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == schema.ValidateMessageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.ValidateMessageResponse)


@pytest.mark.asyncio
async def test_validate_message_async_from_dict():
    await test_validate_message_async(request_type=dict)


def test_validate_message_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ValidateMessageRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_message), "__call__") as call:
        call.return_value = schema.ValidateMessageResponse()
        client.validate_message(request)

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
async def test_validate_message_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = schema.ValidateMessageRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.validate_message), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            schema.ValidateMessageResponse()
        )
        await client.validate_message(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.CreateSchemaRequest,
        dict,
    ],
)
def test_create_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["schema"] = {
        "name": "name_value",
        "type_": 1,
        "definition": "definition_value",
        "revision_id": "revision_id_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.Schema(
            name="name_value",
            type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_schema(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_create_schema_rest_required_fields(request_type=gp_schema.CreateSchemaRequest):
    transport_class = transports.SchemaServiceRestTransport

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
    ).create_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_schema._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("schema_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gp_schema.Schema()
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

            pb_return_value = gp_schema.Schema.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_schema._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("schemaId",))
        & set(
            (
                "parent",
                "schema",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_create_schema"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_create_schema"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gp_schema.CreateSchemaRequest.pb(gp_schema.CreateSchemaRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gp_schema.Schema.to_json(gp_schema.Schema())

        request = gp_schema.CreateSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gp_schema.Schema()

        client.create_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_schema_rest_bad_request(
    transport: str = "rest", request_type=gp_schema.CreateSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["schema"] = {
        "name": "name_value",
        "type_": 1,
        "definition": "definition_value",
        "revision_id": "revision_id_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
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
        client.create_schema(request)


def test_create_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.Schema()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*}/schemas" % client.transport._host, args[1]
        )


def test_create_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_schema(
            gp_schema.CreateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
            schema_id="schema_id_value",
        )


def test_create_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.GetSchemaRequest,
        dict,
    ],
)
def test_get_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_schema(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_get_schema_rest_required_fields(request_type=schema.GetSchemaRequest):
    transport_class = transports.SchemaServiceRestTransport

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
    ).get_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_schema._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("view",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.Schema()
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

            pb_return_value = schema.Schema.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_schema._get_unset_required_fields({})
    assert set(unset_fields) == (set(("view",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_get_schema"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_get_schema"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.GetSchemaRequest.pb(schema.GetSchemaRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = schema.Schema.to_json(schema.Schema())

        request = schema.GetSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.Schema()

        client.get_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_schema_rest_bad_request(
    transport: str = "rest", request_type=schema.GetSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.get_schema(request)


def test_get_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}" % client.transport._host, args[1]
        )


def test_get_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_schema(
            schema.GetSchemaRequest(),
            name="name_value",
        )


def test_get_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ListSchemasRequest,
        dict,
    ],
)
def test_list_schemas_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.ListSchemasResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.ListSchemasResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_schemas(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemasPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_schemas_rest_required_fields(request_type=schema.ListSchemasRequest):
    transport_class = transports.SchemaServiceRestTransport

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
    ).list_schemas._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_schemas._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.ListSchemasResponse()
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

            pb_return_value = schema.ListSchemasResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_schemas(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_schemas_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_schemas._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_schemas_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_list_schemas"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_list_schemas"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.ListSchemasRequest.pb(schema.ListSchemasRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = schema.ListSchemasResponse.to_json(
            schema.ListSchemasResponse()
        )

        request = schema.ListSchemasRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.ListSchemasResponse()

        client.list_schemas(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_schemas_rest_bad_request(
    transport: str = "rest", request_type=schema.ListSchemasRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
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
        client.list_schemas(request)


def test_list_schemas_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.ListSchemasResponse()

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
        pb_return_value = schema.ListSchemasResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_schemas(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*}/schemas" % client.transport._host, args[1]
        )


def test_list_schemas_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_schemas(
            schema.ListSchemasRequest(),
            parent="parent_value",
        )


def test_list_schemas_rest_pager(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemasResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemasResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(schema.ListSchemasResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_schemas(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, schema.Schema) for i in results)

        pages = list(client.list_schemas(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ListSchemaRevisionsRequest,
        dict,
    ],
)
def test_list_schema_revisions_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.ListSchemaRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.ListSchemaRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_schema_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSchemaRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_schema_revisions_rest_required_fields(
    request_type=schema.ListSchemaRevisionsRequest,
):
    transport_class = transports.SchemaServiceRestTransport

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
    ).list_schema_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_schema_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.ListSchemaRevisionsResponse()
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

            pb_return_value = schema.ListSchemaRevisionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_schema_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_schema_revisions_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_schema_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_schema_revisions_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_list_schema_revisions"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_list_schema_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.ListSchemaRevisionsRequest.pb(
            schema.ListSchemaRevisionsRequest()
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
        req.return_value._content = schema.ListSchemaRevisionsResponse.to_json(
            schema.ListSchemaRevisionsResponse()
        )

        request = schema.ListSchemaRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.ListSchemaRevisionsResponse()

        client.list_schema_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_schema_revisions_rest_bad_request(
    transport: str = "rest", request_type=schema.ListSchemaRevisionsRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.list_schema_revisions(request)


def test_list_schema_revisions_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.ListSchemaRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.ListSchemaRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_schema_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}:listRevisions" % client.transport._host,
            args[1],
        )


def test_list_schema_revisions_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_schema_revisions(
            schema.ListSchemaRevisionsRequest(),
            name="name_value",
        )


def test_list_schema_revisions_rest_pager(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                    schema.Schema(),
                ],
                next_page_token="abc",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[],
                next_page_token="def",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                ],
                next_page_token="ghi",
            ),
            schema.ListSchemaRevisionsResponse(
                schemas=[
                    schema.Schema(),
                    schema.Schema(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            schema.ListSchemaRevisionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"name": "projects/sample1/schemas/sample2"}

        pager = client.list_schema_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, schema.Schema) for i in results)

        pages = list(client.list_schema_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.CommitSchemaRequest,
        dict,
    ],
)
def test_commit_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.Schema(
            name="name_value",
            type_=gp_schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.commit_schema(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == gp_schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_commit_schema_rest_required_fields(request_type=gp_schema.CommitSchemaRequest):
    transport_class = transports.SchemaServiceRestTransport

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
    ).commit_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).commit_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gp_schema.Schema()
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

            pb_return_value = gp_schema.Schema.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.commit_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_commit_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.commit_schema._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "schema",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_commit_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_commit_schema"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_commit_schema"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gp_schema.CommitSchemaRequest.pb(gp_schema.CommitSchemaRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gp_schema.Schema.to_json(gp_schema.Schema())

        request = gp_schema.CommitSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gp_schema.Schema()

        client.commit_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_commit_schema_rest_bad_request(
    transport: str = "rest", request_type=gp_schema.CommitSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.commit_schema(request)


def test_commit_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.Schema()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.commit_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}:commit" % client.transport._host, args[1]
        )


def test_commit_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.commit_schema(
            gp_schema.CommitSchemaRequest(),
            name="name_value",
            schema=gp_schema.Schema(name="name_value"),
        )


def test_commit_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.RollbackSchemaRequest,
        dict,
    ],
)
def test_rollback_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.rollback_schema(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_rollback_schema_rest_required_fields(
    request_type=schema.RollbackSchemaRequest,
):
    transport_class = transports.SchemaServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["revision_id"] = ""
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
    ).rollback_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["revisionId"] = "revision_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "revisionId" in jsonified_request
    assert jsonified_request["revisionId"] == "revision_id_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.Schema()
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

            pb_return_value = schema.Schema.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.rollback_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rollback_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rollback_schema._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "revisionId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rollback_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_rollback_schema"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_rollback_schema"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.RollbackSchemaRequest.pb(schema.RollbackSchemaRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = schema.Schema.to_json(schema.Schema())

        request = schema.RollbackSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.Schema()

        client.rollback_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rollback_schema_rest_bad_request(
    transport: str = "rest", request_type=schema.RollbackSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.rollback_schema(request)


def test_rollback_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            revision_id="revision_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.rollback_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}:rollback" % client.transport._host,
            args[1],
        )


def test_rollback_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_schema(
            schema.RollbackSchemaRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


def test_rollback_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.DeleteSchemaRevisionRequest,
        dict,
    ],
)
def test_delete_schema_revision_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema(
            name="name_value",
            type_=schema.Schema.Type.PROTOCOL_BUFFER,
            definition="definition_value",
            revision_id="revision_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_schema_revision(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.Schema)
    assert response.name == "name_value"
    assert response.type_ == schema.Schema.Type.PROTOCOL_BUFFER
    assert response.definition == "definition_value"
    assert response.revision_id == "revision_id_value"


def test_delete_schema_revision_rest_required_fields(
    request_type=schema.DeleteSchemaRevisionRequest,
):
    transport_class = transports.SchemaServiceRestTransport

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
    ).delete_schema_revision._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_schema_revision._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("revision_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.Schema()
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

            pb_return_value = schema.Schema.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_schema_revision(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_schema_revision_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_schema_revision._get_unset_required_fields({})
    assert set(unset_fields) == (set(("revisionId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_schema_revision_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_delete_schema_revision"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_delete_schema_revision"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.DeleteSchemaRevisionRequest.pb(
            schema.DeleteSchemaRevisionRequest()
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
        req.return_value._content = schema.Schema.to_json(schema.Schema())

        request = schema.DeleteSchemaRevisionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.Schema()

        client.delete_schema_revision(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_schema_revision_rest_bad_request(
    transport: str = "rest", request_type=schema.DeleteSchemaRevisionRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.delete_schema_revision(request)


def test_delete_schema_revision_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.Schema()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            revision_id="revision_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.Schema.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_schema_revision(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}:deleteRevision" % client.transport._host,
            args[1],
        )


def test_delete_schema_revision_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_schema_revision(
            schema.DeleteSchemaRevisionRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


def test_delete_schema_revision_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.DeleteSchemaRequest,
        dict,
    ],
)
def test_delete_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        response = client.delete_schema(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_schema_rest_required_fields(request_type=schema.DeleteSchemaRequest):
    transport_class = transports.SchemaServiceRestTransport

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
    ).delete_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = SchemaServiceClient(
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

            response = client.delete_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_schema._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_delete_schema"
    ) as pre:
        pre.assert_not_called()
        pb_message = schema.DeleteSchemaRequest.pb(schema.DeleteSchemaRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = schema.DeleteSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_schema_rest_bad_request(
    transport: str = "rest", request_type=schema.DeleteSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/schemas/sample2"}
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
        client.delete_schema(request)


def test_delete_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/schemas/sample2"}

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

        client.delete_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/schemas/*}" % client.transport._host, args[1]
        )


def test_delete_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_schema(
            schema.DeleteSchemaRequest(),
            name="name_value",
        )


def test_delete_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gp_schema.ValidateSchemaRequest,
        dict,
    ],
)
def test_validate_schema_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.ValidateSchemaResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.ValidateSchemaResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.validate_schema(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gp_schema.ValidateSchemaResponse)


def test_validate_schema_rest_required_fields(
    request_type=gp_schema.ValidateSchemaRequest,
):
    transport_class = transports.SchemaServiceRestTransport

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
    ).validate_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate_schema._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gp_schema.ValidateSchemaResponse()
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

            pb_return_value = gp_schema.ValidateSchemaResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.validate_schema(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_validate_schema_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.validate_schema._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "schema",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_validate_schema_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_validate_schema"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_validate_schema"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gp_schema.ValidateSchemaRequest.pb(
            gp_schema.ValidateSchemaRequest()
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
        req.return_value._content = gp_schema.ValidateSchemaResponse.to_json(
            gp_schema.ValidateSchemaResponse()
        )

        request = gp_schema.ValidateSchemaRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gp_schema.ValidateSchemaResponse()

        client.validate_schema(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_validate_schema_rest_bad_request(
    transport: str = "rest", request_type=gp_schema.ValidateSchemaRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
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
        client.validate_schema(request)


def test_validate_schema_rest_flattened():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gp_schema.ValidateSchemaResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gp_schema.ValidateSchemaResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.validate_schema(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*}/schemas:validate" % client.transport._host,
            args[1],
        )


def test_validate_schema_rest_flattened_error(transport: str = "rest"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.validate_schema(
            gp_schema.ValidateSchemaRequest(),
            parent="parent_value",
            schema=gp_schema.Schema(name="name_value"),
        )


def test_validate_schema_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        schema.ValidateMessageRequest,
        dict,
    ],
)
def test_validate_message_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = schema.ValidateMessageResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = schema.ValidateMessageResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.validate_message(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, schema.ValidateMessageResponse)


def test_validate_message_rest_required_fields(
    request_type=schema.ValidateMessageRequest,
):
    transport_class = transports.SchemaServiceRestTransport

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
    ).validate_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).validate_message._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = schema.ValidateMessageResponse()
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

            pb_return_value = schema.ValidateMessageResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.validate_message(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_validate_message_rest_unset_required_fields():
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.validate_message._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_validate_message_rest_interceptors(null_interceptor):
    transport = transports.SchemaServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.SchemaServiceRestInterceptor(),
    )
    client = SchemaServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "post_validate_message"
    ) as post, mock.patch.object(
        transports.SchemaServiceRestInterceptor, "pre_validate_message"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = schema.ValidateMessageRequest.pb(schema.ValidateMessageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = schema.ValidateMessageResponse.to_json(
            schema.ValidateMessageResponse()
        )

        request = schema.ValidateMessageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = schema.ValidateMessageResponse()

        client.validate_message(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_validate_message_rest_bad_request(
    transport: str = "rest", request_type=schema.ValidateMessageRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
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
        client.validate_message(request)


def test_validate_message_rest_error():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SchemaServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SchemaServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SchemaServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SchemaServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SchemaServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = SchemaServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SchemaServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SchemaServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
        transports.SchemaServiceRestTransport,
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
    transport = SchemaServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.SchemaServiceGrpcTransport,
    )


def test_schema_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.SchemaServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_schema_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.pubsub_v1.services.schema_service.transports.SchemaServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SchemaServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_schema",
        "get_schema",
        "list_schemas",
        "list_schema_revisions",
        "commit_schema",
        "rollback_schema",
        "delete_schema_revision",
        "delete_schema",
        "validate_schema",
        "validate_message",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
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


def test_schema_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.pubsub_v1.services.schema_service.transports.SchemaServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SchemaServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


def test_schema_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.pubsub_v1.services.schema_service.transports.SchemaServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SchemaServiceTransport()
        adc.assert_called_once()


def test_schema_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SchemaServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
    ],
)
def test_schema_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
        transports.SchemaServiceRestTransport,
    ],
)
def test_schema_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.SchemaServiceGrpcTransport, grpc_helpers),
        (transports.SchemaServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_schema_service_transport_create_channel(transport_class, grpc_helpers):
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
            "pubsub.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/pubsub",
            ),
            scopes=["1", "2"],
            default_host="pubsub.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
                ("grpc.max_metadata_size", 4 * 1024 * 1024),
                ("grpc.keepalive_time_ms", 30000),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
    ],
)
def test_schema_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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
                ("grpc.max_metadata_size", 4 * 1024 * 1024),
                ("grpc.keepalive_time_ms", 30000),
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


def test_schema_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.SchemaServiceRestTransport(
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
def test_schema_service_host_no_port(transport_name):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "pubsub.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://pubsub.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_schema_service_host_with_port(transport_name):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="pubsub.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "pubsub.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://pubsub.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_schema_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = SchemaServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = SchemaServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_schema._session
    session2 = client2.transport.create_schema._session
    assert session1 != session2
    session1 = client1.transport.get_schema._session
    session2 = client2.transport.get_schema._session
    assert session1 != session2
    session1 = client1.transport.list_schemas._session
    session2 = client2.transport.list_schemas._session
    assert session1 != session2
    session1 = client1.transport.list_schema_revisions._session
    session2 = client2.transport.list_schema_revisions._session
    assert session1 != session2
    session1 = client1.transport.commit_schema._session
    session2 = client2.transport.commit_schema._session
    assert session1 != session2
    session1 = client1.transport.rollback_schema._session
    session2 = client2.transport.rollback_schema._session
    assert session1 != session2
    session1 = client1.transport.delete_schema_revision._session
    session2 = client2.transport.delete_schema_revision._session
    assert session1 != session2
    session1 = client1.transport.delete_schema._session
    session2 = client2.transport.delete_schema._session
    assert session1 != session2
    session1 = client1.transport.validate_schema._session
    session2 = client2.transport.validate_schema._session
    assert session1 != session2
    session1 = client1.transport.validate_message._session
    session2 = client2.transport.validate_message._session
    assert session1 != session2


def test_schema_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SchemaServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_schema_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SchemaServiceGrpcAsyncIOTransport(
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
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
    ],
)
def test_schema_service_transport_channel_mtls_with_client_cert_source(transport_class):
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
                    ("grpc.max_metadata_size", 4 * 1024 * 1024),
                    ("grpc.keepalive_time_ms", 30000),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SchemaServiceGrpcTransport,
        transports.SchemaServiceGrpcAsyncIOTransport,
    ],
)
def test_schema_service_transport_channel_mtls_with_adc(transport_class):
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
                    ("grpc.max_metadata_size", 4 * 1024 * 1024),
                    ("grpc.keepalive_time_ms", 30000),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_schema_path():
    project = "squid"
    schema = "clam"
    expected = "projects/{project}/schemas/{schema}".format(
        project=project,
        schema=schema,
    )
    actual = SchemaServiceClient.schema_path(project, schema)
    assert expected == actual


def test_parse_schema_path():
    expected = {
        "project": "whelk",
        "schema": "octopus",
    }
    path = SchemaServiceClient.schema_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_schema_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SchemaServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = SchemaServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = SchemaServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = SchemaServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = SchemaServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = SchemaServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = SchemaServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = SchemaServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = SchemaServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = SchemaServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SchemaServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SchemaServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SchemaServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SchemaServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SchemaServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/topics/sample2"}, request
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
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/topics/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/topics/sample2"}, request
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
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/topics/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/subscriptions/sample2"}, request
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
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/subscriptions/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_set_iam_policy(transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = SchemaServiceClient(
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
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = SchemaServiceClient(
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


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

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

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = SchemaServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

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

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = SchemaServiceClient(
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


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = SchemaServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = SchemaServiceClient(
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
        client = SchemaServiceClient(
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
        (SchemaServiceClient, transports.SchemaServiceGrpcTransport),
        (SchemaServiceAsyncClient, transports.SchemaServiceGrpcAsyncIOTransport),
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
