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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.datacatalog_v1.services.data_catalog import (
    DataCatalogAsyncClient,
    DataCatalogClient,
    pagers,
    transports,
)
from google.cloud.datacatalog_v1.types import (
    bigquery,
    common,
    data_source,
    datacatalog,
    dataplex_spec,
    gcs_fileset_spec,
    physical_schema,
    schema,
    search,
    table_spec,
    tags,
    timestamps,
    usage,
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


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert DataCatalogClient._get_default_mtls_endpoint(None) is None
    assert (
        DataCatalogClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataCatalogClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert DataCatalogClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DataCatalogClient, "grpc"),
        (DataCatalogAsyncClient, "grpc_asyncio"),
    ],
)
def test_data_catalog_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("datacatalog.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataCatalogGrpcTransport, "grpc"),
        (transports.DataCatalogGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_data_catalog_client_service_account_always_use_jwt(
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
        (DataCatalogClient, "grpc"),
        (DataCatalogAsyncClient, "grpc_asyncio"),
    ],
)
def test_data_catalog_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("datacatalog.googleapis.com:443")


def test_data_catalog_client_get_transport_class():
    transport = DataCatalogClient.get_transport_class()
    available_transports = [
        transports.DataCatalogGrpcTransport,
    ]
    assert transport in available_transports

    transport = DataCatalogClient.get_transport_class("grpc")
    assert transport == transports.DataCatalogGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataCatalogClient)
)
@mock.patch.object(
    DataCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataCatalogAsyncClient),
)
def test_data_catalog_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataCatalogClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataCatalogClient, "get_transport_class") as gtc:
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", "true"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", "false"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataCatalogClient)
)
@mock.patch.object(
    DataCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataCatalogAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_data_catalog_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [DataCatalogClient, DataCatalogAsyncClient])
@mock.patch.object(
    DataCatalogClient, "DEFAULT_ENDPOINT", modify_default_endpoint(DataCatalogClient)
)
@mock.patch.object(
    DataCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataCatalogAsyncClient),
)
def test_data_catalog_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc"),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_catalog_client_client_options_scopes(
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", grpc_helpers),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_data_catalog_client_client_options_credentials_file(
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


