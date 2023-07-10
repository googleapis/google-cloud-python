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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.metastore_v1alpha.services.dataproc_metastore import (
    DataprocMetastoreAsyncClient,
    DataprocMetastoreClient,
    pagers,
    transports,
)
from google.cloud.metastore_v1alpha.types import metastore


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

    assert DataprocMetastoreClient._get_default_mtls_endpoint(None) is None
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataprocMetastoreClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DataprocMetastoreClient, "grpc"),
        (DataprocMetastoreAsyncClient, "grpc_asyncio"),
        (DataprocMetastoreClient, "rest"),
    ],
)
def test_dataproc_metastore_client_from_service_account_info(
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
            "metastore.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://metastore.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataprocMetastoreGrpcTransport, "grpc"),
        (transports.DataprocMetastoreGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.DataprocMetastoreRestTransport, "rest"),
    ],
)
def test_dataproc_metastore_client_service_account_always_use_jwt(
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
        (DataprocMetastoreClient, "grpc"),
        (DataprocMetastoreAsyncClient, "grpc_asyncio"),
        (DataprocMetastoreClient, "rest"),
    ],
)
def test_dataproc_metastore_client_from_service_account_file(
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
            "metastore.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://metastore.googleapis.com"
        )


def test_dataproc_metastore_client_get_transport_class():
    transport = DataprocMetastoreClient.get_transport_class()
    available_transports = [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreRestTransport,
    ]
    assert transport in available_transports

    transport = DataprocMetastoreClient.get_transport_class("grpc")
    assert transport == transports.DataprocMetastoreGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport, "grpc"),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DataprocMetastoreClient, transports.DataprocMetastoreRestTransport, "rest"),
    ],
)
@mock.patch.object(
    DataprocMetastoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreClient),
)
@mock.patch.object(
    DataprocMetastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreAsyncClient),
)
def test_dataproc_metastore_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataprocMetastoreClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataprocMetastoreClient, "get_transport_class") as gtc:
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
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            "true",
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            "false",
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreRestTransport,
            "rest",
            "true",
        ),
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataprocMetastoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreClient),
)
@mock.patch.object(
    DataprocMetastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_dataproc_metastore_client_mtls_env_auto(
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
    "client_class", [DataprocMetastoreClient, DataprocMetastoreAsyncClient]
)
@mock.patch.object(
    DataprocMetastoreClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreClient),
)
@mock.patch.object(
    DataprocMetastoreAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataprocMetastoreAsyncClient),
)
def test_dataproc_metastore_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport, "grpc"),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (DataprocMetastoreClient, transports.DataprocMetastoreRestTransport, "rest"),
    ],
)
def test_dataproc_metastore_client_client_options_scopes(
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
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            DataprocMetastoreClient,
            transports.DataprocMetastoreRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_dataproc_metastore_client_client_options_credentials_file(
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


def test_dataproc_metastore_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.metastore_v1alpha.services.dataproc_metastore.transports.DataprocMetastoreGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataprocMetastoreClient(
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
            DataprocMetastoreClient,
            transports.DataprocMetastoreGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_dataproc_metastore_client_create_channel_credentials_file(
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
            "metastore.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="metastore.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListServicesRequest,
        dict,
    ],
)
def test_list_services(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_services_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        client.list_services()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()


@pytest.mark.asyncio
async def test_list_services_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListServicesRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListServicesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_services_async_from_dict():
    await test_list_services_async(request_type=dict)


def test_list_services_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListServicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        call.return_value = metastore.ListServicesResponse()
        client.list_services(request)

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
async def test_list_services_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListServicesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse()
        )
        await client.list_services(request)

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


def test_list_services_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_services(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_services_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            metastore.ListServicesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_services_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListServicesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListServicesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_services(
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
async def test_list_services_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_services(
            metastore.ListServicesRequest(),
            parent="parent_value",
        )


def test_list_services_pager(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_services(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Service) for i in results)


def test_list_services_pages(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_services_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_services(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Service) for i in responses)


@pytest.mark.asyncio
async def test_list_services_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_services), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_services(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetServiceRequest,
        dict,
    ],
)
def test_get_service(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service(
            name="name_value",
            network="network_value",
            endpoint_uri="endpoint_uri_value",
            port=453,
            state=metastore.Service.State.CREATING,
            state_message="state_message_value",
            artifact_gcs_uri="artifact_gcs_uri_value",
            tier=metastore.Service.Tier.DEVELOPER,
            uid="uid_value",
            release_channel=metastore.Service.ReleaseChannel.CANARY,
            database_type=metastore.Service.DatabaseType.MYSQL,
        )
        response = client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Service)
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.port == 453
    assert response.state == metastore.Service.State.CREATING
    assert response.state_message == "state_message_value"
    assert response.artifact_gcs_uri == "artifact_gcs_uri_value"
    assert response.tier == metastore.Service.Tier.DEVELOPER
    assert response.uid == "uid_value"
    assert response.release_channel == metastore.Service.ReleaseChannel.CANARY
    assert response.database_type == metastore.Service.DatabaseType.MYSQL


def test_get_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        client.get_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()


@pytest.mark.asyncio
async def test_get_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Service(
                name="name_value",
                network="network_value",
                endpoint_uri="endpoint_uri_value",
                port=453,
                state=metastore.Service.State.CREATING,
                state_message="state_message_value",
                artifact_gcs_uri="artifact_gcs_uri_value",
                tier=metastore.Service.Tier.DEVELOPER,
                uid="uid_value",
                release_channel=metastore.Service.ReleaseChannel.CANARY,
                database_type=metastore.Service.DatabaseType.MYSQL,
            )
        )
        response = await client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Service)
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.port == 453
    assert response.state == metastore.Service.State.CREATING
    assert response.state_message == "state_message_value"
    assert response.artifact_gcs_uri == "artifact_gcs_uri_value"
    assert response.tier == metastore.Service.Tier.DEVELOPER
    assert response.uid == "uid_value"
    assert response.release_channel == metastore.Service.ReleaseChannel.CANARY
    assert response.database_type == metastore.Service.DatabaseType.MYSQL


@pytest.mark.asyncio
async def test_get_service_async_from_dict():
    await test_get_service_async(request_type=dict)


def test_get_service_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        call.return_value = metastore.Service()
        client.get_service(request)

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
async def test_get_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Service())
        await client.get_service(request)

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


def test_get_service_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_service_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(
            metastore.GetServiceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Service()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Service())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_service(
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
async def test_get_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_service(
            metastore.GetServiceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateServiceRequest,
        dict,
    ],
)
def test_create_service(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        client.create_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateServiceRequest()


@pytest.mark.asyncio
async def test_create_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_service_async_from_dict():
    await test_create_service_async(request_type=dict)


def test_create_service_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateServiceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_service(request)

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
async def test_create_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateServiceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_service(request)

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


def test_create_service_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service(
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].service
        mock_val = metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert arg == mock_val
        arg = args[0].service_id
        mock_val = "service_id_value"
        assert arg == mock_val


def test_create_service_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            metastore.CreateServiceRequest(),
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )


@pytest.mark.asyncio
async def test_create_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_service(
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].service
        mock_val = metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert arg == mock_val
        arg = args[0].service_id
        mock_val = "service_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_service(
            metastore.CreateServiceRequest(),
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateServiceRequest,
        dict,
    ],
)
def test_update_service(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        client.update_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()


@pytest.mark.asyncio
async def test_update_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_service_async_from_dict():
    await test_update_service_async(request_type=dict)


def test_update_service_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateServiceRequest()

    request.service.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateServiceRequest()

    request.service.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service.name=name_value",
    ) in kw["metadata"]


