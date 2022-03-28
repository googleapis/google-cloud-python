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
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import (
    BigtableTableAdminAsyncClient,
)
from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import (
    BigtableTableAdminClient,
)
from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import pagers
from google.cloud.bigtable_admin_v2.services.bigtable_table_admin import transports
from google.cloud.bigtable_admin_v2.types import bigtable_table_admin
from google.cloud.bigtable_admin_v2.types import table
from google.cloud.bigtable_admin_v2.types import table as gba_table
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
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

    assert BigtableTableAdminClient._get_default_mtls_endpoint(None) is None
    assert (
        BigtableTableAdminClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigtableTableAdminClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigtableTableAdminClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigtableTableAdminClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigtableTableAdminClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [
        BigtableTableAdminClient,
        BigtableTableAdminAsyncClient,
    ],
)
def test_bigtable_table_admin_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigtableadmin.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.BigtableTableAdminGrpcTransport, "grpc"),
        (transports.BigtableTableAdminGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_bigtable_table_admin_client_service_account_always_use_jwt(
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
    "client_class",
    [
        BigtableTableAdminClient,
        BigtableTableAdminAsyncClient,
    ],
)
def test_bigtable_table_admin_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigtableadmin.googleapis.com:443"


def test_bigtable_table_admin_client_get_transport_class():
    transport = BigtableTableAdminClient.get_transport_class()
    available_transports = [
        transports.BigtableTableAdminGrpcTransport,
    ]
    assert transport in available_transports

    transport = BigtableTableAdminClient.get_transport_class("grpc")
    assert transport == transports.BigtableTableAdminGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigtableTableAdminClient, transports.BigtableTableAdminGrpcTransport, "grpc"),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    BigtableTableAdminClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminClient),
)
@mock.patch.object(
    BigtableTableAdminAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminAsyncClient),
)
def test_bigtable_table_admin_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BigtableTableAdminClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BigtableTableAdminClient, "get_transport_class") as gtc:
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            BigtableTableAdminClient,
            transports.BigtableTableAdminGrpcTransport,
            "grpc",
            "true",
        ),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            BigtableTableAdminClient,
            transports.BigtableTableAdminGrpcTransport,
            "grpc",
            "false",
        ),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    BigtableTableAdminClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminClient),
)
@mock.patch.object(
    BigtableTableAdminAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_bigtable_table_admin_client_mtls_env_auto(
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
                )


@pytest.mark.parametrize(
    "client_class", [BigtableTableAdminClient, BigtableTableAdminAsyncClient]
)
@mock.patch.object(
    BigtableTableAdminClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminClient),
)
@mock.patch.object(
    BigtableTableAdminAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigtableTableAdminAsyncClient),
)
def test_bigtable_table_admin_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (BigtableTableAdminClient, transports.BigtableTableAdminGrpcTransport, "grpc"),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_bigtable_table_admin_client_client_options_scopes(
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            BigtableTableAdminClient,
            transports.BigtableTableAdminGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_bigtable_table_admin_client_client_options_credentials_file(
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
        )


def test_bigtable_table_admin_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigtable_admin_v2.services.bigtable_table_admin.transports.BigtableTableAdminGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BigtableTableAdminClient(
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
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            BigtableTableAdminClient,
            transports.BigtableTableAdminGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_bigtable_table_admin_client_create_channel_credentials_file(
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
            "bigtableadmin.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.admin",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-bigtable.admin",
                "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=None,
            default_host="bigtableadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.CreateTableRequest,
        dict,
    ],
)
def test_create_table(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gba_table.Table(
            name="name_value",
            granularity=gba_table.Table.TimestampGranularity.MILLIS,
        )
        response = client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gba_table.Table)
    assert response.name == "name_value"
    assert response.granularity == gba_table.Table.TimestampGranularity.MILLIS


def test_create_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        client.create_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableRequest()


@pytest.mark.asyncio
async def test_create_table_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.CreateTableRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gba_table.Table(
                name="name_value",
                granularity=gba_table.Table.TimestampGranularity.MILLIS,
            )
        )
        response = await client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gba_table.Table)
    assert response.name == "name_value"
    assert response.granularity == gba_table.Table.TimestampGranularity.MILLIS


@pytest.mark.asyncio
async def test_create_table_async_from_dict():
    await test_create_table_async(request_type=dict)