def test_data_catalog_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.datacatalog_v1.services.data_catalog.transports.DataCatalogGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataCatalogClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport, "grpc", grpc_helpers),
        (
            DataCatalogAsyncClient,
            transports.DataCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_data_catalog_client_create_channel_credentials_file(
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
            "datacatalog.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="datacatalog.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.SearchCatalogRequest,
        dict,
    ],
)
def test_search_catalog(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse(
            total_size=1086,
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.search_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.SearchCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogPager)
    assert response.total_size == 1086
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_search_catalog_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        client.search_catalog()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.SearchCatalogRequest()


@pytest.mark.asyncio
async def test_search_catalog_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.SearchCatalogRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.SearchCatalogResponse(
                total_size=1086,
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.search_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.SearchCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogAsyncPager)
    assert response.total_size == 1086
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_search_catalog_async_from_dict():
    await test_search_catalog_async(request_type=dict)


def test_search_catalog_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_catalog(
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = datacatalog.SearchCatalogRequest.Scope(
            include_org_ids=["include_org_ids_value"]
        )
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


def test_search_catalog_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_catalog(
            datacatalog.SearchCatalogRequest(),
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_catalog_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.SearchCatalogResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.SearchCatalogResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_catalog(
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].scope
        mock_val = datacatalog.SearchCatalogRequest.Scope(
            include_org_ids=["include_org_ids_value"]
        )
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_search_catalog_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_catalog(
            datacatalog.SearchCatalogRequest(),
            scope=datacatalog.SearchCatalogRequest.Scope(
                include_org_ids=["include_org_ids_value"]
            ),
            query="query_value",
        )


def test_search_catalog_pager(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(
                results=[],
                next_page_token="def",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.search_catalog(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, search.SearchCatalogResult) for i in results)


def test_search_catalog_pages(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalog), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(
                results=[],
                next_page_token="def",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_catalog(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_catalog_async_pager():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalog), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(
                results=[],
                next_page_token="def",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_catalog(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, search.SearchCatalogResult) for i in responses)


@pytest.mark.asyncio
async def test_search_catalog_async_pages():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalog), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
                next_page_token="abc",
            ),
            datacatalog.SearchCatalogResponse(
                results=[],
                next_page_token="def",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.SearchCatalogResponse(
                results=[
                    search.SearchCatalogResult(),
                    search.SearchCatalogResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_catalog(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.CreateEntryGroupRequest,
        dict,
    ],
)
def test_create_entry_group(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_entry_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        client.create_entry_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryGroupRequest()


@pytest.mark.asyncio
async def test_create_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.create_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_entry_group_async_from_dict():
    await test_create_entry_group_async(request_type=dict)


def test_create_entry_group_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryGroupRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        call.return_value = datacatalog.EntryGroup()
        client.create_entry_group(request)

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
async def test_create_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryGroupRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        await client.create_entry_group(request)

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


def test_create_entry_group_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_entry_group(
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].entry_group_id
        mock_val = "entry_group_id_value"
        assert arg == mock_val
        arg = args[0].entry_group
        mock_val = datacatalog.EntryGroup(name="name_value")
        assert arg == mock_val


def test_create_entry_group_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_entry_group(
            datacatalog.CreateEntryGroupRequest(),
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_entry_group_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_entry_group(
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].entry_group_id
        mock_val = "entry_group_id_value"
        assert arg == mock_val
        arg = args[0].entry_group
        mock_val = datacatalog.EntryGroup(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_entry_group(
            datacatalog.CreateEntryGroupRequest(),
            parent="parent_value",
            entry_group_id="entry_group_id_value",
            entry_group=datacatalog.EntryGroup(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.GetEntryGroupRequest,
        dict,
    ],
)
def test_get_entry_group(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_entry_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        client.get_entry_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryGroupRequest()


@pytest.mark.asyncio
async def test_get_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_entry_group_async_from_dict():
    await test_get_entry_group_async(request_type=dict)


def test_get_entry_group_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryGroupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        call.return_value = datacatalog.EntryGroup()
        client.get_entry_group(request)

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
async def test_get_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryGroupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        await client.get_entry_group(request)

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


def test_get_entry_group_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_entry_group(
            name="name_value",
            read_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].read_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_get_entry_group_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_entry_group(
            datacatalog.GetEntryGroupRequest(),
            name="name_value",
            read_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_get_entry_group_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_entry_group(
            name="name_value",
            read_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].read_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_entry_group(
            datacatalog.GetEntryGroupRequest(),
            name="name_value",
            read_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UpdateEntryGroupRequest,
        dict,
    ],
)
def test_update_entry_group(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_entry_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        client.update_entry_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryGroupRequest()


@pytest.mark.asyncio
async def test_update_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryGroup)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_entry_group_async_from_dict():
    await test_update_entry_group_async(request_type=dict)


def test_update_entry_group_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryGroupRequest()

    request.entry_group.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        call.return_value = datacatalog.EntryGroup()
        client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "entry_group.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryGroupRequest()

    request.entry_group.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        await client.update_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "entry_group.name=name_value",
    ) in kw["metadata"]


def test_update_entry_group_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_entry_group(
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].entry_group
        mock_val = datacatalog.EntryGroup(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_entry_group_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_entry_group(
            datacatalog.UpdateEntryGroupRequest(),
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_entry_group_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryGroup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryGroup()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_entry_group(
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].entry_group
        mock_val = datacatalog.EntryGroup(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_entry_group(
            datacatalog.UpdateEntryGroupRequest(),
            entry_group=datacatalog.EntryGroup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.DeleteEntryGroupRequest,
        dict,
    ],
)
def test_delete_entry_group(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_entry_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        client.delete_entry_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryGroupRequest()


@pytest.mark.asyncio
async def test_delete_entry_group_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteEntryGroupRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_entry_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryGroupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_entry_group_async_from_dict():
    await test_delete_entry_group_async(request_type=dict)


def test_delete_entry_group_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryGroupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        call.return_value = None
        client.delete_entry_group(request)

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
async def test_delete_entry_group_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryGroupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_entry_group(request)

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


def test_delete_entry_group_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_entry_group(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_entry_group_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_entry_group(
            datacatalog.DeleteEntryGroupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_entry_group_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_entry_group), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_entry_group(
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
async def test_delete_entry_group_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_entry_group(
            datacatalog.DeleteEntryGroupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ListEntryGroupsRequest,
        dict,
    ],
)
def test_list_entry_groups(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntryGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntryGroupsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_entry_groups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        client.list_entry_groups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntryGroupsRequest()


@pytest.mark.asyncio
async def test_list_entry_groups_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListEntryGroupsRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_entry_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntryGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntryGroupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entry_groups_async_from_dict():
    await test_list_entry_groups_async(request_type=dict)


def test_list_entry_groups_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntryGroupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        call.return_value = datacatalog.ListEntryGroupsResponse()
        client.list_entry_groups(request)

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
async def test_list_entry_groups_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntryGroupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse()
        )
        await client.list_entry_groups(request)

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


def test_list_entry_groups_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_entry_groups(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_entry_groups_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entry_groups(
            datacatalog.ListEntryGroupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_entry_groups_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntryGroupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntryGroupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_entry_groups(
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
async def test_list_entry_groups_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_entry_groups(
            datacatalog.ListEntryGroupsRequest(),
            parent="parent_value",
        )


def test_list_entry_groups_pager(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[],
                next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_entry_groups(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datacatalog.EntryGroup) for i in results)


def test_list_entry_groups_pages(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[],
                next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_entry_groups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entry_groups_async_pager():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[],
                next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entry_groups(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datacatalog.EntryGroup) for i in responses)


@pytest.mark.asyncio
async def test_list_entry_groups_async_pages():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entry_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[],
                next_page_token="def",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntryGroupsResponse(
                entry_groups=[
                    datacatalog.EntryGroup(),
                    datacatalog.EntryGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_entry_groups(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.CreateEntryRequest,
        dict,
    ],
)
def test_create_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            fully_qualified_name="fully_qualified_name_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
        )
        response = client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_create_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        client.create_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryRequest()


@pytest.mark.asyncio
async def test_create_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                fully_qualified_name="fully_qualified_name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.create_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_create_entry_async_from_dict():
    await test_create_entry_async(request_type=dict)


def test_create_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()
        client.create_entry(request)

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
async def test_create_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateEntryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        await client.create_entry(request)

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


def test_create_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_entry(
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].entry_id
        mock_val = "entry_id_value"
        assert arg == mock_val
        arg = args[0].entry
        mock_val = datacatalog.Entry(name="name_value")
        assert arg == mock_val


def test_create_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_entry(
            datacatalog.CreateEntryRequest(),
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_entry(
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].entry_id
        mock_val = "entry_id_value"
        assert arg == mock_val
        arg = args[0].entry
        mock_val = datacatalog.Entry(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_entry(
            datacatalog.CreateEntryRequest(),
            parent="parent_value",
            entry_id="entry_id_value",
            entry=datacatalog.Entry(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UpdateEntryRequest,
        dict,
    ],
)
def test_update_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            fully_qualified_name="fully_qualified_name_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
        )
        response = client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_update_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        client.update_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryRequest()


@pytest.mark.asyncio
async def test_update_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                fully_qualified_name="fully_qualified_name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_update_entry_async_from_dict():
    await test_update_entry_async(request_type=dict)


def test_update_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryRequest()

    request.entry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()
        client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "entry.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateEntryRequest()

    request.entry.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        await client.update_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "entry.name=name_value",
    ) in kw["metadata"]


def test_update_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_entry(
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].entry
        mock_val = datacatalog.Entry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_entry(
            datacatalog.UpdateEntryRequest(),
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_entry(
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].entry
        mock_val = datacatalog.Entry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_entry(
            datacatalog.UpdateEntryRequest(),
            entry=datacatalog.Entry(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.DeleteEntryRequest,
        dict,
    ],
)
def test_delete_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        client.delete_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryRequest()


@pytest.mark.asyncio
async def test_delete_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteEntryRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_entry_async_from_dict():
    await test_delete_entry_async(request_type=dict)


def test_delete_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        call.return_value = None
        client.delete_entry(request)

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
async def test_delete_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_entry(request)

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


def test_delete_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_entry(
            datacatalog.DeleteEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_entry(
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
async def test_delete_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_entry(
            datacatalog.DeleteEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.GetEntryRequest,
        dict,
    ],
)
def test_get_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            fully_qualified_name="fully_qualified_name_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
        )
        response = client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        client.get_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryRequest()


@pytest.mark.asyncio
async def test_get_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                fully_qualified_name="fully_qualified_name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_entry_async_from_dict():
    await test_get_entry_async(request_type=dict)


def test_get_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        call.return_value = datacatalog.Entry()
        client.get_entry(request)

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
async def test_get_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        await client.get_entry(request)

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


def test_get_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_entry(
            datacatalog.GetEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(datacatalog.Entry())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_entry(
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
async def test_get_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_entry(
            datacatalog.GetEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.LookupEntryRequest,
        dict,
    ],
)
def test_lookup_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Entry(
            name="name_value",
            linked_resource="linked_resource_value",
            fully_qualified_name="fully_qualified_name_value",
            display_name="display_name_value",
            description="description_value",
            type_=datacatalog.EntryType.TABLE,
            integrated_system=common.IntegratedSystem.BIGQUERY,
        )
        response = client.lookup_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.LookupEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_lookup_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_entry), "__call__") as call:
        client.lookup_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.LookupEntryRequest()


@pytest.mark.asyncio
async def test_lookup_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.LookupEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.lookup_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Entry(
                name="name_value",
                linked_resource="linked_resource_value",
                fully_qualified_name="fully_qualified_name_value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.lookup_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.LookupEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Entry)
    assert response.name == "name_value"
    assert response.linked_resource == "linked_resource_value"
    assert response.fully_qualified_name == "fully_qualified_name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_lookup_entry_async_from_dict():
    await test_lookup_entry_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ListEntriesRequest,
        dict,
    ],
)
def test_list_entries(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        client.list_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntriesRequest()


@pytest.mark.asyncio
async def test_list_entries_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListEntriesRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEntriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_entries_async_from_dict():
    await test_list_entries_async(request_type=dict)


def test_list_entries_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        call.return_value = datacatalog.ListEntriesResponse()
        client.list_entries(request)

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
async def test_list_entries_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse()
        )
        await client.list_entries(request)

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


def test_list_entries_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_entries(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_entries_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_entries(
            datacatalog.ListEntriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_entries_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_entries(
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
async def test_list_entries_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_entries(
            datacatalog.ListEntriesRequest(),
            parent="parent_value",
        )


def test_list_entries_pager(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(
                entries=[],
                next_page_token="def",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_entries(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, datacatalog.Entry) for i in results)


def test_list_entries_pages(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_entries), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(
                entries=[],
                next_page_token="def",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_entries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_entries_async_pager():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(
                entries=[],
                next_page_token="def",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_entries(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, datacatalog.Entry) for i in responses)


@pytest.mark.asyncio
async def test_list_entries_async_pages():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_entries), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListEntriesResponse(
                entries=[],
                next_page_token="def",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListEntriesResponse(
                entries=[
                    datacatalog.Entry(),
                    datacatalog.Entry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_entries(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ModifyEntryOverviewRequest,
        dict,
    ],
)
def test_modify_entry_overview(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_overview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.EntryOverview(
            overview="overview_value",
        )
        response = client.modify_entry_overview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryOverviewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryOverview)
    assert response.overview == "overview_value"


def test_modify_entry_overview_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_overview), "__call__"
    ) as call:
        client.modify_entry_overview()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryOverviewRequest()


@pytest.mark.asyncio
async def test_modify_entry_overview_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ModifyEntryOverviewRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_overview), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryOverview(
                overview="overview_value",
            )
        )
        response = await client.modify_entry_overview(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryOverviewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.EntryOverview)
    assert response.overview == "overview_value"


@pytest.mark.asyncio
async def test_modify_entry_overview_async_from_dict():
    await test_modify_entry_overview_async(request_type=dict)


def test_modify_entry_overview_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ModifyEntryOverviewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_overview), "__call__"
    ) as call:
        call.return_value = datacatalog.EntryOverview()
        client.modify_entry_overview(request)

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
async def test_modify_entry_overview_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ModifyEntryOverviewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_overview), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.EntryOverview()
        )
        await client.modify_entry_overview(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ModifyEntryContactsRequest,
        dict,
    ],
)
def test_modify_entry_contacts(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_contacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.Contacts()
        response = client.modify_entry_contacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryContactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Contacts)


def test_modify_entry_contacts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_contacts), "__call__"
    ) as call:
        client.modify_entry_contacts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryContactsRequest()


@pytest.mark.asyncio
async def test_modify_entry_contacts_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ModifyEntryContactsRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_contacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Contacts()
        )
        response = await client.modify_entry_contacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ModifyEntryContactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.Contacts)


@pytest.mark.asyncio
async def test_modify_entry_contacts_async_from_dict():
    await test_modify_entry_contacts_async(request_type=dict)


def test_modify_entry_contacts_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ModifyEntryContactsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_contacts), "__call__"
    ) as call:
        call.return_value = datacatalog.Contacts()
        client.modify_entry_contacts(request)

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
async def test_modify_entry_contacts_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ModifyEntryContactsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_entry_contacts), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.Contacts()
        )
        await client.modify_entry_contacts(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.CreateTagTemplateRequest,
        dict,
    ],
)
def test_create_tag_template(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value",
            display_name="display_name_value",
            is_publicly_readable=True,
        )
        response = client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


def test_create_tag_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        client.create_tag_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateRequest()


@pytest.mark.asyncio
async def test_create_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(
                name="name_value",
                display_name="display_name_value",
                is_publicly_readable=True,
            )
        )
        response = await client.create_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


@pytest.mark.asyncio
async def test_create_tag_template_async_from_dict():
    await test_create_tag_template_async(request_type=dict)


def test_create_tag_template_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        call.return_value = tags.TagTemplate()
        client.create_tag_template(request)

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
async def test_create_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        await client.create_tag_template(request)

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


def test_create_tag_template_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag_template(
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag_template_id
        mock_val = "tag_template_id_value"
        assert arg == mock_val
        arg = args[0].tag_template
        mock_val = tags.TagTemplate(name="name_value")
        assert arg == mock_val


def test_create_tag_template_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag_template(
            datacatalog.CreateTagTemplateRequest(),
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_template_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag_template(
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag_template_id
        mock_val = "tag_template_id_value"
        assert arg == mock_val
        arg = args[0].tag_template
        mock_val = tags.TagTemplate(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag_template(
            datacatalog.CreateTagTemplateRequest(),
            parent="parent_value",
            tag_template_id="tag_template_id_value",
            tag_template=tags.TagTemplate(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.GetTagTemplateRequest,
        dict,
    ],
)
def test_get_tag_template(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value",
            display_name="display_name_value",
            is_publicly_readable=True,
        )
        response = client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


def test_get_tag_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        client.get_tag_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetTagTemplateRequest()


@pytest.mark.asyncio
async def test_get_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.GetTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(
                name="name_value",
                display_name="display_name_value",
                is_publicly_readable=True,
            )
        )
        response = await client.get_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.GetTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


@pytest.mark.asyncio
async def test_get_tag_template_async_from_dict():
    await test_get_tag_template_async(request_type=dict)


def test_get_tag_template_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetTagTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        call.return_value = tags.TagTemplate()
        client.get_tag_template(request)

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
async def test_get_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.GetTagTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        await client.get_tag_template(request)

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


def test_get_tag_template_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tag_template(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tag_template_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tag_template(
            datacatalog.GetTagTemplateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tag_template_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag_template), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tag_template(
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
async def test_get_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tag_template(
            datacatalog.GetTagTemplateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UpdateTagTemplateRequest,
        dict,
    ],
)
def test_update_tag_template(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate(
            name="name_value",
            display_name="display_name_value",
            is_publicly_readable=True,
        )
        response = client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


def test_update_tag_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        client.update_tag_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateRequest()


@pytest.mark.asyncio
async def test_update_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplate(
                name="name_value",
                display_name="display_name_value",
                is_publicly_readable=True,
            )
        )
        response = await client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplate)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_publicly_readable is True


@pytest.mark.asyncio
async def test_update_tag_template_async_from_dict():
    await test_update_tag_template_async(request_type=dict)


def test_update_tag_template_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateRequest()

    request.tag_template.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        call.return_value = tags.TagTemplate()
        client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag_template.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateRequest()

    request.tag_template.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        await client.update_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag_template.name=name_value",
    ) in kw["metadata"]


def test_update_tag_template_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag_template(
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag_template
        mock_val = tags.TagTemplate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tag_template_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag_template(
            datacatalog.UpdateTagTemplateRequest(),
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_template_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.TagTemplate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag_template(
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag_template
        mock_val = tags.TagTemplate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag_template(
            datacatalog.UpdateTagTemplateRequest(),
            tag_template=tags.TagTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.DeleteTagTemplateRequest,
        dict,
    ],
)
def test_delete_tag_template(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        client.delete_tag_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateRequest()


@pytest.mark.asyncio
async def test_delete_tag_template_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteTagTemplateRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_tag_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_template_async_from_dict():
    await test_delete_tag_template_async(request_type=dict)


def test_delete_tag_template_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        call.return_value = None
        client.delete_tag_template(request)

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
async def test_delete_tag_template_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_tag_template(request)

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


def test_delete_tag_template_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag_template(
            name="name_value",
            force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].force
        mock_val = True
        assert arg == mock_val


def test_delete_tag_template_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag_template(
            datacatalog.DeleteTagTemplateRequest(),
            name="name_value",
            force=True,
        )


@pytest.mark.asyncio
async def test_delete_tag_template_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag_template(
            name="name_value",
            force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].force
        mock_val = True
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tag_template_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag_template(
            datacatalog.DeleteTagTemplateRequest(),
            name="name_value",
            force=True,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.CreateTagTemplateFieldRequest,
        dict,
    ],
)
def test_create_tag_template_field(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            description="description_value",
            order=540,
        )
        response = client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


def test_create_tag_template_field_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        client.create_tag_template_field()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateFieldRequest()


@pytest.mark.asyncio
async def test_create_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.CreateTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                description="description_value",
                order=540,
            )
        )
        response = await client.create_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


@pytest.mark.asyncio
async def test_create_tag_template_field_async_from_dict():
    await test_create_tag_template_field_async(request_type=dict)


def test_create_tag_template_field_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateFieldRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()
        client.create_tag_template_field(request)

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
async def test_create_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagTemplateFieldRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        await client.create_tag_template_field(request)

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


def test_create_tag_template_field_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag_template_field(
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag_template_field_id
        mock_val = "tag_template_field_id_value"
        assert arg == mock_val
        arg = args[0].tag_template_field
        mock_val = tags.TagTemplateField(name="name_value")
        assert arg == mock_val


def test_create_tag_template_field_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag_template_field(
            datacatalog.CreateTagTemplateFieldRequest(),
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag_template_field(
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag_template_field_id
        mock_val = "tag_template_field_id_value"
        assert arg == mock_val
        arg = args[0].tag_template_field
        mock_val = tags.TagTemplateField(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag_template_field(
            datacatalog.CreateTagTemplateFieldRequest(),
            parent="parent_value",
            tag_template_field_id="tag_template_field_id_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UpdateTagTemplateFieldRequest,
        dict,
    ],
)
def test_update_tag_template_field(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            description="description_value",
            order=540,
        )
        response = client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


def test_update_tag_template_field_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        client.update_tag_template_field()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateFieldRequest()


@pytest.mark.asyncio
async def test_update_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.UpdateTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                description="description_value",
                order=540,
            )
        )
        response = await client.update_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


@pytest.mark.asyncio
async def test_update_tag_template_field_async_from_dict():
    await test_update_tag_template_field_async(request_type=dict)


def test_update_tag_template_field_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()
        client.update_tag_template_field(request)

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
async def test_update_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        await client.update_tag_template_field(request)

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


def test_update_tag_template_field_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag_template_field(
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].tag_template_field
        mock_val = tags.TagTemplateField(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tag_template_field_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag_template_field(
            datacatalog.UpdateTagTemplateFieldRequest(),
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag_template_field(
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].tag_template_field
        mock_val = tags.TagTemplateField(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag_template_field(
            datacatalog.UpdateTagTemplateFieldRequest(),
            name="name_value",
            tag_template_field=tags.TagTemplateField(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.RenameTagTemplateFieldRequest,
        dict,
    ],
)
def test_rename_tag_template_field(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            description="description_value",
            order=540,
        )
        response = client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


def test_rename_tag_template_field_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        client.rename_tag_template_field()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldRequest()


@pytest.mark.asyncio
async def test_rename_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.RenameTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                description="description_value",
                order=540,
            )
        )
        response = await client.rename_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


@pytest.mark.asyncio
async def test_rename_tag_template_field_async_from_dict():
    await test_rename_tag_template_field_async(request_type=dict)


def test_rename_tag_template_field_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()
        client.rename_tag_template_field(request)

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
async def test_rename_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        await client.rename_tag_template_field(request)

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


def test_rename_tag_template_field_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rename_tag_template_field(
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_tag_template_field_id
        mock_val = "new_tag_template_field_id_value"
        assert arg == mock_val


def test_rename_tag_template_field_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_tag_template_field(
            datacatalog.RenameTagTemplateFieldRequest(),
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )


@pytest.mark.asyncio
async def test_rename_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rename_tag_template_field(
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_tag_template_field_id
        mock_val = "new_tag_template_field_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rename_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rename_tag_template_field(
            datacatalog.RenameTagTemplateFieldRequest(),
            name="name_value",
            new_tag_template_field_id="new_tag_template_field_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.RenameTagTemplateFieldEnumValueRequest,
        dict,
    ],
)
def test_rename_tag_template_field_enum_value(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField(
            name="name_value",
            display_name="display_name_value",
            is_required=True,
            description="description_value",
            order=540,
        )
        response = client.rename_tag_template_field_enum_value(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldEnumValueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


def test_rename_tag_template_field_enum_value_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        client.rename_tag_template_field_enum_value()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldEnumValueRequest()


@pytest.mark.asyncio
async def test_rename_tag_template_field_enum_value_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.RenameTagTemplateFieldEnumValueRequest,
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField(
                name="name_value",
                display_name="display_name_value",
                is_required=True,
                description="description_value",
                order=540,
            )
        )
        response = await client.rename_tag_template_field_enum_value(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.RenameTagTemplateFieldEnumValueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.TagTemplateField)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.is_required is True
    assert response.description == "description_value"
    assert response.order == 540


@pytest.mark.asyncio
async def test_rename_tag_template_field_enum_value_async_from_dict():
    await test_rename_tag_template_field_enum_value_async(request_type=dict)


def test_rename_tag_template_field_enum_value_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldEnumValueRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        call.return_value = tags.TagTemplateField()
        client.rename_tag_template_field_enum_value(request)

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
async def test_rename_tag_template_field_enum_value_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.RenameTagTemplateFieldEnumValueRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        await client.rename_tag_template_field_enum_value(request)

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


def test_rename_tag_template_field_enum_value_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rename_tag_template_field_enum_value(
            name="name_value",
            new_enum_value_display_name="new_enum_value_display_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_enum_value_display_name
        mock_val = "new_enum_value_display_name_value"
        assert arg == mock_val


def test_rename_tag_template_field_enum_value_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_tag_template_field_enum_value(
            datacatalog.RenameTagTemplateFieldEnumValueRequest(),
            name="name_value",
            new_enum_value_display_name="new_enum_value_display_name_value",
        )


@pytest.mark.asyncio
async def test_rename_tag_template_field_enum_value_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rename_tag_template_field_enum_value), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.TagTemplateField()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.TagTemplateField()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rename_tag_template_field_enum_value(
            name="name_value",
            new_enum_value_display_name="new_enum_value_display_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_enum_value_display_name
        mock_val = "new_enum_value_display_name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rename_tag_template_field_enum_value_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rename_tag_template_field_enum_value(
            datacatalog.RenameTagTemplateFieldEnumValueRequest(),
            name="name_value",
            new_enum_value_display_name="new_enum_value_display_name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.DeleteTagTemplateFieldRequest,
        dict,
    ],
)
def test_delete_tag_template_field(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_template_field_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        client.delete_tag_template_field()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateFieldRequest()


@pytest.mark.asyncio
async def test_delete_tag_template_field_async(
    transport: str = "grpc_asyncio",
    request_type=datacatalog.DeleteTagTemplateFieldRequest,
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_tag_template_field(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagTemplateFieldRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_template_field_async_from_dict():
    await test_delete_tag_template_field_async(request_type=dict)


def test_delete_tag_template_field_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        call.return_value = None
        client.delete_tag_template_field(request)

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
async def test_delete_tag_template_field_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagTemplateFieldRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_tag_template_field(request)

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


def test_delete_tag_template_field_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag_template_field(
            name="name_value",
            force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].force
        mock_val = True
        assert arg == mock_val


def test_delete_tag_template_field_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag_template_field(
            datacatalog.DeleteTagTemplateFieldRequest(),
            name="name_value",
            force=True,
        )


@pytest.mark.asyncio
async def test_delete_tag_template_field_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_tag_template_field), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag_template_field(
            name="name_value",
            force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].force
        mock_val = True
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_tag_template_field_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag_template_field(
            datacatalog.DeleteTagTemplateFieldRequest(),
            name="name_value",
            force=True,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.CreateTagRequest,
        dict,
    ],
)
def test_create_tag(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag(
            name="name_value",
            template="template_value",
            template_display_name="template_display_name_value",
            column="column_value",
        )
        response = client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)
    assert response.name == "name_value"
    assert response.template == "template_value"
    assert response.template_display_name == "template_display_name_value"


def test_create_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        client.create_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagRequest()


@pytest.mark.asyncio
async def test_create_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.CreateTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.Tag(
                name="name_value",
                template="template_value",
                template_display_name="template_display_name_value",
            )
        )
        response = await client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.CreateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)
    assert response.name == "name_value"
    assert response.template == "template_value"
    assert response.template_display_name == "template_display_name_value"


@pytest.mark.asyncio
async def test_create_tag_async_from_dict():
    await test_create_tag_async(request_type=dict)


def test_create_tag_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = tags.Tag()
        client.create_tag(request)

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
async def test_create_tag_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.CreateTagRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        await client.create_tag(request)

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


def test_create_tag_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag(
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag
        mock_val = tags.Tag(name="name_value")
        assert arg == mock_val


def test_create_tag_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag(
            datacatalog.CreateTagRequest(),
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_tag_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag(
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag
        mock_val = tags.Tag(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tag_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag(
            datacatalog.CreateTagRequest(),
            parent="parent_value",
            tag=tags.Tag(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UpdateTagRequest,
        dict,
    ],
)
def test_update_tag(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag(
            name="name_value",
            template="template_value",
            template_display_name="template_display_name_value",
            column="column_value",
        )
        response = client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)
    assert response.name == "name_value"
    assert response.template == "template_value"
    assert response.template_display_name == "template_display_name_value"


def test_update_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        client.update_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagRequest()


@pytest.mark.asyncio
async def test_update_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UpdateTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tags.Tag(
                name="name_value",
                template="template_value",
                template_display_name="template_display_name_value",
            )
        )
        response = await client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UpdateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tags.Tag)
    assert response.name == "name_value"
    assert response.template == "template_value"
    assert response.template_display_name == "template_display_name_value"


@pytest.mark.asyncio
async def test_update_tag_async_from_dict():
    await test_update_tag_async(request_type=dict)


def test_update_tag_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagRequest()

    request.tag.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = tags.Tag()
        client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UpdateTagRequest()

    request.tag.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        await client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "tag.name=name_value",
    ) in kw["metadata"]


def test_update_tag_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag(
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag
        mock_val = tags.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tag_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag(
            datacatalog.UpdateTagRequest(),
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tags.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tags.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag(
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag
        mock_val = tags.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tag_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag(
            datacatalog.UpdateTagRequest(),
            tag=tags.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.DeleteTagRequest,
        dict,
    ],
)
def test_delete_tag(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        client.delete_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagRequest()


@pytest.mark.asyncio
async def test_delete_tag_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.DeleteTagRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_async_from_dict():
    await test_delete_tag_async(request_type=dict)


def test_delete_tag_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        call.return_value = None
        client.delete_tag(request)

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
async def test_delete_tag_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.DeleteTagRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_tag(request)

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


def test_delete_tag_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_tag(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_tag_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag(
            datacatalog.DeleteTagRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tag_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_tag(
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
async def test_delete_tag_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag(
            datacatalog.DeleteTagRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ListTagsRequest,
        dict,
    ],
)
def test_list_tags(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tags_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        client.list_tags()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListTagsRequest()


@pytest.mark.asyncio
async def test_list_tags_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ListTagsRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ListTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tags_async_from_dict():
    await test_list_tags_async(request_type=dict)


def test_list_tags_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = datacatalog.ListTagsResponse()
        client.list_tags(request)

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
async def test_list_tags_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ListTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse()
        )
        await client.list_tags(request)

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


def test_list_tags_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tags(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tags_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tags(
            datacatalog.ListTagsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tags_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.ListTagsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.ListTagsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tags(
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
async def test_list_tags_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tags(
            datacatalog.ListTagsRequest(),
            parent="parent_value",
        )


def test_list_tags_pager(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                    tags.Tag(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tags(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tags.Tag) for i in results)


def test_list_tags_pages(transport_name: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                    tags.Tag(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tags(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tags_async_pager():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                    tags.Tag(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tags(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tags.Tag) for i in responses)


@pytest.mark.asyncio
async def test_list_tags_async_pages():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                    tags.Tag(),
                ],
                next_page_token="abc",
            ),
            datacatalog.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                ],
                next_page_token="ghi",
            ),
            datacatalog.ListTagsResponse(
                tags=[
                    tags.Tag(),
                    tags.Tag(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tags(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ReconcileTagsRequest,
        dict,
    ],
)
def test_reconcile_tags(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reconcile_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.reconcile_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ReconcileTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_reconcile_tags_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reconcile_tags), "__call__") as call:
        client.reconcile_tags()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ReconcileTagsRequest()


@pytest.mark.asyncio
async def test_reconcile_tags_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ReconcileTagsRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reconcile_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.reconcile_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ReconcileTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_reconcile_tags_async_from_dict():
    await test_reconcile_tags_async(request_type=dict)


def test_reconcile_tags_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ReconcileTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reconcile_tags), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.reconcile_tags(request)

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
async def test_reconcile_tags_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ReconcileTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reconcile_tags), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.reconcile_tags(request)

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
        datacatalog.StarEntryRequest,
        dict,
    ],
)
def test_star_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.StarEntryResponse()
        response = client.star_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.StarEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.StarEntryResponse)


def test_star_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        client.star_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.StarEntryRequest()


@pytest.mark.asyncio
async def test_star_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.StarEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.StarEntryResponse()
        )
        response = await client.star_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.StarEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.StarEntryResponse)


@pytest.mark.asyncio
async def test_star_entry_async_from_dict():
    await test_star_entry_async(request_type=dict)


def test_star_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.StarEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        call.return_value = datacatalog.StarEntryResponse()
        client.star_entry(request)

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
async def test_star_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.StarEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.StarEntryResponse()
        )
        await client.star_entry(request)

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


def test_star_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.StarEntryResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.star_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_star_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.star_entry(
            datacatalog.StarEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_star_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.star_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.StarEntryResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.StarEntryResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.star_entry(
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
async def test_star_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.star_entry(
            datacatalog.StarEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.UnstarEntryRequest,
        dict,
    ],
)
def test_unstar_entry(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.UnstarEntryResponse()
        response = client.unstar_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UnstarEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.UnstarEntryResponse)


def test_unstar_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        client.unstar_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UnstarEntryRequest()


@pytest.mark.asyncio
async def test_unstar_entry_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.UnstarEntryRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.UnstarEntryResponse()
        )
        response = await client.unstar_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.UnstarEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, datacatalog.UnstarEntryResponse)


@pytest.mark.asyncio
async def test_unstar_entry_async_from_dict():
    await test_unstar_entry_async(request_type=dict)


def test_unstar_entry_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UnstarEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        call.return_value = datacatalog.UnstarEntryResponse()
        client.unstar_entry(request)

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
async def test_unstar_entry_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.UnstarEntryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.UnstarEntryResponse()
        )
        await client.unstar_entry(request)

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


def test_unstar_entry_flattened():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.UnstarEntryResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.unstar_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_unstar_entry_flattened_error():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.unstar_entry(
            datacatalog.UnstarEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_unstar_entry_flattened_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.unstar_entry), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = datacatalog.UnstarEntryResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            datacatalog.UnstarEntryResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.unstar_entry(
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
async def test_unstar_entry_flattened_error_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.unstar_entry(
            datacatalog.UnstarEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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


def test_set_iam_policy_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

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
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())
        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogAsyncClient(
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
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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


def test_get_iam_policy_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

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
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()

    request.resource = "resource_value"

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
        "resource=resource_value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict_foreign():
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogAsyncClient(
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
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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


def test_test_iam_permissions_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

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
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    request.resource = "resource_value"

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
        "resource=resource_value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict_foreign():
    client = DataCatalogClient(
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


@pytest.mark.parametrize(
    "request_type",
    [
        datacatalog.ImportEntriesRequest,
        dict,
    ],
)
def test_import_entries(request_type, transport: str = "grpc"):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ImportEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_entries), "__call__") as call:
        client.import_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ImportEntriesRequest()


@pytest.mark.asyncio
async def test_import_entries_async(
    transport: str = "grpc_asyncio", request_type=datacatalog.ImportEntriesRequest
):
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_entries), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == datacatalog.ImportEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_entries_async_from_dict():
    await test_import_entries_async(request_type=dict)


def test_import_entries_field_headers():
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ImportEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_entries), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_entries(request)

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
async def test_import_entries_field_headers_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = datacatalog.ImportEntriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_entries), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_entries(request)

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


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataCatalogClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataCatalogClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataCatalogGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataCatalogGrpcTransport,
        transports.DataCatalogGrpcAsyncIOTransport,
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
    transport = DataCatalogClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DataCatalogGrpcTransport,
    )


def test_data_catalog_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_data_catalog_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.datacatalog_v1.services.data_catalog.transports.DataCatalogTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "search_catalog",
        "create_entry_group",
        "get_entry_group",
        "update_entry_group",
        "delete_entry_group",
        "list_entry_groups",
        "create_entry",
        "update_entry",
        "delete_entry",
        "get_entry",
        "lookup_entry",
        "list_entries",
        "modify_entry_overview",
        "modify_entry_contacts",
        "create_tag_template",
        "get_tag_template",
        "update_tag_template",
        "delete_tag_template",
        "create_tag_template_field",
        "update_tag_template_field",
        "rename_tag_template_field",
        "rename_tag_template_field_enum_value",
        "delete_tag_template_field",
        "create_tag",
        "update_tag",
        "delete_tag",
        "list_tags",
        "reconcile_tags",
        "star_entry",
        "unstar_entry",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "import_entries",
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


def test_data_catalog_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.datacatalog_v1.services.data_catalog.transports.DataCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataCatalogTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_catalog_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.datacatalog_v1.services.data_catalog.transports.DataCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataCatalogTransport()
        adc.assert_called_once()


def test_data_catalog_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataCatalogClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataCatalogGrpcTransport,
        transports.DataCatalogGrpcAsyncIOTransport,
    ],
)
def test_data_catalog_transport_auth_adc(transport_class):
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
        transports.DataCatalogGrpcTransport,
        transports.DataCatalogGrpcAsyncIOTransport,
    ],
)
def test_data_catalog_transport_auth_gdch_credentials(transport_class):
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
        (transports.DataCatalogGrpcTransport, grpc_helpers),
        (transports.DataCatalogGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_data_catalog_transport_create_channel(transport_class, grpc_helpers):
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
            "datacatalog.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="datacatalog.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_data_catalog_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_data_catalog_host_no_port(transport_name):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("datacatalog.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_data_catalog_host_with_port(transport_name):
    client = DataCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datacatalog.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("datacatalog.googleapis.com:8000")


def test_data_catalog_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataCatalogGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_data_catalog_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataCatalogGrpcAsyncIOTransport(
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
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_data_catalog_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.DataCatalogGrpcTransport, transports.DataCatalogGrpcAsyncIOTransport],
)
def test_data_catalog_transport_channel_mtls_with_adc(transport_class):
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


def test_data_catalog_grpc_lro_client():
    client = DataCatalogClient(
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


def test_data_catalog_grpc_lro_async_client():
    client = DataCatalogAsyncClient(
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


def test_entry_path():
    project = "squid"
    location = "clam"
    entry_group = "whelk"
    entry = "octopus"
    expected = "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}".format(
        project=project,
        location=location,
        entry_group=entry_group,
        entry=entry,
    )
    actual = DataCatalogClient.entry_path(project, location, entry_group, entry)
    assert expected == actual


def test_parse_entry_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "entry_group": "cuttlefish",
        "entry": "mussel",
    }
    path = DataCatalogClient.entry_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_entry_path(path)
    assert expected == actual


def test_entry_group_path():
    project = "winkle"
    location = "nautilus"
    entry_group = "scallop"
    expected = (
        "projects/{project}/locations/{location}/entryGroups/{entry_group}".format(
            project=project,
            location=location,
            entry_group=entry_group,
        )
    )
    actual = DataCatalogClient.entry_group_path(project, location, entry_group)
    assert expected == actual


def test_parse_entry_group_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "entry_group": "clam",
    }
    path = DataCatalogClient.entry_group_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_entry_group_path(path)
    assert expected == actual


def test_tag_path():
    project = "whelk"
    location = "octopus"
    entry_group = "oyster"
    entry = "nudibranch"
    tag = "cuttlefish"
    expected = "projects/{project}/locations/{location}/entryGroups/{entry_group}/entries/{entry}/tags/{tag}".format(
        project=project,
        location=location,
        entry_group=entry_group,
        entry=entry,
        tag=tag,
    )
    actual = DataCatalogClient.tag_path(project, location, entry_group, entry, tag)
    assert expected == actual


def test_parse_tag_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "entry_group": "nautilus",
        "entry": "scallop",
        "tag": "abalone",
    }
    path = DataCatalogClient.tag_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_path(path)
    assert expected == actual