def test_update_service_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_service(
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].service
        mock_val = metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_service_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service(
            metastore.UpdateServiceRequest(),
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_service(
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].service
        mock_val = metastore.Service(
            hive_metastore_config=metastore.HiveMetastoreConfig(version="version_value")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_service(
            metastore.UpdateServiceRequest(),
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteServiceRequest,
        dict,
    ],
)
def test_delete_service(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        client.delete_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteServiceRequest()


@pytest.mark.asyncio
async def test_delete_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_service_async_from_dict():
    await test_delete_service_async(request_type=dict)


def test_delete_service_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_service(request)

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
async def test_delete_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteServiceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_service(request)

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


def test_delete_service_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_service_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            metastore.DeleteServiceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_service(
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
async def test_delete_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_service(
            metastore.DeleteServiceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListMetadataImportsRequest,
        dict,
    ],
)
def test_list_metadata_imports(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMetadataImportsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_metadata_imports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        client.list_metadata_imports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()


@pytest.mark.asyncio
async def test_list_metadata_imports_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListMetadataImportsRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_metadata_imports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListMetadataImportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMetadataImportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_metadata_imports_async_from_dict():
    await test_list_metadata_imports_async(request_type=dict)


def test_list_metadata_imports_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListMetadataImportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        call.return_value = metastore.ListMetadataImportsResponse()
        client.list_metadata_imports(request)

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
async def test_list_metadata_imports_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListMetadataImportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse()
        )
        await client.list_metadata_imports(request)

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


def test_list_metadata_imports_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_metadata_imports(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_metadata_imports_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_metadata_imports(
            metastore.ListMetadataImportsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_metadata_imports_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListMetadataImportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListMetadataImportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_metadata_imports(
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
async def test_list_metadata_imports_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_metadata_imports(
            metastore.ListMetadataImportsRequest(),
            parent="parent_value",
        )


def test_list_metadata_imports_pager(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[],
                next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_metadata_imports(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.MetadataImport) for i in results)


def test_list_metadata_imports_pages(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[],
                next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_metadata_imports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_metadata_imports_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[],
                next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_metadata_imports(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.MetadataImport) for i in responses)


@pytest.mark.asyncio
async def test_list_metadata_imports_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_metadata_imports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[],
                next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_metadata_imports(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetMetadataImportRequest,
        dict,
    ],
)
def test_get_metadata_import(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport(
            name="name_value",
            description="description_value",
            state=metastore.MetadataImport.State.RUNNING,
        )
        response = client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.MetadataImport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.state == metastore.MetadataImport.State.RUNNING


def test_get_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        client.get_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()


@pytest.mark.asyncio
async def test_get_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport(
                name="name_value",
                description="description_value",
                state=metastore.MetadataImport.State.RUNNING,
            )
        )
        response = await client.get_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.MetadataImport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.state == metastore.MetadataImport.State.RUNNING


@pytest.mark.asyncio
async def test_get_metadata_import_async_from_dict():
    await test_get_metadata_import_async(request_type=dict)


def test_get_metadata_import_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetMetadataImportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        call.return_value = metastore.MetadataImport()
        client.get_metadata_import(request)

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
async def test_get_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetMetadataImportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport()
        )
        await client.get_metadata_import(request)

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


def test_get_metadata_import_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_metadata_import(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_metadata_import_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata_import(
            metastore.GetMetadataImportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.MetadataImport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.MetadataImport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_metadata_import(
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
async def test_get_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_metadata_import(
            metastore.GetMetadataImportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateMetadataImportRequest,
        dict,
    ],
)
def test_create_metadata_import(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        client.create_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()


@pytest.mark.asyncio
async def test_create_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_metadata_import_async_from_dict():
    await test_create_metadata_import_async(request_type=dict)


def test_create_metadata_import_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateMetadataImportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_metadata_import(request)

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
async def test_create_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateMetadataImportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_metadata_import(request)

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


def test_create_metadata_import_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_metadata_import(
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].metadata_import
        mock_val = metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert arg == mock_val
        arg = args[0].metadata_import_id
        mock_val = "metadata_import_id_value"
        assert arg == mock_val


def test_create_metadata_import_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_metadata_import(
            metastore.CreateMetadataImportRequest(),
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )


@pytest.mark.asyncio
async def test_create_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_metadata_import(
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].metadata_import
        mock_val = metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert arg == mock_val
        arg = args[0].metadata_import_id
        mock_val = "metadata_import_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_metadata_import(
            metastore.CreateMetadataImportRequest(),
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateMetadataImportRequest,
        dict,
    ],
)
def test_update_metadata_import(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_metadata_import_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        client.update_metadata_import()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()


@pytest.mark.asyncio
async def test_update_metadata_import_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateMetadataImportRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateMetadataImportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_metadata_import_async_from_dict():
    await test_update_metadata_import_async(request_type=dict)


def test_update_metadata_import_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateMetadataImportRequest()

    request.metadata_import.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "metadata_import.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_metadata_import_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateMetadataImportRequest()

    request.metadata_import.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_metadata_import(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "metadata_import.name=name_value",
    ) in kw["metadata"]


def test_update_metadata_import_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_metadata_import(
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].metadata_import
        mock_val = metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_metadata_import_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_metadata_import(
            metastore.UpdateMetadataImportRequest(),
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_metadata_import_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_metadata_import), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_metadata_import(
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].metadata_import
        mock_val = metastore.MetadataImport(
            database_dump=metastore.MetadataImport.DatabaseDump(
                database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_metadata_import_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_metadata_import(
            metastore.UpdateMetadataImportRequest(),
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ExportMetadataRequest,
        dict,
    ],
)
def test_export_metadata(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_metadata_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        client.export_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()


@pytest.mark.asyncio
async def test_export_metadata_async(
    transport: str = "grpc_asyncio", request_type=metastore.ExportMetadataRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ExportMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_metadata_async_from_dict():
    await test_export_metadata_async(request_type=dict)


def test_export_metadata_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ExportMetadataRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_metadata_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ExportMetadataRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_metadata), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RestoreServiceRequest,
        dict,
    ],
)
def test_restore_service(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restore_service_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        client.restore_service()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()


@pytest.mark.asyncio
async def test_restore_service_async(
    transport: str = "grpc_asyncio", request_type=metastore.RestoreServiceRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RestoreServiceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restore_service_async_from_dict():
    await test_restore_service_async(request_type=dict)


def test_restore_service_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RestoreServiceRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_restore_service_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RestoreServiceRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restore_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


def test_restore_service_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.restore_service(
            service="service_value",
            backup="backup_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].service
        mock_val = "service_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = "backup_value"
        assert arg == mock_val


def test_restore_service_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_service(
            metastore.RestoreServiceRequest(),
            service="service_value",
            backup="backup_value",
        )


@pytest.mark.asyncio
async def test_restore_service_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.restore_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.restore_service(
            service="service_value",
            backup="backup_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].service
        mock_val = "service_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = "backup_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_restore_service_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.restore_service(
            metastore.RestoreServiceRequest(),
            service="service_value",
            backup="backup_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListBackupsRequest,
        dict,
    ],
)
def test_list_backups(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_backups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        client.list_backups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()


@pytest.mark.asyncio
async def test_list_backups_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListBackupsRequest
):
    client = DataprocMetastoreAsyncClient(
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
            metastore.ListBackupsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_backups_async_from_dict():
    await test_list_backups_async(request_type=dict)


def test_list_backups_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListBackupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = metastore.ListBackupsResponse()
        client.list_backups(request)

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
async def test_list_backups_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListBackupsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListBackupsResponse()
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
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_backups_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse()
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            metastore.ListBackupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_backups_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListBackupsResponse()
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_backups(
            metastore.ListBackupsRequest(),
            parent="parent_value",
        )


def test_list_backups_pager(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                    metastore.Backup(),
                ],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
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

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Backup) for i in results)


def test_list_backups_pages(transport_name: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_backups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                    metastore.Backup(),
                ],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_backups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_backups_async_pager():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                    metastore.Backup(),
                ],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_backups(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Backup) for i in responses)


@pytest.mark.asyncio
async def test_list_backups_async_pages():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_backups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                    metastore.Backup(),
                ],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_backups(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetBackupRequest,
        dict,
    ],
)
def test_get_backup(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup(
            name="name_value",
            state=metastore.Backup.State.CREATING,
            description="description_value",
            restoring_services=["restoring_services_value"],
        )
        response = client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Backup)
    assert response.name == "name_value"
    assert response.state == metastore.Backup.State.CREATING
    assert response.description == "description_value"
    assert response.restoring_services == ["restoring_services_value"]


def test_get_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        client.get_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()


@pytest.mark.asyncio
async def test_get_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetBackupRequest
):
    client = DataprocMetastoreAsyncClient(
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
            metastore.Backup(
                name="name_value",
                state=metastore.Backup.State.CREATING,
                description="description_value",
                restoring_services=["restoring_services_value"],
            )
        )
        response = await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Backup)
    assert response.name == "name_value"
    assert response.state == metastore.Backup.State.CREATING
    assert response.description == "description_value"
    assert response.restoring_services == ["restoring_services_value"]


@pytest.mark.asyncio
async def test_get_backup_async_from_dict():
    await test_get_backup_async(request_type=dict)


def test_get_backup_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetBackupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = metastore.Backup()
        client.get_backup(request)

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
async def test_get_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetBackupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Backup())
        await client.get_backup(request)

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