def test_create_table_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateTableRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        call.return_value = gba_table.Table()
        client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_table_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateTableRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gba_table.Table())
        await client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_table_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gba_table.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_table(
            parent="parent_value",
            table_id="table_id_value",
            table=gba_table.Table(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val
        arg = args[0].table
        mock_val = gba_table.Table(name="name_value")
        assert arg == mock_val


def test_create_table_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_table(
            bigtable_table_admin.CreateTableRequest(),
            parent="parent_value",
            table_id="table_id_value",
            table=gba_table.Table(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_table_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gba_table.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gba_table.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_table(
            parent="parent_value",
            table_id="table_id_value",
            table=gba_table.Table(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val
        arg = args[0].table
        mock_val = gba_table.Table(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_table_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_table(
            bigtable_table_admin.CreateTableRequest(),
            parent="parent_value",
            table_id="table_id_value",
            table=gba_table.Table(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.CreateTableFromSnapshotRequest,
        dict,
    ],
)
def test_create_table_from_snapshot(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_table_from_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableFromSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_table_from_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        client.create_table_from_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableFromSnapshotRequest()


@pytest.mark.asyncio
async def test_create_table_from_snapshot_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.CreateTableFromSnapshotRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_table_from_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateTableFromSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_table_from_snapshot_async_from_dict():
    await test_create_table_from_snapshot_async(request_type=dict)


def test_create_table_from_snapshot_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateTableFromSnapshotRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_table_from_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_table_from_snapshot_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateTableFromSnapshotRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_table_from_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_table_from_snapshot_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_table_from_snapshot(
            parent="parent_value",
            table_id="table_id_value",
            source_snapshot="source_snapshot_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val
        arg = args[0].source_snapshot
        mock_val = "source_snapshot_value"
        assert arg == mock_val


def test_create_table_from_snapshot_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_table_from_snapshot(
            bigtable_table_admin.CreateTableFromSnapshotRequest(),
            parent="parent_value",
            table_id="table_id_value",
            source_snapshot="source_snapshot_value",
        )


@pytest.mark.asyncio
async def test_create_table_from_snapshot_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_table_from_snapshot), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_table_from_snapshot(
            parent="parent_value",
            table_id="table_id_value",
            source_snapshot="source_snapshot_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val
        arg = args[0].source_snapshot
        mock_val = "source_snapshot_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_table_from_snapshot_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_table_from_snapshot(
            bigtable_table_admin.CreateTableFromSnapshotRequest(),
            parent="parent_value",
            table_id="table_id_value",
            source_snapshot="source_snapshot_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.ListTablesRequest,
        dict,
    ],
)
def test_list_tables(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListTablesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListTablesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTablesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tables_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        client.list_tables()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListTablesRequest()


@pytest.mark.asyncio
async def test_list_tables_async(
    transport: str = "grpc_asyncio", request_type=bigtable_table_admin.ListTablesRequest
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListTablesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListTablesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTablesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tables_async_from_dict():
    await test_list_tables_async(request_type=dict)


def test_list_tables_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListTablesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        call.return_value = bigtable_table_admin.ListTablesResponse()
        client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tables_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListTablesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListTablesResponse()
        )
        await client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_tables_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListTablesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tables(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tables_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tables(
            bigtable_table_admin.ListTablesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tables_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListTablesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListTablesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tables(
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
async def test_list_tables_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tables(
            bigtable_table_admin.ListTablesRequest(),
            parent="parent_value",
        )


def test_list_tables_pager(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                    table.Table(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tables(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, table.Table) for i in results)


def test_list_tables_pages(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                    table.Table(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tables(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tables_async_pager():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tables), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                    table.Table(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tables(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, table.Table) for i in responses)


@pytest.mark.asyncio
async def test_list_tables_async_pages():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tables), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                    table.Table(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListTablesResponse(
                tables=[
                    table.Table(),
                    table.Table(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_tables(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.GetTableRequest,
        dict,
    ],
)
def test_get_table(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table(
            name="name_value",
            granularity=table.Table.TimestampGranularity.MILLIS,
        )
        response = client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Table)
    assert response.name == "name_value"
    assert response.granularity == table.Table.TimestampGranularity.MILLIS


def test_get_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        client.get_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetTableRequest()


@pytest.mark.asyncio
async def test_get_table_async(
    transport: str = "grpc_asyncio", request_type=bigtable_table_admin.GetTableRequest
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table.Table(
                name="name_value",
                granularity=table.Table.TimestampGranularity.MILLIS,
            )
        )
        response = await client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Table)
    assert response.name == "name_value"
    assert response.granularity == table.Table.TimestampGranularity.MILLIS


@pytest.mark.asyncio
async def test_get_table_async_from_dict():
    await test_get_table_async(request_type=dict)


def test_get_table_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        call.return_value = table.Table()
        client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_table_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Table())
        await client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_table_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_table(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_table_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_table(
            bigtable_table_admin.GetTableRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_table_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_table(
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
async def test_get_table_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_table(
            bigtable_table_admin.GetTableRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.DeleteTableRequest,
        dict,
    ],
)
def test_delete_table(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteTableRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        client.delete_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteTableRequest()


@pytest.mark.asyncio
async def test_delete_table_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.DeleteTableRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteTableRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_table_async_from_dict():
    await test_delete_table_async(request_type=dict)


def test_delete_table_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        call.return_value = None
        client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_table_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_table_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_table(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_table_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_table(
            bigtable_table_admin.DeleteTableRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_table_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_table(
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
async def test_delete_table_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_table(
            bigtable_table_admin.DeleteTableRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.ModifyColumnFamiliesRequest,
        dict,
    ],
)
def test_modify_column_families(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table(
            name="name_value",
            granularity=table.Table.TimestampGranularity.MILLIS,
        )
        response = client.modify_column_families(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ModifyColumnFamiliesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Table)
    assert response.name == "name_value"
    assert response.granularity == table.Table.TimestampGranularity.MILLIS


def test_modify_column_families_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        client.modify_column_families()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ModifyColumnFamiliesRequest()


@pytest.mark.asyncio
async def test_modify_column_families_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.ModifyColumnFamiliesRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table.Table(
                name="name_value",
                granularity=table.Table.TimestampGranularity.MILLIS,
            )
        )
        response = await client.modify_column_families(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ModifyColumnFamiliesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Table)
    assert response.name == "name_value"
    assert response.granularity == table.Table.TimestampGranularity.MILLIS


@pytest.mark.asyncio
async def test_modify_column_families_async_from_dict():
    await test_modify_column_families_async(request_type=dict)


def test_modify_column_families_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ModifyColumnFamiliesRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        call.return_value = table.Table()
        client.modify_column_families(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_modify_column_families_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ModifyColumnFamiliesRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Table())
        await client.modify_column_families(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_modify_column_families_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.modify_column_families(
            name="name_value",
            modifications=[
                bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(
                    id="id_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].modifications
        mock_val = [
            bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(id="id_value")
        ]
        assert arg == mock_val


def test_modify_column_families_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.modify_column_families(
            bigtable_table_admin.ModifyColumnFamiliesRequest(),
            name="name_value",
            modifications=[
                bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(
                    id="id_value"
                )
            ],
        )


@pytest.mark.asyncio
async def test_modify_column_families_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.modify_column_families), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.modify_column_families(
            name="name_value",
            modifications=[
                bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(
                    id="id_value"
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].modifications
        mock_val = [
            bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(id="id_value")
        ]
        assert arg == mock_val


@pytest.mark.asyncio
async def test_modify_column_families_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.modify_column_families(
            bigtable_table_admin.ModifyColumnFamiliesRequest(),
            name="name_value",
            modifications=[
                bigtable_table_admin.ModifyColumnFamiliesRequest.Modification(
                    id="id_value"
                )
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.DropRowRangeRequest,
        dict,
    ],
)
def test_drop_row_range(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.drop_row_range), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.drop_row_range(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DropRowRangeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_drop_row_range_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.drop_row_range), "__call__") as call:
        client.drop_row_range()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DropRowRangeRequest()


@pytest.mark.asyncio
async def test_drop_row_range_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.DropRowRangeRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.drop_row_range), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.drop_row_range(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DropRowRangeRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_drop_row_range_async_from_dict():
    await test_drop_row_range_async(request_type=dict)


def test_drop_row_range_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DropRowRangeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.drop_row_range), "__call__") as call:
        call.return_value = None
        client.drop_row_range(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_drop_row_range_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DropRowRangeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.drop_row_range), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.drop_row_range(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.GenerateConsistencyTokenRequest,
        dict,
    ],
)
def test_generate_consistency_token(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.GenerateConsistencyTokenResponse(
            consistency_token="consistency_token_value",
        )
        response = client.generate_consistency_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GenerateConsistencyTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable_table_admin.GenerateConsistencyTokenResponse)
    assert response.consistency_token == "consistency_token_value"


def test_generate_consistency_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        client.generate_consistency_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GenerateConsistencyTokenRequest()


@pytest.mark.asyncio
async def test_generate_consistency_token_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.GenerateConsistencyTokenRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.GenerateConsistencyTokenResponse(
                consistency_token="consistency_token_value",
            )
        )
        response = await client.generate_consistency_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GenerateConsistencyTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable_table_admin.GenerateConsistencyTokenResponse)
    assert response.consistency_token == "consistency_token_value"


@pytest.mark.asyncio
async def test_generate_consistency_token_async_from_dict():
    await test_generate_consistency_token_async(request_type=dict)


def test_generate_consistency_token_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GenerateConsistencyTokenRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        call.return_value = bigtable_table_admin.GenerateConsistencyTokenResponse()
        client.generate_consistency_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_consistency_token_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GenerateConsistencyTokenRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.GenerateConsistencyTokenResponse()
        )
        await client.generate_consistency_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_generate_consistency_token_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.GenerateConsistencyTokenResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_consistency_token(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_generate_consistency_token_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_consistency_token(
            bigtable_table_admin.GenerateConsistencyTokenRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_generate_consistency_token_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_consistency_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.GenerateConsistencyTokenResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.GenerateConsistencyTokenResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_consistency_token(
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
async def test_generate_consistency_token_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_consistency_token(
            bigtable_table_admin.GenerateConsistencyTokenRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.CheckConsistencyRequest,
        dict,
    ],
)
def test_check_consistency(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.CheckConsistencyResponse(
            consistent=True,
        )
        response = client.check_consistency(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CheckConsistencyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable_table_admin.CheckConsistencyResponse)
    assert response.consistent is True


def test_check_consistency_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        client.check_consistency()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CheckConsistencyRequest()


@pytest.mark.asyncio
async def test_check_consistency_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.CheckConsistencyRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.CheckConsistencyResponse(
                consistent=True,
            )
        )
        response = await client.check_consistency(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CheckConsistencyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigtable_table_admin.CheckConsistencyResponse)
    assert response.consistent is True


@pytest.mark.asyncio
async def test_check_consistency_async_from_dict():
    await test_check_consistency_async(request_type=dict)


def test_check_consistency_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CheckConsistencyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        call.return_value = bigtable_table_admin.CheckConsistencyResponse()
        client.check_consistency(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_check_consistency_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CheckConsistencyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.CheckConsistencyResponse()
        )
        await client.check_consistency(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_check_consistency_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.CheckConsistencyResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.check_consistency(
            name="name_value",
            consistency_token="consistency_token_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].consistency_token
        mock_val = "consistency_token_value"
        assert arg == mock_val


def test_check_consistency_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.check_consistency(
            bigtable_table_admin.CheckConsistencyRequest(),
            name="name_value",
            consistency_token="consistency_token_value",
        )


@pytest.mark.asyncio
async def test_check_consistency_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.check_consistency), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.CheckConsistencyResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.CheckConsistencyResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.check_consistency(
            name="name_value",
            consistency_token="consistency_token_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].consistency_token
        mock_val = "consistency_token_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_check_consistency_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.check_consistency(
            bigtable_table_admin.CheckConsistencyRequest(),
            name="name_value",
            consistency_token="consistency_token_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.SnapshotTableRequest,
        dict,
    ],
)
def test_snapshot_table(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.snapshot_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.SnapshotTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_snapshot_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        client.snapshot_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.SnapshotTableRequest()


@pytest.mark.asyncio
async def test_snapshot_table_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.SnapshotTableRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.snapshot_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.SnapshotTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_snapshot_table_async_from_dict():
    await test_snapshot_table_async(request_type=dict)


def test_snapshot_table_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.SnapshotTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.snapshot_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_snapshot_table_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.SnapshotTableRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.snapshot_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_snapshot_table_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.snapshot_table(
            name="name_value",
            cluster="cluster_value",
            snapshot_id="snapshot_id_value",
            description="description_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val
        arg = args[0].snapshot_id
        mock_val = "snapshot_id_value"
        assert arg == mock_val
        arg = args[0].description
        mock_val = "description_value"
        assert arg == mock_val


def test_snapshot_table_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.snapshot_table(
            bigtable_table_admin.SnapshotTableRequest(),
            name="name_value",
            cluster="cluster_value",
            snapshot_id="snapshot_id_value",
            description="description_value",
        )


@pytest.mark.asyncio
async def test_snapshot_table_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.snapshot_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.snapshot_table(
            name="name_value",
            cluster="cluster_value",
            snapshot_id="snapshot_id_value",
            description="description_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val
        arg = args[0].snapshot_id
        mock_val = "snapshot_id_value"
        assert arg == mock_val
        arg = args[0].description
        mock_val = "description_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_snapshot_table_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.snapshot_table(
            bigtable_table_admin.SnapshotTableRequest(),
            name="name_value",
            cluster="cluster_value",
            snapshot_id="snapshot_id_value",
            description="description_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.GetSnapshotRequest,
        dict,
    ],
)
def test_get_snapshot(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Snapshot(
            name="name_value",
            data_size_bytes=1594,
            state=table.Snapshot.State.READY,
            description="description_value",
        )
        response = client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Snapshot)
    assert response.name == "name_value"
    assert response.data_size_bytes == 1594
    assert response.state == table.Snapshot.State.READY
    assert response.description == "description_value"


def test_get_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        client.get_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetSnapshotRequest()


@pytest.mark.asyncio
async def test_get_snapshot_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.GetSnapshotRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table.Snapshot(
                name="name_value",
                data_size_bytes=1594,
                state=table.Snapshot.State.READY,
                description="description_value",
            )
        )
        response = await client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Snapshot)
    assert response.name == "name_value"
    assert response.data_size_bytes == 1594
    assert response.state == table.Snapshot.State.READY
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_snapshot_async_from_dict():
    await test_get_snapshot_async(request_type=dict)


def test_get_snapshot_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetSnapshotRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        call.return_value = table.Snapshot()
        client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_snapshot_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetSnapshotRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Snapshot())
        await client.get_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_snapshot_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Snapshot()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_snapshot(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_snapshot_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_snapshot(
            bigtable_table_admin.GetSnapshotRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_snapshot_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Snapshot()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Snapshot())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_snapshot(
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
async def test_get_snapshot_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_snapshot(
            bigtable_table_admin.GetSnapshotRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.ListSnapshotsRequest,
        dict,
    ],
)
def test_list_snapshots(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListSnapshotsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListSnapshotsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSnapshotsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_snapshots_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        client.list_snapshots()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListSnapshotsRequest()


@pytest.mark.asyncio
async def test_list_snapshots_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.ListSnapshotsRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListSnapshotsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListSnapshotsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSnapshotsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_snapshots_async_from_dict():
    await test_list_snapshots_async(request_type=dict)


def test_list_snapshots_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListSnapshotsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        call.return_value = bigtable_table_admin.ListSnapshotsResponse()
        client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_snapshots_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListSnapshotsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListSnapshotsResponse()
        )
        await client.list_snapshots(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_snapshots_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListSnapshotsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_snapshots(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_snapshots_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_snapshots(
            bigtable_table_admin.ListSnapshotsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_snapshots_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListSnapshotsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListSnapshotsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_snapshots(
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
async def test_list_snapshots_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_snapshots(
            bigtable_table_admin.ListSnapshotsRequest(),
            parent="parent_value",
        )


def test_list_snapshots_pager(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                    table.Snapshot(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_snapshots(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, table.Snapshot) for i in results)


def test_list_snapshots_pages(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_snapshots), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                    table.Snapshot(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_snapshots(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_snapshots_async_pager():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_snapshots), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                    table.Snapshot(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_snapshots(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, table.Snapshot) for i in responses)


@pytest.mark.asyncio
async def test_list_snapshots_async_pages():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_snapshots), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                    table.Snapshot(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListSnapshotsResponse(
                snapshots=[
                    table.Snapshot(),
                    table.Snapshot(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_snapshots(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.DeleteSnapshotRequest,
        dict,
    ],
)
def test_delete_snapshot(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_snapshot_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        client.delete_snapshot()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteSnapshotRequest()


@pytest.mark.asyncio
async def test_delete_snapshot_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.DeleteSnapshotRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteSnapshotRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_snapshot_async_from_dict():
    await test_delete_snapshot_async(request_type=dict)


def test_delete_snapshot_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteSnapshotRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        call.return_value = None
        client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_snapshot_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteSnapshotRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_snapshot(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_snapshot_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_snapshot(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_snapshot_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_snapshot(
            bigtable_table_admin.DeleteSnapshotRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_snapshot_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_snapshot), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_snapshot(
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
async def test_delete_snapshot_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_snapshot(
            bigtable_table_admin.DeleteSnapshotRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.CreateBackupRequest,
        dict,
    ],
)
def test_create_backup(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        client.create_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateBackupRequest()


@pytest.mark.asyncio
async def test_create_backup_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.CreateBackupRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_backup_async_from_dict():
    await test_create_backup_async(request_type=dict)


def test_create_backup_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateBackupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_backup_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.CreateBackupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_backup_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_backup(
            parent="parent_value",
            backup_id="backup_id_value",
            backup=table.Backup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = "backup_id_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = table.Backup(name="name_value")
        assert arg == mock_val


def test_create_backup_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            bigtable_table_admin.CreateBackupRequest(),
            parent="parent_value",
            backup_id="backup_id_value",
            backup=table.Backup(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_backup_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_backup(
            parent="parent_value",
            backup_id="backup_id_value",
            backup=table.Backup(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = "backup_id_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = table.Backup(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_backup_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_backup(
            bigtable_table_admin.CreateBackupRequest(),
            parent="parent_value",
            backup_id="backup_id_value",
            backup=table.Backup(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.GetBackupRequest,
        dict,
    ],
)
def test_get_backup(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup(
            name="name_value",
            source_table="source_table_value",
            size_bytes=1089,
            state=table.Backup.State.CREATING,
        )
        response = client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Backup)
    assert response.name == "name_value"
    assert response.source_table == "source_table_value"
    assert response.size_bytes == 1089
    assert response.state == table.Backup.State.CREATING


def test_get_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        client.get_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetBackupRequest()


@pytest.mark.asyncio
async def test_get_backup_async(
    transport: str = "grpc_asyncio", request_type=bigtable_table_admin.GetBackupRequest
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table.Backup(
                name="name_value",
                source_table="source_table_value",
                size_bytes=1089,
                state=table.Backup.State.CREATING,
            )
        )
        response = await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Backup)
    assert response.name == "name_value"
    assert response.source_table == "source_table_value"
    assert response.size_bytes == 1089
    assert response.state == table.Backup.State.CREATING


@pytest.mark.asyncio
async def test_get_backup_async_from_dict():
    await test_get_backup_async(request_type=dict)


def test_get_backup_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = table.Backup()
        client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_backup_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.GetBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Backup())
        await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_backup_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_backup(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_backup_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            bigtable_table_admin.GetBackupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_backup_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Backup())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_backup(
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
async def test_get_backup_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_backup(
            bigtable_table_admin.GetBackupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.UpdateBackupRequest,
        dict,
    ],
)
def test_update_backup(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup(
            name="name_value",
            source_table="source_table_value",
            size_bytes=1089,
            state=table.Backup.State.CREATING,
        )
        response = client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.UpdateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Backup)
    assert response.name == "name_value"
    assert response.source_table == "source_table_value"
    assert response.size_bytes == 1089
    assert response.state == table.Backup.State.CREATING


def test_update_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        client.update_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.UpdateBackupRequest()


@pytest.mark.asyncio
async def test_update_backup_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.UpdateBackupRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table.Backup(
                name="name_value",
                source_table="source_table_value",
                size_bytes=1089,
                state=table.Backup.State.CREATING,
            )
        )
        response = await client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.UpdateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table.Backup)
    assert response.name == "name_value"
    assert response.source_table == "source_table_value"
    assert response.size_bytes == 1089
    assert response.state == table.Backup.State.CREATING


@pytest.mark.asyncio
async def test_update_backup_async_from_dict():
    await test_update_backup_async(request_type=dict)


def test_update_backup_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.UpdateBackupRequest()

    request.backup.name = "backup.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        call.return_value = table.Backup()
        client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "backup.name=backup.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_backup_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.UpdateBackupRequest()

    request.backup.name = "backup.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Backup())
        await client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "backup.name=backup.name/value",
    ) in kw["metadata"]


def test_update_backup_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_backup(
            backup=table.Backup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup
        mock_val = table.Backup(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_backup_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_backup(
            bigtable_table_admin.UpdateBackupRequest(),
            backup=table.Backup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_backup_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table.Backup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(table.Backup())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_backup(
            backup=table.Backup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup
        mock_val = table.Backup(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_backup_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_backup(
            bigtable_table_admin.UpdateBackupRequest(),
            backup=table.Backup(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.DeleteBackupRequest,
        dict,
    ],
)
def test_delete_backup(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        client.delete_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteBackupRequest()


@pytest.mark.asyncio
async def test_delete_backup_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.DeleteBackupRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_backup_async_from_dict():
    await test_delete_backup_async(request_type=dict)


def test_delete_backup_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = None
        client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_backup_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.DeleteBackupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_backup_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_backup(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_backup_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            bigtable_table_admin.DeleteBackupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_backup_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_backup(
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
async def test_delete_backup_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_backup(
            bigtable_table_admin.DeleteBackupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.ListBackupsRequest,
        dict,
    ],
)
def test_list_backups(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListBackupsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_backups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        client.list_backups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListBackupsRequest()


@pytest.mark.asyncio
async def test_list_backups_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.ListBackupsRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListBackupsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_backups_async_from_dict():
    await test_list_backups_async(request_type=dict)


def test_list_backups_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListBackupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = bigtable_table_admin.ListBackupsResponse()
        client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_backups_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.ListBackupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListBackupsResponse()
        )
        await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_backups_flattened():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListBackupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_backups(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_backups_flattened_error():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            bigtable_table_admin.ListBackupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_backups_flattened_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigtable_table_admin.ListBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigtable_table_admin.ListBackupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_backups(
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
async def test_list_backups_flattened_error_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_backups(
            bigtable_table_admin.ListBackupsRequest(),
            parent="parent_value",
        )


def test_list_backups_pager(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                    table.Backup(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_backups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, table.Backup) for i in results)


def test_list_backups_pages(transport_name: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                    table.Backup(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_backups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_backups_async_pager():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                    table.Backup(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_backups(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, table.Backup) for i in responses)


@pytest.mark.asyncio
async def test_list_backups_async_pages():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                    table.Backup(),
                ],
                next_page_token="abc",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                ],
                next_page_token="ghi",
            ),
            bigtable_table_admin.ListBackupsResponse(
                backups=[
                    table.Backup(),
                    table.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_backups(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        bigtable_table_admin.RestoreTableRequest,
        dict,
    ],
)
def test_restore_table(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restore_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.RestoreTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restore_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_table), "__call__") as call:
        client.restore_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.RestoreTableRequest()


@pytest.mark.asyncio
async def test_restore_table_async(
    transport: str = "grpc_asyncio",
    request_type=bigtable_table_admin.RestoreTableRequest,
):
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restore_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == bigtable_table_admin.RestoreTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restore_table_async_from_dict():
    await test_restore_table_async(request_type=dict)


def test_restore_table_field_headers():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.RestoreTableRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_table), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_restore_table_field_headers_async():
    client = BigtableTableAdminAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = bigtable_table_admin.RestoreTableRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restore_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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


def test_get_iam_policy_from_dict_foreign():
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict_foreign():
    client = BigtableTableAdminClient(
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


def test_set_iam_policy_flattened():
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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


def test_test_iam_permissions_from_dict_foreign():
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminClient(
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
    client = BigtableTableAdminAsyncClient(
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
    client = BigtableTableAdminAsyncClient(
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


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableTableAdminClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableTableAdminClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BigtableTableAdminClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BigtableTableAdminClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigtableTableAdminClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BigtableTableAdminClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigtableTableAdminGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BigtableTableAdminGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigtableTableAdminGrpcTransport,
        transports.BigtableTableAdminGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.BigtableTableAdminGrpcTransport,
    )


def test_bigtable_table_admin_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BigtableTableAdminTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_bigtable_table_admin_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigtable_admin_v2.services.bigtable_table_admin.transports.BigtableTableAdminTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BigtableTableAdminTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_table",
        "create_table_from_snapshot",
        "list_tables",
        "get_table",
        "delete_table",
        "modify_column_families",
        "drop_row_range",
        "generate_consistency_token",
        "check_consistency",
        "snapshot_table",
        "get_snapshot",
        "list_snapshots",
        "delete_snapshot",
        "create_backup",
        "get_backup",
        "update_backup",
        "delete_backup",
        "list_backups",
        "restore_table",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
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


def test_bigtable_table_admin_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigtable_admin_v2.services.bigtable_table_admin.transports.BigtableTableAdminTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BigtableTableAdminTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.admin",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-bigtable.admin",
                "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_bigtable_table_admin_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigtable_admin_v2.services.bigtable_table_admin.transports.BigtableTableAdminTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BigtableTableAdminTransport()
        adc.assert_called_once()


def test_bigtable_table_admin_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BigtableTableAdminClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.admin",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-bigtable.admin",
                "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigtableTableAdminGrpcTransport,
        transports.BigtableTableAdminGrpcAsyncIOTransport,
    ],
)
def test_bigtable_table_admin_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.admin",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-bigtable.admin",
                "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.BigtableTableAdminGrpcTransport, grpc_helpers),
        (transports.BigtableTableAdminGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_bigtable_table_admin_transport_create_channel(transport_class, grpc_helpers):
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
            "bigtableadmin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/bigtable.admin",
                "https://www.googleapis.com/auth/bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-bigtable.admin",
                "https://www.googleapis.com/auth/cloud-bigtable.admin.table",
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=["1", "2"],
            default_host="bigtableadmin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigtableTableAdminGrpcTransport,
        transports.BigtableTableAdminGrpcAsyncIOTransport,
    ],
)
def test_bigtable_table_admin_grpc_transport_client_cert_source_for_mtls(
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


def test_bigtable_table_admin_host_no_port():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigtableadmin.googleapis.com"
        ),
    )
    assert client.transport._host == "bigtableadmin.googleapis.com:443"


def test_bigtable_table_admin_host_with_port():
    client = BigtableTableAdminClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigtableadmin.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "bigtableadmin.googleapis.com:8000"


def test_bigtable_table_admin_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigtableTableAdminGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_bigtable_table_admin_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BigtableTableAdminGrpcAsyncIOTransport(
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
        transports.BigtableTableAdminGrpcTransport,
        transports.BigtableTableAdminGrpcAsyncIOTransport,
    ],
)
def test_bigtable_table_admin_transport_channel_mtls_with_client_cert_source(
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
        transports.BigtableTableAdminGrpcTransport,
        transports.BigtableTableAdminGrpcAsyncIOTransport,
    ],
)
def test_bigtable_table_admin_transport_channel_mtls_with_adc(transport_class):
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


def test_bigtable_table_admin_grpc_lro_client():
    client = BigtableTableAdminClient(
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


def test_bigtable_table_admin_grpc_lro_async_client():
    client = BigtableTableAdminAsyncClient(
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


def test_backup_path():
    project = "squid"
    instance = "clam"
    cluster = "whelk"
    backup = "octopus"
    expected = "projects/{project}/instances/{instance}/clusters/{cluster}/backups/{backup}".format(
        project=project,
        instance=instance,
        cluster=cluster,
        backup=backup,
    )
    actual = BigtableTableAdminClient.backup_path(project, instance, cluster, backup)
    assert expected == actual


def test_parse_backup_path():
    expected = {
        "project": "oyster",
        "instance": "nudibranch",
        "cluster": "cuttlefish",
        "backup": "mussel",
    }
    path = BigtableTableAdminClient.backup_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_backup_path(path)
    assert expected == actual


def test_cluster_path():
    project = "winkle"
    instance = "nautilus"
    cluster = "scallop"
    expected = "projects/{project}/instances/{instance}/clusters/{cluster}".format(
        project=project,
        instance=instance,
        cluster=cluster,
    )
    actual = BigtableTableAdminClient.cluster_path(project, instance, cluster)
    assert expected == actual


def test_parse_cluster_path():
    expected = {
        "project": "abalone",
        "instance": "squid",
        "cluster": "clam",
    }
    path = BigtableTableAdminClient.cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_cluster_path(path)
    assert expected == actual


def test_crypto_key_version_path():
    project = "whelk"
    location = "octopus"
    key_ring = "oyster"
    crypto_key = "nudibranch"
    crypto_key_version = "cuttlefish"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
    )
    actual = BigtableTableAdminClient.crypto_key_version_path(
        project, location, key_ring, crypto_key, crypto_key_version
    )
    assert expected == actual


def test_parse_crypto_key_version_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "key_ring": "nautilus",
        "crypto_key": "scallop",
        "crypto_key_version": "abalone",
    }
    path = BigtableTableAdminClient.crypto_key_version_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_crypto_key_version_path(path)
    assert expected == actual


def test_instance_path():
    project = "squid"
    instance = "clam"
    expected = "projects/{project}/instances/{instance}".format(
        project=project,
        instance=instance,
    )
    actual = BigtableTableAdminClient.instance_path(project, instance)
    assert expected == actual


def test_parse_instance_path():
    expected = {
        "project": "whelk",
        "instance": "octopus",
    }
    path = BigtableTableAdminClient.instance_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_instance_path(path)
    assert expected == actual


def test_snapshot_path():
    project = "oyster"
    instance = "nudibranch"
    cluster = "cuttlefish"
    snapshot = "mussel"
    expected = "projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}".format(
        project=project,
        instance=instance,
        cluster=cluster,
        snapshot=snapshot,
    )
    actual = BigtableTableAdminClient.snapshot_path(
        project, instance, cluster, snapshot
    )
    assert expected == actual


def test_parse_snapshot_path():
    expected = {
        "project": "winkle",
        "instance": "nautilus",
        "cluster": "scallop",
        "snapshot": "abalone",
    }
    path = BigtableTableAdminClient.snapshot_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_snapshot_path(path)
    assert expected == actual


def test_table_path():
    project = "squid"
    instance = "clam"
    table = "whelk"
    expected = "projects/{project}/instances/{instance}/tables/{table}".format(
        project=project,
        instance=instance,
        table=table,
    )
    actual = BigtableTableAdminClient.table_path(project, instance, table)
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "octopus",
        "instance": "oyster",
        "table": "nudibranch",
    }
    path = BigtableTableAdminClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_table_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BigtableTableAdminClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = BigtableTableAdminClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = BigtableTableAdminClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = BigtableTableAdminClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = BigtableTableAdminClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = BigtableTableAdminClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = BigtableTableAdminClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = BigtableTableAdminClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = BigtableTableAdminClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = BigtableTableAdminClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BigtableTableAdminClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BigtableTableAdminTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BigtableTableAdminClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BigtableTableAdminTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BigtableTableAdminClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = BigtableTableAdminAsyncClient(
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
        client = BigtableTableAdminClient(
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
        client = BigtableTableAdminClient(
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
        (BigtableTableAdminClient, transports.BigtableTableAdminGrpcTransport),
        (
            BigtableTableAdminAsyncClient,
            transports.BigtableTableAdminGrpcAsyncIOTransport,
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
            )