def test_tag_template_path():
    project = "squid"
    location = "clam"
    tag_template = "whelk"
    expected = (
        "projects/{project}/locations/{location}/tagTemplates/{tag_template}".format(
            project=project,
            location=location,
            tag_template=tag_template,
        )
    )
    actual = DataCatalogClient.tag_template_path(project, location, tag_template)
    assert expected == actual


def test_parse_tag_template_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "tag_template": "nudibranch",
    }
    path = DataCatalogClient.tag_template_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_template_path(path)
    assert expected == actual


def test_tag_template_field_path():
    project = "cuttlefish"
    location = "mussel"
    tag_template = "winkle"
    field = "nautilus"
    expected = "projects/{project}/locations/{location}/tagTemplates/{tag_template}/fields/{field}".format(
        project=project,
        location=location,
        tag_template=tag_template,
        field=field,
    )
    actual = DataCatalogClient.tag_template_field_path(
        project, location, tag_template, field
    )
    assert expected == actual


def test_parse_tag_template_field_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "tag_template": "squid",
        "field": "clam",
    }
    path = DataCatalogClient.tag_template_field_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_template_field_path(path)
    assert expected == actual


def test_tag_template_field_enum_value_path():
    project = "whelk"
    location = "octopus"
    tag_template = "oyster"
    tag_template_field_id = "nudibranch"
    enum_value_display_name = "cuttlefish"
    expected = "projects/{project}/locations/{location}/tagTemplates/{tag_template}/fields/{tag_template_field_id}/enumValues/{enum_value_display_name}".format(
        project=project,
        location=location,
        tag_template=tag_template,
        tag_template_field_id=tag_template_field_id,
        enum_value_display_name=enum_value_display_name,
    )
    actual = DataCatalogClient.tag_template_field_enum_value_path(
        project, location, tag_template, tag_template_field_id, enum_value_display_name
    )
    assert expected == actual


def test_parse_tag_template_field_enum_value_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "tag_template": "nautilus",
        "tag_template_field_id": "scallop",
        "enum_value_display_name": "abalone",
    }
    path = DataCatalogClient.tag_template_field_enum_value_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_tag_template_field_enum_value_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataCatalogClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = DataCatalogClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DataCatalogClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = DataCatalogClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DataCatalogClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = DataCatalogClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DataCatalogClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = DataCatalogClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DataCatalogClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = DataCatalogClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataCatalogClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataCatalogClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DataCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_delete_operation(transport: str = "grpc"):
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
    client = DataCatalogClient(
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
    client = DataCatalogAsyncClient(
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
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = DataCatalogClient(
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
        client = DataCatalogClient(
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
        (DataCatalogClient, transports.DataCatalogGrpcTransport),
        (DataCatalogAsyncClient, transports.DataCatalogGrpcAsyncIOTransport),
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