def test_get_backup_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup()
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            metastore.GetBackupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Backup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Backup())
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_backup(
            metastore.GetBackupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateBackupRequest,
        dict,
    ],
)
def test_create_backup(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
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
        assert args[0] == metastore.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_backup), "__call__") as call:
        client.create_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateBackupRequest()


@pytest.mark.asyncio
async def test_create_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateBackupRequest
):
    client = DataprocMetastoreAsyncClient(
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
        assert args[0] == metastore.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_backup_async_from_dict():
    await test_create_backup_async(request_type=dict)


def test_create_backup_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateBackupRequest()

    request.parent = "parent_value"

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
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateBackupRequest()

    request.parent = "parent_value"

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
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_backup_flattened():
    client = DataprocMetastoreClient(
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
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = metastore.Backup(name="name_value")
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = "backup_id_value"
        assert arg == mock_val


def test_create_backup_flattened_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            metastore.CreateBackupRequest(),
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )


@pytest.mark.asyncio
async def test_create_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
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
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].backup
        mock_val = metastore.Backup(name="name_value")
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = "backup_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_backup_flattened_error_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_backup(
            metastore.CreateBackupRequest(),
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteBackupRequest,
        dict,
    ],
)
def test_delete_backup(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        client.delete_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()


@pytest.mark.asyncio
async def test_delete_backup_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteBackupRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_backup_async_from_dict():
    await test_delete_backup_async(request_type=dict)


def test_delete_backup_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteBackupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_backup(request)

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
async def test_delete_backup_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteBackupRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_backup(request)

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


def test_delete_backup_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            metastore.DeleteBackupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_backup_flattened_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_backup), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
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
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_backup(
            metastore.DeleteBackupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RemoveIamPolicyRequest,
        dict,
    ],
)
def test_remove_iam_policy(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.RemoveIamPolicyResponse(
            success=True,
        )
        response = client.remove_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RemoveIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.RemoveIamPolicyResponse)
    assert response.success is True


def test_remove_iam_policy_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_iam_policy), "__call__"
    ) as call:
        client.remove_iam_policy()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RemoveIamPolicyRequest()


@pytest.mark.asyncio
async def test_remove_iam_policy_async(
    transport: str = "grpc_asyncio", request_type=metastore.RemoveIamPolicyRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.RemoveIamPolicyResponse(
                success=True,
            )
        )
        response = await client.remove_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RemoveIamPolicyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.RemoveIamPolicyResponse)
    assert response.success is True


@pytest.mark.asyncio
async def test_remove_iam_policy_async_from_dict():
    await test_remove_iam_policy_async(request_type=dict)


def test_remove_iam_policy_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RemoveIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_iam_policy), "__call__"
    ) as call:
        call.return_value = metastore.RemoveIamPolicyResponse()
        client.remove_iam_policy(request)

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
async def test_remove_iam_policy_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RemoveIamPolicyRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.RemoveIamPolicyResponse()
        )
        await client.remove_iam_policy(request)

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


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.QueryMetadataRequest,
        dict,
    ],
)
def test_query_metadata(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.query_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.query_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.QueryMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_query_metadata_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.query_metadata), "__call__") as call:
        client.query_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.QueryMetadataRequest()


@pytest.mark.asyncio
async def test_query_metadata_async(
    transport: str = "grpc_asyncio", request_type=metastore.QueryMetadataRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.query_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.query_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.QueryMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_query_metadata_async_from_dict():
    await test_query_metadata_async(request_type=dict)


def test_query_metadata_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.QueryMetadataRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.query_metadata), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.query_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_query_metadata_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.QueryMetadataRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.query_metadata), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.query_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.MoveTableToDatabaseRequest,
        dict,
    ],
)
def test_move_table_to_database(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.move_table_to_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.move_table_to_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.MoveTableToDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_move_table_to_database_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.move_table_to_database), "__call__"
    ) as call:
        client.move_table_to_database()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.MoveTableToDatabaseRequest()


@pytest.mark.asyncio
async def test_move_table_to_database_async(
    transport: str = "grpc_asyncio", request_type=metastore.MoveTableToDatabaseRequest
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.move_table_to_database), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.move_table_to_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.MoveTableToDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_move_table_to_database_async_from_dict():
    await test_move_table_to_database_async(request_type=dict)


def test_move_table_to_database_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.MoveTableToDatabaseRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.move_table_to_database), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.move_table_to_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_move_table_to_database_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.MoveTableToDatabaseRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.move_table_to_database), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.move_table_to_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.AlterMetadataResourceLocationRequest,
        dict,
    ],
)
def test_alter_metadata_resource_location(request_type, transport: str = "grpc"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.alter_metadata_resource_location), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.alter_metadata_resource_location(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.AlterMetadataResourceLocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_alter_metadata_resource_location_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.alter_metadata_resource_location), "__call__"
    ) as call:
        client.alter_metadata_resource_location()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.AlterMetadataResourceLocationRequest()


@pytest.mark.asyncio
async def test_alter_metadata_resource_location_async(
    transport: str = "grpc_asyncio",
    request_type=metastore.AlterMetadataResourceLocationRequest,
):
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.alter_metadata_resource_location), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.alter_metadata_resource_location(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.AlterMetadataResourceLocationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_alter_metadata_resource_location_async_from_dict():
    await test_alter_metadata_resource_location_async(request_type=dict)


def test_alter_metadata_resource_location_field_headers():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.AlterMetadataResourceLocationRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.alter_metadata_resource_location), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.alter_metadata_resource_location(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_alter_metadata_resource_location_field_headers_async():
    client = DataprocMetastoreAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.AlterMetadataResourceLocationRequest()

    request.service = "service_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.alter_metadata_resource_location), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.alter_metadata_resource_location(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "service=service_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListServicesRequest,
        dict,
    ],
)
def test_list_services_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListServicesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListServicesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_services(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_services_rest_required_fields(request_type=metastore.ListServicesRequest):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).list_services._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_services._get_unset_required_fields(jsonified_request)
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

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListServicesResponse()
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

            pb_return_value = metastore.ListServicesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_services(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_services_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_services._get_unset_required_fields({})
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
def test_list_services_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_list_services"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_list_services"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListServicesRequest.pb(metastore.ListServicesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListServicesResponse.to_json(
            metastore.ListServicesResponse()
        )

        request = metastore.ListServicesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListServicesResponse()

        client.list_services(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_services_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListServicesRequest
):
    client = DataprocMetastoreClient(
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
        client.list_services(request)


def test_list_services_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListServicesResponse()

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
        pb_return_value = metastore.ListServicesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_services(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*}/services"
            % client.transport._host,
            args[1],
        )


def test_list_services_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            metastore.ListServicesRequest(),
            parent="parent_value",
        )


def test_list_services_rest_pager(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                    metastore.Service(),
                ],
                next_page_token="abc",
            ),
            metastore.ListServicesResponse(
                services=[],
                next_page_token="def",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListServicesResponse(
                services=[
                    metastore.Service(),
                    metastore.Service(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListServicesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_services(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Service) for i in results)

        pages = list(client.list_services(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetServiceRequest,
        dict,
    ],
)
def test_get_service_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/services/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Service(
            name="name_value",
            network="network_value",
            endpoint_uri="endpoint_uri_value",
            port=453,
            state=metastore.Service.State.CREATING,
            state_message="state_message_value",
            artifact_gcs_uri="artifact_gcs_uri_value",
            tier=metastore.Service.Tier.DEVELOPER,
            uid="uid_value",
            release_channel=metastore.Service.ReleaseChannel.CANARY,
            database_type=metastore.Service.DatabaseType.MYSQL,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Service.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_service(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Service)
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.endpoint_uri == "endpoint_uri_value"
    assert response.port == 453
    assert response.state == metastore.Service.State.CREATING
    assert response.state_message == "state_message_value"
    assert response.artifact_gcs_uri == "artifact_gcs_uri_value"
    assert response.tier == metastore.Service.Tier.DEVELOPER
    assert response.uid == "uid_value"
    assert response.release_channel == metastore.Service.ReleaseChannel.CANARY
    assert response.database_type == metastore.Service.DatabaseType.MYSQL


def test_get_service_rest_required_fields(request_type=metastore.GetServiceRequest):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).get_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Service()
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

            pb_return_value = metastore.Service.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_service_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_service._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_service_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_get_service"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_get_service"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetServiceRequest.pb(metastore.GetServiceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Service.to_json(metastore.Service())

        request = metastore.GetServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Service()

        client.get_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_service_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/services/sample3"}
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
        client.get_service(request)


def test_get_service_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Service()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/services/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Service.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/services/*}"
            % client.transport._host,
            args[1],
        )


def test_get_service_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(
            metastore.GetServiceRequest(),
            name="name_value",
        )


def test_get_service_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateServiceRequest,
        dict,
    ],
)
def test_create_service_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["service"] = {
        "hive_metastore_config": {
            "version": "version_value",
            "config_overrides": {},
            "kerberos_config": {
                "keytab": {"cloud_secret": "cloud_secret_value"},
                "principal": "principal_value",
                "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
            },
            "endpoint_protocol": 1,
            "auxiliary_versions": {},
        },
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "network": "network_value",
        "endpoint_uri": "endpoint_uri_value",
        "port": 453,
        "state": 1,
        "state_message": "state_message_value",
        "artifact_gcs_uri": "artifact_gcs_uri_value",
        "tier": 1,
        "metadata_integration": {
            "data_catalog_config": {"enabled": True},
            "dataplex_config": {"lake_resources": {}},
        },
        "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
        "uid": "uid_value",
        "metadata_management_activity": {
            "metadata_exports": [
                {
                    "destination_gcs_uri": "destination_gcs_uri_value",
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "database_dump_type": 1,
                }
            ],
            "restores": [
                {
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "backup": "backup_value",
                    "type_": 1,
                    "details": "details_value",
                }
            ],
        },
        "release_channel": 1,
        "encryption_config": {"kms_key": "kms_key_value"},
        "network_config": {
            "consumers": [
                {"subnetwork": "subnetwork_value", "endpoint_uri": "endpoint_uri_value"}
            ],
            "custom_routes_enabled": True,
        },
        "database_type": 1,
        "telemetry_config": {"log_format": 1},
        "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
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
        response = client.create_service(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_service_rest_required_fields(
    request_type=metastore.CreateServiceRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["service_id"] = ""
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
    assert "serviceId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "serviceId" in jsonified_request
    assert jsonified_request["serviceId"] == request_init["service_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["serviceId"] = "service_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_service._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "service_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "serviceId" in jsonified_request
    assert jsonified_request["serviceId"] == "service_id_value"

    client = DataprocMetastoreClient(
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

            response = client.create_service(request)

            expected_params = [
                (
                    "serviceId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_service_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_service._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "serviceId",
            )
        )
        & set(
            (
                "parent",
                "serviceId",
                "service",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_service_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_create_service"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_create_service"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateServiceRequest.pb(metastore.CreateServiceRequest())
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

        request = metastore.CreateServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_service_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["service"] = {
        "hive_metastore_config": {
            "version": "version_value",
            "config_overrides": {},
            "kerberos_config": {
                "keytab": {"cloud_secret": "cloud_secret_value"},
                "principal": "principal_value",
                "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
            },
            "endpoint_protocol": 1,
            "auxiliary_versions": {},
        },
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "network": "network_value",
        "endpoint_uri": "endpoint_uri_value",
        "port": 453,
        "state": 1,
        "state_message": "state_message_value",
        "artifact_gcs_uri": "artifact_gcs_uri_value",
        "tier": 1,
        "metadata_integration": {
            "data_catalog_config": {"enabled": True},
            "dataplex_config": {"lake_resources": {}},
        },
        "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
        "uid": "uid_value",
        "metadata_management_activity": {
            "metadata_exports": [
                {
                    "destination_gcs_uri": "destination_gcs_uri_value",
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "database_dump_type": 1,
                }
            ],
            "restores": [
                {
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "backup": "backup_value",
                    "type_": 1,
                    "details": "details_value",
                }
            ],
        },
        "release_channel": 1,
        "encryption_config": {"kms_key": "kms_key_value"},
        "network_config": {
            "consumers": [
                {"subnetwork": "subnetwork_value", "endpoint_uri": "endpoint_uri_value"}
            ],
            "custom_routes_enabled": True,
        },
        "database_type": 1,
        "telemetry_config": {"log_format": 1},
        "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
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
        client.create_service(request)


def test_create_service_rest_flattened():
    client = DataprocMetastoreClient(
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
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*}/services"
            % client.transport._host,
            args[1],
        )


def test_create_service_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            metastore.CreateServiceRequest(),
            parent="parent_value",
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            service_id="service_id_value",
        )


def test_create_service_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateServiceRequest,
        dict,
    ],
)
def test_update_service_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "service": {"name": "projects/sample1/locations/sample2/services/sample3"}
    }
    request_init["service"] = {
        "hive_metastore_config": {
            "version": "version_value",
            "config_overrides": {},
            "kerberos_config": {
                "keytab": {"cloud_secret": "cloud_secret_value"},
                "principal": "principal_value",
                "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
            },
            "endpoint_protocol": 1,
            "auxiliary_versions": {},
        },
        "name": "projects/sample1/locations/sample2/services/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "network": "network_value",
        "endpoint_uri": "endpoint_uri_value",
        "port": 453,
        "state": 1,
        "state_message": "state_message_value",
        "artifact_gcs_uri": "artifact_gcs_uri_value",
        "tier": 1,
        "metadata_integration": {
            "data_catalog_config": {"enabled": True},
            "dataplex_config": {"lake_resources": {}},
        },
        "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
        "uid": "uid_value",
        "metadata_management_activity": {
            "metadata_exports": [
                {
                    "destination_gcs_uri": "destination_gcs_uri_value",
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "database_dump_type": 1,
                }
            ],
            "restores": [
                {
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "backup": "backup_value",
                    "type_": 1,
                    "details": "details_value",
                }
            ],
        },
        "release_channel": 1,
        "encryption_config": {"kms_key": "kms_key_value"},
        "network_config": {
            "consumers": [
                {"subnetwork": "subnetwork_value", "endpoint_uri": "endpoint_uri_value"}
            ],
            "custom_routes_enabled": True,
        },
        "database_type": 1,
        "telemetry_config": {"log_format": 1},
        "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
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
        response = client.update_service(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_service_rest_required_fields(
    request_type=metastore.UpdateServiceRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).update_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_service._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DataprocMetastoreClient(
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

            response = client.update_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_service_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_service._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "updateMask",
            )
        )
        & set(
            (
                "updateMask",
                "service",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_service_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_update_service"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_update_service"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.UpdateServiceRequest.pb(metastore.UpdateServiceRequest())
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

        request = metastore.UpdateServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_service_rest_bad_request(
    transport: str = "rest", request_type=metastore.UpdateServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "service": {"name": "projects/sample1/locations/sample2/services/sample3"}
    }
    request_init["service"] = {
        "hive_metastore_config": {
            "version": "version_value",
            "config_overrides": {},
            "kerberos_config": {
                "keytab": {"cloud_secret": "cloud_secret_value"},
                "principal": "principal_value",
                "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
            },
            "endpoint_protocol": 1,
            "auxiliary_versions": {},
        },
        "name": "projects/sample1/locations/sample2/services/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "network": "network_value",
        "endpoint_uri": "endpoint_uri_value",
        "port": 453,
        "state": 1,
        "state_message": "state_message_value",
        "artifact_gcs_uri": "artifact_gcs_uri_value",
        "tier": 1,
        "metadata_integration": {
            "data_catalog_config": {"enabled": True},
            "dataplex_config": {"lake_resources": {}},
        },
        "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
        "uid": "uid_value",
        "metadata_management_activity": {
            "metadata_exports": [
                {
                    "destination_gcs_uri": "destination_gcs_uri_value",
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "database_dump_type": 1,
                }
            ],
            "restores": [
                {
                    "start_time": {},
                    "end_time": {},
                    "state": 1,
                    "backup": "backup_value",
                    "type_": 1,
                    "details": "details_value",
                }
            ],
        },
        "release_channel": 1,
        "encryption_config": {"kms_key": "kms_key_value"},
        "network_config": {
            "consumers": [
                {"subnetwork": "subnetwork_value", "endpoint_uri": "endpoint_uri_value"}
            ],
            "custom_routes_enabled": True,
        },
        "database_type": 1,
        "telemetry_config": {"log_format": 1},
        "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
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
        client.update_service(request)


def test_update_service_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "service": {"name": "projects/sample1/locations/sample2/services/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
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

        client.update_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{service.name=projects/*/locations/*/services/*}"
            % client.transport._host,
            args[1],
        )


def test_update_service_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service(
            metastore.UpdateServiceRequest(),
            service=metastore.Service(
                hive_metastore_config=metastore.HiveMetastoreConfig(
                    version="version_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_service_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteServiceRequest,
        dict,
    ],
)
def test_delete_service_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.delete_service(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_service_rest_required_fields(
    request_type=metastore.DeleteServiceRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).delete_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_service._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataprocMetastoreClient(
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

            response = client.delete_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_service_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_service._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_service_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_delete_service"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_delete_service"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.DeleteServiceRequest.pb(metastore.DeleteServiceRequest())
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

        request = metastore.DeleteServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_service_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/services/sample3"}
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
        client.delete_service(request)


def test_delete_service_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/services/sample3"}

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

        client.delete_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/services/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_service_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            metastore.DeleteServiceRequest(),
            name="name_value",
        )


def test_delete_service_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListMetadataImportsRequest,
        dict,
    ],
)
def test_list_metadata_imports_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListMetadataImportsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListMetadataImportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_metadata_imports(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMetadataImportsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_metadata_imports_rest_required_fields(
    request_type=metastore.ListMetadataImportsRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).list_metadata_imports._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_metadata_imports._get_unset_required_fields(jsonified_request)
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

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListMetadataImportsResponse()
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

            pb_return_value = metastore.ListMetadataImportsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_metadata_imports(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_metadata_imports_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_metadata_imports._get_unset_required_fields({})
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
def test_list_metadata_imports_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_list_metadata_imports"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_list_metadata_imports"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListMetadataImportsRequest.pb(
            metastore.ListMetadataImportsRequest()
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
        req.return_value._content = metastore.ListMetadataImportsResponse.to_json(
            metastore.ListMetadataImportsResponse()
        )

        request = metastore.ListMetadataImportsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListMetadataImportsResponse()

        client.list_metadata_imports(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_metadata_imports_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListMetadataImportsRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
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
        client.list_metadata_imports(request)


def test_list_metadata_imports_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListMetadataImportsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListMetadataImportsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_metadata_imports(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*/services/*}/metadataImports"
            % client.transport._host,
            args[1],
        )


def test_list_metadata_imports_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_metadata_imports(
            metastore.ListMetadataImportsRequest(),
            parent="parent_value",
        )


def test_list_metadata_imports_rest_pager(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
                next_page_token="abc",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[],
                next_page_token="def",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListMetadataImportsResponse(
                metadata_imports=[
                    metastore.MetadataImport(),
                    metastore.MetadataImport(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            metastore.ListMetadataImportsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        pager = client.list_metadata_imports(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.MetadataImport) for i in results)

        pages = list(client.list_metadata_imports(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetMetadataImportRequest,
        dict,
    ],
)
def test_get_metadata_import_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.MetadataImport(
            name="name_value",
            description="description_value",
            state=metastore.MetadataImport.State.RUNNING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.MetadataImport.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_metadata_import(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.MetadataImport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.state == metastore.MetadataImport.State.RUNNING


def test_get_metadata_import_rest_required_fields(
    request_type=metastore.GetMetadataImportRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).get_metadata_import._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_metadata_import._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.MetadataImport()
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

            pb_return_value = metastore.MetadataImport.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_metadata_import(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_metadata_import_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_metadata_import._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_metadata_import_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_get_metadata_import"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_get_metadata_import"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetMetadataImportRequest.pb(
            metastore.GetMetadataImportRequest()
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
        req.return_value._content = metastore.MetadataImport.to_json(
            metastore.MetadataImport()
        )

        request = metastore.GetMetadataImportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.MetadataImport()

        client.get_metadata_import(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_metadata_import_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
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
        client.get_metadata_import(request)


def test_get_metadata_import_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.MetadataImport()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.MetadataImport.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_metadata_import(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/services/*/metadataImports/*}"
            % client.transport._host,
            args[1],
        )


def test_get_metadata_import_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata_import(
            metastore.GetMetadataImportRequest(),
            name="name_value",
        )


def test_get_metadata_import_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateMetadataImportRequest,
        dict,
    ],
)
def test_create_metadata_import_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request_init["metadata_import"] = {
        "database_dump": {
            "database_type": 1,
            "gcs_uri": "gcs_uri_value",
            "source_database": "source_database_value",
            "type_": 1,
        },
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "end_time": {},
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
        response = client.create_metadata_import(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_metadata_import_rest_required_fields(
    request_type=metastore.CreateMetadataImportRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["metadata_import_id"] = ""
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
    assert "metadataImportId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_metadata_import._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "metadataImportId" in jsonified_request
    assert jsonified_request["metadataImportId"] == request_init["metadata_import_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["metadataImportId"] = "metadata_import_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_metadata_import._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "metadata_import_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "metadataImportId" in jsonified_request
    assert jsonified_request["metadataImportId"] == "metadata_import_id_value"

    client = DataprocMetastoreClient(
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

            response = client.create_metadata_import(request)

            expected_params = [
                (
                    "metadataImportId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_metadata_import_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_metadata_import._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "metadataImportId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "metadataImportId",
                "metadataImport",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_metadata_import_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_create_metadata_import"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_create_metadata_import"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateMetadataImportRequest.pb(
            metastore.CreateMetadataImportRequest()
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

        request = metastore.CreateMetadataImportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_metadata_import(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_metadata_import_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request_init["metadata_import"] = {
        "database_dump": {
            "database_type": 1,
            "gcs_uri": "gcs_uri_value",
            "source_database": "source_database_value",
            "type_": 1,
        },
        "name": "name_value",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "end_time": {},
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
        client.create_metadata_import(request)


def test_create_metadata_import_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_metadata_import(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*/services/*}/metadataImports"
            % client.transport._host,
            args[1],
        )


def test_create_metadata_import_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_metadata_import(
            metastore.CreateMetadataImportRequest(),
            parent="parent_value",
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            metadata_import_id="metadata_import_id_value",
        )


def test_create_metadata_import_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateMetadataImportRequest,
        dict,
    ],
)
def test_update_metadata_import_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "metadata_import": {
            "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
        }
    }
    request_init["metadata_import"] = {
        "database_dump": {
            "database_type": 1,
            "gcs_uri": "gcs_uri_value",
            "source_database": "source_database_value",
            "type_": 1,
        },
        "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "end_time": {},
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
        response = client.update_metadata_import(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_metadata_import_rest_required_fields(
    request_type=metastore.UpdateMetadataImportRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).update_metadata_import._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_metadata_import._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "update_mask",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = DataprocMetastoreClient(
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

            response = client.update_metadata_import(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_metadata_import_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_metadata_import._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "updateMask",
            )
        )
        & set(
            (
                "updateMask",
                "metadataImport",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_metadata_import_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_update_metadata_import"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_update_metadata_import"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.UpdateMetadataImportRequest.pb(
            metastore.UpdateMetadataImportRequest()
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

        request = metastore.UpdateMetadataImportRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_metadata_import(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_metadata_import_rest_bad_request(
    transport: str = "rest", request_type=metastore.UpdateMetadataImportRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "metadata_import": {
            "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
        }
    }
    request_init["metadata_import"] = {
        "database_dump": {
            "database_type": 1,
            "gcs_uri": "gcs_uri_value",
            "source_database": "source_database_value",
            "type_": 1,
        },
        "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4",
        "description": "description_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "end_time": {},
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
        client.update_metadata_import(request)


def test_update_metadata_import_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "metadata_import": {
                "name": "projects/sample1/locations/sample2/services/sample3/metadataImports/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
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

        client.update_metadata_import(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{metadata_import.name=projects/*/locations/*/services/*/metadataImports/*}"
            % client.transport._host,
            args[1],
        )


def test_update_metadata_import_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_metadata_import(
            metastore.UpdateMetadataImportRequest(),
            metadata_import=metastore.MetadataImport(
                database_dump=metastore.MetadataImport.DatabaseDump(
                    database_type=metastore.MetadataImport.DatabaseDump.DatabaseType.MYSQL
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_metadata_import_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ExportMetadataRequest,
        dict,
    ],
)
def test_export_metadata_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.export_metadata(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_export_metadata_rest_required_fields(
    request_type=metastore.ExportMetadataRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["service"] = ""
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
    ).export_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["service"] = "service_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).export_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "service" in jsonified_request
    assert jsonified_request["service"] == "service_value"

    client = DataprocMetastoreClient(
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

            response = client.export_metadata(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_export_metadata_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.export_metadata._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("service",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_export_metadata_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_export_metadata"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_export_metadata"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ExportMetadataRequest.pb(
            metastore.ExportMetadataRequest()
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

        request = metastore.ExportMetadataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.export_metadata(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_export_metadata_rest_bad_request(
    transport: str = "rest", request_type=metastore.ExportMetadataRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        client.export_metadata(request)


def test_export_metadata_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RestoreServiceRequest,
        dict,
    ],
)
def test_restore_service_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.restore_service(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_restore_service_rest_required_fields(
    request_type=metastore.RestoreServiceRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["service"] = ""
    request_init["backup"] = ""
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
    ).restore_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["service"] = "service_value"
    jsonified_request["backup"] = "backup_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).restore_service._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "service" in jsonified_request
    assert jsonified_request["service"] == "service_value"
    assert "backup" in jsonified_request
    assert jsonified_request["backup"] == "backup_value"

    client = DataprocMetastoreClient(
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

            response = client.restore_service(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_restore_service_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.restore_service._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "service",
                "backup",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_restore_service_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_restore_service"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_restore_service"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.RestoreServiceRequest.pb(
            metastore.RestoreServiceRequest()
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

        request = metastore.RestoreServiceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.restore_service(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_restore_service_rest_bad_request(
    transport: str = "rest", request_type=metastore.RestoreServiceRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        client.restore_service(request)


def test_restore_service_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "service": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            service="service_value",
            backup="backup_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.restore_service(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{service=projects/*/locations/*/services/*}:restore"
            % client.transport._host,
            args[1],
        )


def test_restore_service_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_service(
            metastore.RestoreServiceRequest(),
            service="service_value",
            backup="backup_value",
        )


def test_restore_service_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListBackupsRequest,
        dict,
    ],
)
def test_list_backups_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListBackupsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_backups(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_backups_rest_required_fields(request_type=metastore.ListBackupsRequest):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).list_backups._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_backups._get_unset_required_fields(jsonified_request)
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

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListBackupsResponse()
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

            pb_return_value = metastore.ListBackupsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_backups(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_backups_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_backups._get_unset_required_fields({})
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
def test_list_backups_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_list_backups"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_list_backups"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListBackupsRequest.pb(metastore.ListBackupsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListBackupsResponse.to_json(
            metastore.ListBackupsResponse()
        )

        request = metastore.ListBackupsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListBackupsResponse()

        client.list_backups(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_backups_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListBackupsRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
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
        client.list_backups(request)


def test_list_backups_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListBackupsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_backups(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*/services/*}/backups"
            % client.transport._host,
            args[1],
        )


def test_list_backups_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            metastore.ListBackupsRequest(),
            parent="parent_value",
        )


def test_list_backups_rest_pager(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                    metastore.Backup(),
                ],
                next_page_token="abc",
            ),
            metastore.ListBackupsResponse(
                backups=[],
                next_page_token="def",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListBackupsResponse(
                backups=[
                    metastore.Backup(),
                    metastore.Backup(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListBackupsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        pager = client.list_backups(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Backup) for i in results)

        pages = list(client.list_backups(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetBackupRequest,
        dict,
    ],
)
def test_get_backup_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Backup(
            name="name_value",
            state=metastore.Backup.State.CREATING,
            description="description_value",
            restoring_services=["restoring_services_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Backup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_backup(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Backup)
    assert response.name == "name_value"
    assert response.state == metastore.Backup.State.CREATING
    assert response.description == "description_value"
    assert response.restoring_services == ["restoring_services_value"]


def test_get_backup_rest_required_fields(request_type=metastore.GetBackupRequest):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).get_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Backup()
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

            pb_return_value = metastore.Backup.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_backup(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_backup_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_backup_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_get_backup"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_get_backup"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetBackupRequest.pb(metastore.GetBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Backup.to_json(metastore.Backup())

        request = metastore.GetBackupRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Backup()

        client.get_backup(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_backup_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetBackupRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
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
        client.get_backup(request)


def test_get_backup_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Backup()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Backup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/services/*/backups/*}"
            % client.transport._host,
            args[1],
        )


def test_get_backup_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            metastore.GetBackupRequest(),
            name="name_value",
        )


def test_get_backup_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateBackupRequest,
        dict,
    ],
)
def test_create_backup_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request_init["backup"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "end_time": {},
        "state": 1,
        "service_revision": {
            "hive_metastore_config": {
                "version": "version_value",
                "config_overrides": {},
                "kerberos_config": {
                    "keytab": {"cloud_secret": "cloud_secret_value"},
                    "principal": "principal_value",
                    "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
                },
                "endpoint_protocol": 1,
                "auxiliary_versions": {},
            },
            "name": "name_value",
            "create_time": {},
            "update_time": {},
            "labels": {},
            "network": "network_value",
            "endpoint_uri": "endpoint_uri_value",
            "port": 453,
            "state": 1,
            "state_message": "state_message_value",
            "artifact_gcs_uri": "artifact_gcs_uri_value",
            "tier": 1,
            "metadata_integration": {
                "data_catalog_config": {"enabled": True},
                "dataplex_config": {"lake_resources": {}},
            },
            "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
            "uid": "uid_value",
            "metadata_management_activity": {
                "metadata_exports": [
                    {
                        "destination_gcs_uri": "destination_gcs_uri_value",
                        "start_time": {},
                        "end_time": {},
                        "state": 1,
                        "database_dump_type": 1,
                    }
                ],
                "restores": [
                    {
                        "start_time": {},
                        "end_time": {},
                        "state": 1,
                        "backup": "backup_value",
                        "type_": 1,
                        "details": "details_value",
                    }
                ],
            },
            "release_channel": 1,
            "encryption_config": {"kms_key": "kms_key_value"},
            "network_config": {
                "consumers": [
                    {
                        "subnetwork": "subnetwork_value",
                        "endpoint_uri": "endpoint_uri_value",
                    }
                ],
                "custom_routes_enabled": True,
            },
            "database_type": 1,
            "telemetry_config": {"log_format": 1},
            "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
        },
        "description": "description_value",
        "restoring_services": [
            "restoring_services_value1",
            "restoring_services_value2",
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
        response = client.create_backup(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_backup_rest_required_fields(request_type=metastore.CreateBackupRequest):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["backup_id"] = ""
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
    assert "backupId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "backupId" in jsonified_request
    assert jsonified_request["backupId"] == request_init["backup_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["backupId"] = "backup_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_backup._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "backup_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "backupId" in jsonified_request
    assert jsonified_request["backupId"] == "backup_id_value"

    client = DataprocMetastoreClient(
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

            response = client.create_backup(request)

            expected_params = [
                (
                    "backupId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_backup_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_backup._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "backupId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "backupId",
                "backup",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_backup_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_create_backup"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_create_backup"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateBackupRequest.pb(metastore.CreateBackupRequest())
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

        request = metastore.CreateBackupRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_backup(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_backup_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateBackupRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request_init["backup"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "end_time": {},
        "state": 1,
        "service_revision": {
            "hive_metastore_config": {
                "version": "version_value",
                "config_overrides": {},
                "kerberos_config": {
                    "keytab": {"cloud_secret": "cloud_secret_value"},
                    "principal": "principal_value",
                    "krb5_config_gcs_uri": "krb5_config_gcs_uri_value",
                },
                "endpoint_protocol": 1,
                "auxiliary_versions": {},
            },
            "name": "name_value",
            "create_time": {},
            "update_time": {},
            "labels": {},
            "network": "network_value",
            "endpoint_uri": "endpoint_uri_value",
            "port": 453,
            "state": 1,
            "state_message": "state_message_value",
            "artifact_gcs_uri": "artifact_gcs_uri_value",
            "tier": 1,
            "metadata_integration": {
                "data_catalog_config": {"enabled": True},
                "dataplex_config": {"lake_resources": {}},
            },
            "maintenance_window": {"hour_of_day": {"value": 541}, "day_of_week": 1},
            "uid": "uid_value",
            "metadata_management_activity": {
                "metadata_exports": [
                    {
                        "destination_gcs_uri": "destination_gcs_uri_value",
                        "start_time": {},
                        "end_time": {},
                        "state": 1,
                        "database_dump_type": 1,
                    }
                ],
                "restores": [
                    {
                        "start_time": {},
                        "end_time": {},
                        "state": 1,
                        "backup": "backup_value",
                        "type_": 1,
                        "details": "details_value",
                    }
                ],
            },
            "release_channel": 1,
            "encryption_config": {"kms_key": "kms_key_value"},
            "network_config": {
                "consumers": [
                    {
                        "subnetwork": "subnetwork_value",
                        "endpoint_uri": "endpoint_uri_value",
                    }
                ],
                "custom_routes_enabled": True,
            },
            "database_type": 1,
            "telemetry_config": {"log_format": 1},
            "scaling_config": {"instance_size": 1, "scaling_factor": 0.1471},
        },
        "description": "description_value",
        "restoring_services": [
            "restoring_services_value1",
            "restoring_services_value2",
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
        client.create_backup(request)


def test_create_backup_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*/locations/*/services/*}/backups"
            % client.transport._host,
            args[1],
        )


def test_create_backup_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            metastore.CreateBackupRequest(),
            parent="parent_value",
            backup=metastore.Backup(name="name_value"),
            backup_id="backup_id_value",
        )


def test_create_backup_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteBackupRequest,
        dict,
    ],
)
def test_delete_backup_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
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
        response = client.delete_backup(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_backup_rest_required_fields(request_type=metastore.DeleteBackupRequest):
    transport_class = transports.DataprocMetastoreRestTransport

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
    ).delete_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_backup._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = DataprocMetastoreClient(
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

            response = client.delete_backup(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_backup_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_backup_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_delete_backup"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_delete_backup"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.DeleteBackupRequest.pb(metastore.DeleteBackupRequest())
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

        request = metastore.DeleteBackupRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_backup(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_backup_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteBackupRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
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
        client.delete_backup(request)


def test_delete_backup_rest_flattened():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/services/sample3/backups/sample4"
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

        client.delete_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/locations/*/services/*/backups/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_backup_rest_flattened_error(transport: str = "rest"):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            metastore.DeleteBackupRequest(),
            name="name_value",
        )


def test_delete_backup_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RemoveIamPolicyRequest,
        dict,
    ],
)
def test_remove_iam_policy_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/services/sample3/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.RemoveIamPolicyResponse(
            success=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.RemoveIamPolicyResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.RemoveIamPolicyResponse)
    assert response.success is True


def test_remove_iam_policy_rest_required_fields(
    request_type=metastore.RemoveIamPolicyRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["resource"] = ""
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
    ).remove_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).remove_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.RemoveIamPolicyResponse()
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

            pb_return_value = metastore.RemoveIamPolicyResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_iam_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_iam_policy_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.remove_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("resource",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_remove_iam_policy"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_remove_iam_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.RemoveIamPolicyRequest.pb(
            metastore.RemoveIamPolicyRequest()
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
        req.return_value._content = metastore.RemoveIamPolicyResponse.to_json(
            metastore.RemoveIamPolicyResponse()
        )

        request = metastore.RemoveIamPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.RemoveIamPolicyResponse()

        client.remove_iam_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_remove_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=metastore.RemoveIamPolicyRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/services/sample3/sample4"
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
        client.remove_iam_policy(request)


def test_remove_iam_policy_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.QueryMetadataRequest,
        dict,
    ],
)
def test_query_metadata_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.query_metadata(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_query_metadata_rest_required_fields(
    request_type=metastore.QueryMetadataRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["service"] = ""
    request_init["query"] = ""
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
    ).query_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["service"] = "service_value"
    jsonified_request["query"] = "query_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).query_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "service" in jsonified_request
    assert jsonified_request["service"] == "service_value"
    assert "query" in jsonified_request
    assert jsonified_request["query"] == "query_value"

    client = DataprocMetastoreClient(
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

            response = client.query_metadata(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_query_metadata_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.query_metadata._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "service",
                "query",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_query_metadata_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_query_metadata"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_query_metadata"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.QueryMetadataRequest.pb(metastore.QueryMetadataRequest())
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

        request = metastore.QueryMetadataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.query_metadata(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_query_metadata_rest_bad_request(
    transport: str = "rest", request_type=metastore.QueryMetadataRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        client.query_metadata(request)


def test_query_metadata_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.MoveTableToDatabaseRequest,
        dict,
    ],
)
def test_move_table_to_database_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.move_table_to_database(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_move_table_to_database_rest_required_fields(
    request_type=metastore.MoveTableToDatabaseRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["service"] = ""
    request_init["table_name"] = ""
    request_init["db_name"] = ""
    request_init["destination_db_name"] = ""
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
    ).move_table_to_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["service"] = "service_value"
    jsonified_request["tableName"] = "table_name_value"
    jsonified_request["dbName"] = "db_name_value"
    jsonified_request["destinationDbName"] = "destination_db_name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).move_table_to_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "service" in jsonified_request
    assert jsonified_request["service"] == "service_value"
    assert "tableName" in jsonified_request
    assert jsonified_request["tableName"] == "table_name_value"
    assert "dbName" in jsonified_request
    assert jsonified_request["dbName"] == "db_name_value"
    assert "destinationDbName" in jsonified_request
    assert jsonified_request["destinationDbName"] == "destination_db_name_value"

    client = DataprocMetastoreClient(
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

            response = client.move_table_to_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_move_table_to_database_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.move_table_to_database._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "service",
                "tableName",
                "dbName",
                "destinationDbName",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_move_table_to_database_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "post_move_table_to_database"
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor, "pre_move_table_to_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.MoveTableToDatabaseRequest.pb(
            metastore.MoveTableToDatabaseRequest()
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

        request = metastore.MoveTableToDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.move_table_to_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_move_table_to_database_rest_bad_request(
    transport: str = "rest", request_type=metastore.MoveTableToDatabaseRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        client.move_table_to_database(request)


def test_move_table_to_database_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.AlterMetadataResourceLocationRequest,
        dict,
    ],
)
def test_alter_metadata_resource_location_rest(request_type):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        response = client.alter_metadata_resource_location(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_alter_metadata_resource_location_rest_required_fields(
    request_type=metastore.AlterMetadataResourceLocationRequest,
):
    transport_class = transports.DataprocMetastoreRestTransport

    request_init = {}
    request_init["service"] = ""
    request_init["resource_name"] = ""
    request_init["location_uri"] = ""
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
    ).alter_metadata_resource_location._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["service"] = "service_value"
    jsonified_request["resourceName"] = "resource_name_value"
    jsonified_request["locationUri"] = "location_uri_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).alter_metadata_resource_location._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "service" in jsonified_request
    assert jsonified_request["service"] == "service_value"
    assert "resourceName" in jsonified_request
    assert jsonified_request["resourceName"] == "resource_name_value"
    assert "locationUri" in jsonified_request
    assert jsonified_request["locationUri"] == "location_uri_value"

    client = DataprocMetastoreClient(
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

            response = client.alter_metadata_resource_location(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_alter_metadata_resource_location_rest_unset_required_fields():
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.alter_metadata_resource_location._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "service",
                "resourceName",
                "locationUri",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_alter_metadata_resource_location_rest_interceptors(null_interceptor):
    transport = transports.DataprocMetastoreRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.DataprocMetastoreRestInterceptor(),
    )
    client = DataprocMetastoreClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.DataprocMetastoreRestInterceptor,
        "post_alter_metadata_resource_location",
    ) as post, mock.patch.object(
        transports.DataprocMetastoreRestInterceptor,
        "pre_alter_metadata_resource_location",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.AlterMetadataResourceLocationRequest.pb(
            metastore.AlterMetadataResourceLocationRequest()
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

        request = metastore.AlterMetadataResourceLocationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.alter_metadata_resource_location(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_alter_metadata_resource_location_rest_bad_request(
    transport: str = "rest", request_type=metastore.AlterMetadataResourceLocationRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"service": "projects/sample1/locations/sample2/services/sample3"}
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
        client.alter_metadata_resource_location(request)


def test_alter_metadata_resource_location_rest_error():
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataprocMetastoreClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataprocMetastoreClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataprocMetastoreGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataprocMetastoreGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
        transports.DataprocMetastoreRestTransport,
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
    transport = DataprocMetastoreClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DataprocMetastoreGrpcTransport,
    )


def test_dataproc_metastore_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataprocMetastoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_dataproc_metastore_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.metastore_v1alpha.services.dataproc_metastore.transports.DataprocMetastoreTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataprocMetastoreTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_services",
        "get_service",
        "create_service",
        "update_service",
        "delete_service",
        "list_metadata_imports",
        "get_metadata_import",
        "create_metadata_import",
        "update_metadata_import",
        "export_metadata",
        "restore_service",
        "list_backups",
        "get_backup",
        "create_backup",
        "delete_backup",
        "remove_iam_policy",
        "query_metadata",
        "move_table_to_database",
        "alter_metadata_resource_location",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
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


def test_dataproc_metastore_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.metastore_v1alpha.services.dataproc_metastore.transports.DataprocMetastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataprocMetastoreTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_dataproc_metastore_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.metastore_v1alpha.services.dataproc_metastore.transports.DataprocMetastoreTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataprocMetastoreTransport()
        adc.assert_called_once()


def test_dataproc_metastore_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataprocMetastoreClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_transport_auth_adc(transport_class):
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
        transports.DataprocMetastoreRestTransport,
    ],
)
def test_dataproc_metastore_transport_auth_gdch_credentials(transport_class):
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
        (transports.DataprocMetastoreGrpcTransport, grpc_helpers),
        (transports.DataprocMetastoreGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_dataproc_metastore_transport_create_channel(transport_class, grpc_helpers):
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
            "metastore.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="metastore.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_dataproc_metastore_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.DataprocMetastoreRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_dataproc_metastore_rest_lro_client():
    client = DataprocMetastoreClient(
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
def test_dataproc_metastore_host_no_port(transport_name):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="metastore.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "metastore.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://metastore.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_dataproc_metastore_host_with_port(transport_name):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="metastore.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "metastore.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://metastore.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_dataproc_metastore_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = DataprocMetastoreClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = DataprocMetastoreClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_services._session
    session2 = client2.transport.list_services._session
    assert session1 != session2
    session1 = client1.transport.get_service._session
    session2 = client2.transport.get_service._session
    assert session1 != session2
    session1 = client1.transport.create_service._session
    session2 = client2.transport.create_service._session
    assert session1 != session2
    session1 = client1.transport.update_service._session
    session2 = client2.transport.update_service._session
    assert session1 != session2
    session1 = client1.transport.delete_service._session
    session2 = client2.transport.delete_service._session
    assert session1 != session2
    session1 = client1.transport.list_metadata_imports._session
    session2 = client2.transport.list_metadata_imports._session
    assert session1 != session2
    session1 = client1.transport.get_metadata_import._session
    session2 = client2.transport.get_metadata_import._session
    assert session1 != session2
    session1 = client1.transport.create_metadata_import._session
    session2 = client2.transport.create_metadata_import._session
    assert session1 != session2
    session1 = client1.transport.update_metadata_import._session
    session2 = client2.transport.update_metadata_import._session
    assert session1 != session2
    session1 = client1.transport.export_metadata._session
    session2 = client2.transport.export_metadata._session
    assert session1 != session2
    session1 = client1.transport.restore_service._session
    session2 = client2.transport.restore_service._session
    assert session1 != session2
    session1 = client1.transport.list_backups._session
    session2 = client2.transport.list_backups._session
    assert session1 != session2
    session1 = client1.transport.get_backup._session
    session2 = client2.transport.get_backup._session
    assert session1 != session2
    session1 = client1.transport.create_backup._session
    session2 = client2.transport.create_backup._session
    assert session1 != session2
    session1 = client1.transport.delete_backup._session
    session2 = client2.transport.delete_backup._session
    assert session1 != session2
    session1 = client1.transport.remove_iam_policy._session
    session2 = client2.transport.remove_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.query_metadata._session
    session2 = client2.transport.query_metadata._session
    assert session1 != session2
    session1 = client1.transport.move_table_to_database._session
    session2 = client2.transport.move_table_to_database._session
    assert session1 != session2
    session1 = client1.transport.alter_metadata_resource_location._session
    session2 = client2.transport.alter_metadata_resource_location._session
    assert session1 != session2


def test_dataproc_metastore_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataprocMetastoreGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_dataproc_metastore_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataprocMetastoreGrpcAsyncIOTransport(
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_transport_channel_mtls_with_client_cert_source(
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
        transports.DataprocMetastoreGrpcTransport,
        transports.DataprocMetastoreGrpcAsyncIOTransport,
    ],
)
def test_dataproc_metastore_transport_channel_mtls_with_adc(transport_class):
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


def test_dataproc_metastore_grpc_lro_client():
    client = DataprocMetastoreClient(
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


def test_dataproc_metastore_grpc_lro_async_client():
    client = DataprocMetastoreAsyncClient(
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
    location = "clam"
    service = "whelk"
    backup = "octopus"
    expected = "projects/{project}/locations/{location}/services/{service}/backups/{backup}".format(
        project=project,
        location=location,
        service=service,
        backup=backup,
    )
    actual = DataprocMetastoreClient.backup_path(project, location, service, backup)
    assert expected == actual


def test_parse_backup_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "service": "cuttlefish",
        "backup": "mussel",
    }
    path = DataprocMetastoreClient.backup_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_backup_path(path)
    assert expected == actual


def test_lake_path():
    project = "winkle"
    location = "nautilus"
    lake = "scallop"
    expected = "projects/{project}/locations/{location}/lakes/{lake}".format(
        project=project,
        location=location,
        lake=lake,
    )
    actual = DataprocMetastoreClient.lake_path(project, location, lake)
    assert expected == actual


def test_parse_lake_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "lake": "clam",
    }
    path = DataprocMetastoreClient.lake_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_lake_path(path)
    assert expected == actual


def test_metadata_import_path():
    project = "whelk"
    location = "octopus"
    service = "oyster"
    metadata_import = "nudibranch"
    expected = "projects/{project}/locations/{location}/services/{service}/metadataImports/{metadata_import}".format(
        project=project,
        location=location,
        service=service,
        metadata_import=metadata_import,
    )
    actual = DataprocMetastoreClient.metadata_import_path(
        project, location, service, metadata_import
    )
    assert expected == actual


def test_parse_metadata_import_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "service": "winkle",
        "metadata_import": "nautilus",
    }
    path = DataprocMetastoreClient.metadata_import_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_metadata_import_path(path)
    assert expected == actual


def test_network_path():
    project = "scallop"
    network = "abalone"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project,
        network=network,
    )
    actual = DataprocMetastoreClient.network_path(project, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "squid",
        "network": "clam",
    }
    path = DataprocMetastoreClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_network_path(path)
    assert expected == actual


def test_service_path():
    project = "whelk"
    location = "octopus"
    service = "oyster"
    expected = "projects/{project}/locations/{location}/services/{service}".format(
        project=project,
        location=location,
        service=service,
    )
    actual = DataprocMetastoreClient.service_path(project, location, service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "service": "mussel",
    }
    path = DataprocMetastoreClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_service_path(path)
    assert expected == actual


def test_subnetwork_path():
    project = "winkle"
    region = "nautilus"
    subnetwork = "scallop"
    expected = "projects/{project}/regions/{region}/subnetworks/{subnetwork}".format(
        project=project,
        region=region,
        subnetwork=subnetwork,
    )
    actual = DataprocMetastoreClient.subnetwork_path(project, region, subnetwork)
    assert expected == actual


def test_parse_subnetwork_path():
    expected = {
        "project": "abalone",
        "region": "squid",
        "subnetwork": "clam",
    }
    path = DataprocMetastoreClient.subnetwork_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_subnetwork_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataprocMetastoreClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = DataprocMetastoreClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DataprocMetastoreClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = DataprocMetastoreClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DataprocMetastoreClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = DataprocMetastoreClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DataprocMetastoreClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = DataprocMetastoreClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DataprocMetastoreClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = DataprocMetastoreClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataprocMetastoreClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataprocMetastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataprocMetastoreClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataprocMetastoreTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataprocMetastoreClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/services/sample3"}, request
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/services/sample3"}
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/services/sample3"}, request
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/services/sample3"}
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/locations/sample2/services/sample3"}, request
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
    client = DataprocMetastoreClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/locations/sample2/services/sample3"}
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


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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


def test_set_iam_policy(transport: str = "grpc"):
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
    client = DataprocMetastoreClient(
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
    client = DataprocMetastoreAsyncClient(
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
        client = DataprocMetastoreClient(
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
        client = DataprocMetastoreClient(
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
        (DataprocMetastoreClient, transports.DataprocMetastoreGrpcTransport),
        (
            DataprocMetastoreAsyncClient,
            transports.DataprocMetastoreGrpcAsyncIOTransport,
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
