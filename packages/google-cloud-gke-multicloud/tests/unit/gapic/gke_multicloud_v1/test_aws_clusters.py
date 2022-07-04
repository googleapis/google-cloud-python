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
    from unittest.mock import AsyncMock
except ImportError:
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
from google.cloud.gke_multicloud_v1.services.aws_clusters import AwsClustersAsyncClient
from google.cloud.gke_multicloud_v1.services.aws_clusters import AwsClustersClient
from google.cloud.gke_multicloud_v1.services.aws_clusters import pagers
from google.cloud.gke_multicloud_v1.services.aws_clusters import transports
from google.cloud.gke_multicloud_v1.types import aws_resources
from google.cloud.gke_multicloud_v1.types import aws_service
from google.cloud.gke_multicloud_v1.types import common_resources
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert AwsClustersClient._get_default_mtls_endpoint(None) is None
    assert (
        AwsClustersClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        AwsClustersClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AwsClustersClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AwsClustersClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert AwsClustersClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (AwsClustersClient, "grpc"),
        (AwsClustersAsyncClient, "grpc_asyncio"),
    ],
)
def test_aws_clusters_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("gkemulticloud.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AwsClustersGrpcTransport, "grpc"),
        (transports.AwsClustersGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_aws_clusters_client_service_account_always_use_jwt(
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
        (AwsClustersClient, "grpc"),
        (AwsClustersAsyncClient, "grpc_asyncio"),
    ],
)
def test_aws_clusters_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("gkemulticloud.googleapis.com:443")


def test_aws_clusters_client_get_transport_class():
    transport = AwsClustersClient.get_transport_class()
    available_transports = [
        transports.AwsClustersGrpcTransport,
    ]
    assert transport in available_transports

    transport = AwsClustersClient.get_transport_class("grpc")
    assert transport == transports.AwsClustersGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc"),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AwsClustersClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AwsClustersClient)
)
@mock.patch.object(
    AwsClustersAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AwsClustersAsyncClient),
)
def test_aws_clusters_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AwsClustersClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AwsClustersClient, "get_transport_class") as gtc:
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
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc", "true"),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc", "false"),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AwsClustersClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AwsClustersClient)
)
@mock.patch.object(
    AwsClustersAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AwsClustersAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_aws_clusters_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [AwsClustersClient, AwsClustersAsyncClient])
@mock.patch.object(
    AwsClustersClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AwsClustersClient)
)
@mock.patch.object(
    AwsClustersAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AwsClustersAsyncClient),
)
def test_aws_clusters_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc"),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_aws_clusters_client_client_options_scopes(
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
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc", grpc_helpers),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_aws_clusters_client_client_options_credentials_file(
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


def test_aws_clusters_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.gke_multicloud_v1.services.aws_clusters.transports.AwsClustersGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AwsClustersClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
        (AwsClustersClient, transports.AwsClustersGrpcTransport, "grpc", grpc_helpers),
        (
            AwsClustersAsyncClient,
            transports.AwsClustersGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_aws_clusters_client_create_channel_credentials_file(
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
        aws_service.CreateAwsClusterRequest,
        dict,
    ],
)
def test_create_aws_cluster(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_aws_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        client.create_aws_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsClusterRequest()


@pytest.mark.asyncio
async def test_create_aws_cluster_async(
    transport: str = "grpc_asyncio", request_type=aws_service.CreateAwsClusterRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_aws_cluster_async_from_dict():
    await test_create_aws_cluster_async(request_type=dict)


def test_create_aws_cluster_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.CreateAwsClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_aws_cluster(request)

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
async def test_create_aws_cluster_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.CreateAwsClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_aws_cluster(request)

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


def test_create_aws_cluster_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_aws_cluster(
            parent="parent_value",
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            aws_cluster_id="aws_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].aws_cluster
        mock_val = aws_resources.AwsCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].aws_cluster_id
        mock_val = "aws_cluster_id_value"
        assert arg == mock_val


def test_create_aws_cluster_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_aws_cluster(
            aws_service.CreateAwsClusterRequest(),
            parent="parent_value",
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            aws_cluster_id="aws_cluster_id_value",
        )


@pytest.mark.asyncio
async def test_create_aws_cluster_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_aws_cluster(
            parent="parent_value",
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            aws_cluster_id="aws_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].aws_cluster
        mock_val = aws_resources.AwsCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].aws_cluster_id
        mock_val = "aws_cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_aws_cluster_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_aws_cluster(
            aws_service.CreateAwsClusterRequest(),
            parent="parent_value",
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            aws_cluster_id="aws_cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.UpdateAwsClusterRequest,
        dict,
    ],
)
def test_update_aws_cluster(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_aws_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        client.update_aws_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsClusterRequest()


@pytest.mark.asyncio
async def test_update_aws_cluster_async(
    transport: str = "grpc_asyncio", request_type=aws_service.UpdateAwsClusterRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_aws_cluster_async_from_dict():
    await test_update_aws_cluster_async(request_type=dict)


def test_update_aws_cluster_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.UpdateAwsClusterRequest()

    request.aws_cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_cluster.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_aws_cluster_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.UpdateAwsClusterRequest()

    request.aws_cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_cluster.name=name_value",
    ) in kw["metadata"]


def test_update_aws_cluster_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_aws_cluster(
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].aws_cluster
        mock_val = aws_resources.AwsCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_aws_cluster_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_aws_cluster(
            aws_service.UpdateAwsClusterRequest(),
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_aws_cluster_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_aws_cluster(
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].aws_cluster
        mock_val = aws_resources.AwsCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_aws_cluster_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_aws_cluster(
            aws_service.UpdateAwsClusterRequest(),
            aws_cluster=aws_resources.AwsCluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.GetAwsClusterRequest,
        dict,
    ],
)
def test_get_aws_cluster(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsCluster(
            name="name_value",
            description="description_value",
            aws_region="aws_region_value",
            state=aws_resources.AwsCluster.State.PROVISIONING,
            endpoint="endpoint_value",
            uid="uid_value",
            reconciling=True,
            etag="etag_value",
            cluster_ca_certificate="cluster_ca_certificate_value",
        )
        response = client.get_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsCluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.aws_region == "aws_region_value"
    assert response.state == aws_resources.AwsCluster.State.PROVISIONING
    assert response.endpoint == "endpoint_value"
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"
    assert response.cluster_ca_certificate == "cluster_ca_certificate_value"


def test_get_aws_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        client.get_aws_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsClusterRequest()


@pytest.mark.asyncio
async def test_get_aws_cluster_async(
    transport: str = "grpc_asyncio", request_type=aws_service.GetAwsClusterRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsCluster(
                name="name_value",
                description="description_value",
                aws_region="aws_region_value",
                state=aws_resources.AwsCluster.State.PROVISIONING,
                endpoint="endpoint_value",
                uid="uid_value",
                reconciling=True,
                etag="etag_value",
                cluster_ca_certificate="cluster_ca_certificate_value",
            )
        )
        response = await client.get_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsCluster)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.aws_region == "aws_region_value"
    assert response.state == aws_resources.AwsCluster.State.PROVISIONING
    assert response.endpoint == "endpoint_value"
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"
    assert response.cluster_ca_certificate == "cluster_ca_certificate_value"


@pytest.mark.asyncio
async def test_get_aws_cluster_async_from_dict():
    await test_get_aws_cluster_async(request_type=dict)


def test_get_aws_cluster_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        call.return_value = aws_resources.AwsCluster()
        client.get_aws_cluster(request)

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
async def test_get_aws_cluster_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsCluster()
        )
        await client.get_aws_cluster(request)

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


def test_get_aws_cluster_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsCluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_aws_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_aws_cluster_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_aws_cluster(
            aws_service.GetAwsClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_aws_cluster_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_aws_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsCluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsCluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_aws_cluster(
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
async def test_get_aws_cluster_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_aws_cluster(
            aws_service.GetAwsClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.ListAwsClustersRequest,
        dict,
    ],
)
def test_list_aws_clusters(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsClustersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_aws_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAwsClustersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_aws_clusters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        client.list_aws_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsClustersRequest()


@pytest.mark.asyncio
async def test_list_aws_clusters_async(
    transport: str = "grpc_asyncio", request_type=aws_service.ListAwsClustersRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsClustersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_aws_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAwsClustersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_aws_clusters_async_from_dict():
    await test_list_aws_clusters_async(request_type=dict)


def test_list_aws_clusters_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.ListAwsClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        call.return_value = aws_service.ListAwsClustersResponse()
        client.list_aws_clusters(request)

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
async def test_list_aws_clusters_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.ListAwsClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsClustersResponse()
        )
        await client.list_aws_clusters(request)

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


def test_list_aws_clusters_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_aws_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_aws_clusters_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_aws_clusters(
            aws_service.ListAwsClustersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_aws_clusters_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_aws_clusters(
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
async def test_list_aws_clusters_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_aws_clusters(
            aws_service.ListAwsClustersRequest(),
            parent="parent_value",
        )


def test_list_aws_clusters_pager(transport_name: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[],
                next_page_token="def",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_aws_clusters(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, aws_resources.AwsCluster) for i in results)


def test_list_aws_clusters_pages(transport_name: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[],
                next_page_token="def",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_aws_clusters(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_aws_clusters_async_pager():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[],
                next_page_token="def",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_aws_clusters(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, aws_resources.AwsCluster) for i in responses)


@pytest.mark.asyncio
async def test_list_aws_clusters_async_pages():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[],
                next_page_token="def",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsClustersResponse(
                aws_clusters=[
                    aws_resources.AwsCluster(),
                    aws_resources.AwsCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_aws_clusters(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.DeleteAwsClusterRequest,
        dict,
    ],
)
def test_delete_aws_cluster(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_aws_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        client.delete_aws_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsClusterRequest()


@pytest.mark.asyncio
async def test_delete_aws_cluster_async(
    transport: str = "grpc_asyncio", request_type=aws_service.DeleteAwsClusterRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_aws_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_aws_cluster_async_from_dict():
    await test_delete_aws_cluster_async(request_type=dict)


def test_delete_aws_cluster_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.DeleteAwsClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_aws_cluster(request)

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
async def test_delete_aws_cluster_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.DeleteAwsClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_aws_cluster(request)

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


def test_delete_aws_cluster_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_aws_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_aws_cluster_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_aws_cluster(
            aws_service.DeleteAwsClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_aws_cluster_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_aws_cluster(
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
async def test_delete_aws_cluster_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_aws_cluster(
            aws_service.DeleteAwsClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.GenerateAwsAccessTokenRequest,
        dict,
    ],
)
def test_generate_aws_access_token(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_aws_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.GenerateAwsAccessTokenResponse(
            access_token="access_token_value",
        )
        response = client.generate_aws_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GenerateAwsAccessTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_service.GenerateAwsAccessTokenResponse)
    assert response.access_token == "access_token_value"


def test_generate_aws_access_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_aws_access_token), "__call__"
    ) as call:
        client.generate_aws_access_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GenerateAwsAccessTokenRequest()


@pytest.mark.asyncio
async def test_generate_aws_access_token_async(
    transport: str = "grpc_asyncio",
    request_type=aws_service.GenerateAwsAccessTokenRequest,
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_aws_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.GenerateAwsAccessTokenResponse(
                access_token="access_token_value",
            )
        )
        response = await client.generate_aws_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GenerateAwsAccessTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_service.GenerateAwsAccessTokenResponse)
    assert response.access_token == "access_token_value"


@pytest.mark.asyncio
async def test_generate_aws_access_token_async_from_dict():
    await test_generate_aws_access_token_async(request_type=dict)


def test_generate_aws_access_token_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GenerateAwsAccessTokenRequest()

    request.aws_cluster = "aws_cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_aws_access_token), "__call__"
    ) as call:
        call.return_value = aws_service.GenerateAwsAccessTokenResponse()
        client.generate_aws_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_cluster=aws_cluster_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_aws_access_token_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GenerateAwsAccessTokenRequest()

    request.aws_cluster = "aws_cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_aws_access_token), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.GenerateAwsAccessTokenResponse()
        )
        await client.generate_aws_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_cluster=aws_cluster_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.CreateAwsNodePoolRequest,
        dict,
    ],
)
def test_create_aws_node_pool(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_aws_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        client.create_aws_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsNodePoolRequest()


@pytest.mark.asyncio
async def test_create_aws_node_pool_async(
    transport: str = "grpc_asyncio", request_type=aws_service.CreateAwsNodePoolRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.CreateAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_aws_node_pool_async_from_dict():
    await test_create_aws_node_pool_async(request_type=dict)


def test_create_aws_node_pool_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.CreateAwsNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_aws_node_pool(request)

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
async def test_create_aws_node_pool_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.CreateAwsNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_aws_node_pool(request)

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


def test_create_aws_node_pool_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_aws_node_pool(
            parent="parent_value",
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            aws_node_pool_id="aws_node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].aws_node_pool
        mock_val = aws_resources.AwsNodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].aws_node_pool_id
        mock_val = "aws_node_pool_id_value"
        assert arg == mock_val


def test_create_aws_node_pool_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_aws_node_pool(
            aws_service.CreateAwsNodePoolRequest(),
            parent="parent_value",
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            aws_node_pool_id="aws_node_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_aws_node_pool_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_aws_node_pool(
            parent="parent_value",
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            aws_node_pool_id="aws_node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].aws_node_pool
        mock_val = aws_resources.AwsNodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].aws_node_pool_id
        mock_val = "aws_node_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_aws_node_pool_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_aws_node_pool(
            aws_service.CreateAwsNodePoolRequest(),
            parent="parent_value",
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            aws_node_pool_id="aws_node_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.UpdateAwsNodePoolRequest,
        dict,
    ],
)
def test_update_aws_node_pool(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_aws_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        client.update_aws_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsNodePoolRequest()


@pytest.mark.asyncio
async def test_update_aws_node_pool_async(
    transport: str = "grpc_asyncio", request_type=aws_service.UpdateAwsNodePoolRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.UpdateAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_aws_node_pool_async_from_dict():
    await test_update_aws_node_pool_async(request_type=dict)


def test_update_aws_node_pool_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.UpdateAwsNodePoolRequest()

    request.aws_node_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_node_pool.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_aws_node_pool_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.UpdateAwsNodePoolRequest()

    request.aws_node_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "aws_node_pool.name=name_value",
    ) in kw["metadata"]


def test_update_aws_node_pool_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_aws_node_pool(
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].aws_node_pool
        mock_val = aws_resources.AwsNodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_aws_node_pool_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_aws_node_pool(
            aws_service.UpdateAwsNodePoolRequest(),
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_aws_node_pool_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_aws_node_pool(
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].aws_node_pool
        mock_val = aws_resources.AwsNodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_aws_node_pool_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_aws_node_pool(
            aws_service.UpdateAwsNodePoolRequest(),
            aws_node_pool=aws_resources.AwsNodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.GetAwsNodePoolRequest,
        dict,
    ],
)
def test_get_aws_node_pool(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsNodePool(
            name="name_value",
            version="version_value",
            subnet_id="subnet_id_value",
            state=aws_resources.AwsNodePool.State.PROVISIONING,
            uid="uid_value",
            reconciling=True,
            etag="etag_value",
        )
        response = client.get_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsNodePool)
    assert response.name == "name_value"
    assert response.version == "version_value"
    assert response.subnet_id == "subnet_id_value"
    assert response.state == aws_resources.AwsNodePool.State.PROVISIONING
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"


def test_get_aws_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        client.get_aws_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsNodePoolRequest()


@pytest.mark.asyncio
async def test_get_aws_node_pool_async(
    transport: str = "grpc_asyncio", request_type=aws_service.GetAwsNodePoolRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsNodePool(
                name="name_value",
                version="version_value",
                subnet_id="subnet_id_value",
                state=aws_resources.AwsNodePool.State.PROVISIONING,
                uid="uid_value",
                reconciling=True,
                etag="etag_value",
            )
        )
        response = await client.get_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsNodePool)
    assert response.name == "name_value"
    assert response.version == "version_value"
    assert response.subnet_id == "subnet_id_value"
    assert response.state == aws_resources.AwsNodePool.State.PROVISIONING
    assert response.uid == "uid_value"
    assert response.reconciling is True
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_aws_node_pool_async_from_dict():
    await test_get_aws_node_pool_async(request_type=dict)


def test_get_aws_node_pool_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        call.return_value = aws_resources.AwsNodePool()
        client.get_aws_node_pool(request)

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
async def test_get_aws_node_pool_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsNodePool()
        )
        await client.get_aws_node_pool(request)

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


def test_get_aws_node_pool_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsNodePool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_aws_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_aws_node_pool_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_aws_node_pool(
            aws_service.GetAwsNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_aws_node_pool_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsNodePool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsNodePool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_aws_node_pool(
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
async def test_get_aws_node_pool_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_aws_node_pool(
            aws_service.GetAwsNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.ListAwsNodePoolsRequest,
        dict,
    ],
)
def test_list_aws_node_pools(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsNodePoolsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_aws_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsNodePoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAwsNodePoolsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_aws_node_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        client.list_aws_node_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsNodePoolsRequest()


@pytest.mark.asyncio
async def test_list_aws_node_pools_async(
    transport: str = "grpc_asyncio", request_type=aws_service.ListAwsNodePoolsRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsNodePoolsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_aws_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.ListAwsNodePoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAwsNodePoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_aws_node_pools_async_from_dict():
    await test_list_aws_node_pools_async(request_type=dict)


def test_list_aws_node_pools_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.ListAwsNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        call.return_value = aws_service.ListAwsNodePoolsResponse()
        client.list_aws_node_pools(request)

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
async def test_list_aws_node_pools_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.ListAwsNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsNodePoolsResponse()
        )
        await client.list_aws_node_pools(request)

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


def test_list_aws_node_pools_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsNodePoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_aws_node_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_aws_node_pools_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_aws_node_pools(
            aws_service.ListAwsNodePoolsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_aws_node_pools_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_service.ListAwsNodePoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_service.ListAwsNodePoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_aws_node_pools(
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
async def test_list_aws_node_pools_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_aws_node_pools(
            aws_service.ListAwsNodePoolsRequest(),
            parent="parent_value",
        )


def test_list_aws_node_pools_pager(transport_name: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[],
                next_page_token="def",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_aws_node_pools(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, aws_resources.AwsNodePool) for i in results)


def test_list_aws_node_pools_pages(transport_name: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[],
                next_page_token="def",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_aws_node_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_aws_node_pools_async_pager():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[],
                next_page_token="def",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_aws_node_pools(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, aws_resources.AwsNodePool) for i in responses)


@pytest.mark.asyncio
async def test_list_aws_node_pools_async_pages():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_aws_node_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="abc",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[],
                next_page_token="def",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                ],
                next_page_token="ghi",
            ),
            aws_service.ListAwsNodePoolsResponse(
                aws_node_pools=[
                    aws_resources.AwsNodePool(),
                    aws_resources.AwsNodePool(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_aws_node_pools(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.DeleteAwsNodePoolRequest,
        dict,
    ],
)
def test_delete_aws_node_pool(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_aws_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        client.delete_aws_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsNodePoolRequest()


@pytest.mark.asyncio
async def test_delete_aws_node_pool_async(
    transport: str = "grpc_asyncio", request_type=aws_service.DeleteAwsNodePoolRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_aws_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.DeleteAwsNodePoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_aws_node_pool_async_from_dict():
    await test_delete_aws_node_pool_async(request_type=dict)


def test_delete_aws_node_pool_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.DeleteAwsNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_aws_node_pool(request)

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
async def test_delete_aws_node_pool_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.DeleteAwsNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_aws_node_pool(request)

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


def test_delete_aws_node_pool_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_aws_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_aws_node_pool_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_aws_node_pool(
            aws_service.DeleteAwsNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_aws_node_pool_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_aws_node_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_aws_node_pool(
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
async def test_delete_aws_node_pool_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_aws_node_pool(
            aws_service.DeleteAwsNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        aws_service.GetAwsServerConfigRequest,
        dict,
    ],
)
def test_get_aws_server_config(request_type, transport: str = "grpc"):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsServerConfig(
            name="name_value",
            supported_aws_regions=["supported_aws_regions_value"],
        )
        response = client.get_aws_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsServerConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsServerConfig)
    assert response.name == "name_value"
    assert response.supported_aws_regions == ["supported_aws_regions_value"]


def test_get_aws_server_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        client.get_aws_server_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsServerConfigRequest()


@pytest.mark.asyncio
async def test_get_aws_server_config_async(
    transport: str = "grpc_asyncio", request_type=aws_service.GetAwsServerConfigRequest
):
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsServerConfig(
                name="name_value",
                supported_aws_regions=["supported_aws_regions_value"],
            )
        )
        response = await client.get_aws_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == aws_service.GetAwsServerConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, aws_resources.AwsServerConfig)
    assert response.name == "name_value"
    assert response.supported_aws_regions == ["supported_aws_regions_value"]


@pytest.mark.asyncio
async def test_get_aws_server_config_async_from_dict():
    await test_get_aws_server_config_async(request_type=dict)


def test_get_aws_server_config_field_headers():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        call.return_value = aws_resources.AwsServerConfig()
        client.get_aws_server_config(request)

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
async def test_get_aws_server_config_field_headers_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = aws_service.GetAwsServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsServerConfig()
        )
        await client.get_aws_server_config(request)

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


def test_get_aws_server_config_flattened():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsServerConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_aws_server_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_aws_server_config_flattened_error():
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_aws_server_config(
            aws_service.GetAwsServerConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_aws_server_config_flattened_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_aws_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = aws_resources.AwsServerConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            aws_resources.AwsServerConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_aws_server_config(
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
async def test_get_aws_server_config_flattened_error_async():
    client = AwsClustersAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_aws_server_config(
            aws_service.GetAwsServerConfigRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AwsClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AwsClustersClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AwsClustersClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AwsClustersClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AwsClustersClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AwsClustersClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AwsClustersGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AwsClustersGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AwsClustersGrpcTransport,
        transports.AwsClustersGrpcAsyncIOTransport,
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
    transport = AwsClustersClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AwsClustersGrpcTransport,
    )


def test_aws_clusters_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AwsClustersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_aws_clusters_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.gke_multicloud_v1.services.aws_clusters.transports.AwsClustersTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AwsClustersTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_aws_cluster",
        "update_aws_cluster",
        "get_aws_cluster",
        "list_aws_clusters",
        "delete_aws_cluster",
        "generate_aws_access_token",
        "create_aws_node_pool",
        "update_aws_node_pool",
        "get_aws_node_pool",
        "list_aws_node_pools",
        "delete_aws_node_pool",
        "get_aws_server_config",
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


def test_aws_clusters_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.gke_multicloud_v1.services.aws_clusters.transports.AwsClustersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AwsClustersTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_aws_clusters_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.gke_multicloud_v1.services.aws_clusters.transports.AwsClustersTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AwsClustersTransport()
        adc.assert_called_once()


def test_aws_clusters_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AwsClustersClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AwsClustersGrpcTransport,
        transports.AwsClustersGrpcAsyncIOTransport,
    ],
)
def test_aws_clusters_transport_auth_adc(transport_class):
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
        transports.AwsClustersGrpcTransport,
        transports.AwsClustersGrpcAsyncIOTransport,
        transports.AwsClustersRestTransport,
    ],
)
def test_aws_clusters_transport_auth_gdch_credentials(transport_class):
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
        (transports.AwsClustersGrpcTransport, grpc_helpers),
        (transports.AwsClustersGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_aws_clusters_transport_create_channel(transport_class, grpc_helpers):
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
    [transports.AwsClustersGrpcTransport, transports.AwsClustersGrpcAsyncIOTransport],
)
def test_aws_clusters_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_aws_clusters_host_no_port(transport_name):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gkemulticloud.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("gkemulticloud.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_aws_clusters_host_with_port(transport_name):
    client = AwsClustersClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="gkemulticloud.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("gkemulticloud.googleapis.com:8000")


def test_aws_clusters_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AwsClustersGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_aws_clusters_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AwsClustersGrpcAsyncIOTransport(
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
    [transports.AwsClustersGrpcTransport, transports.AwsClustersGrpcAsyncIOTransport],
)
def test_aws_clusters_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.AwsClustersGrpcTransport, transports.AwsClustersGrpcAsyncIOTransport],
)
def test_aws_clusters_transport_channel_mtls_with_adc(transport_class):
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


def test_aws_clusters_grpc_lro_client():
    client = AwsClustersClient(
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


def test_aws_clusters_grpc_lro_async_client():
    client = AwsClustersAsyncClient(
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


def test_aws_cluster_path():
    project = "squid"
    location = "clam"
    aws_cluster = "whelk"
    expected = (
        "projects/{project}/locations/{location}/awsClusters/{aws_cluster}".format(
            project=project,
            location=location,
            aws_cluster=aws_cluster,
        )
    )
    actual = AwsClustersClient.aws_cluster_path(project, location, aws_cluster)
    assert expected == actual


def test_parse_aws_cluster_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "aws_cluster": "nudibranch",
    }
    path = AwsClustersClient.aws_cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_aws_cluster_path(path)
    assert expected == actual


def test_aws_node_pool_path():
    project = "cuttlefish"
    location = "mussel"
    aws_cluster = "winkle"
    aws_node_pool = "nautilus"
    expected = "projects/{project}/locations/{location}/awsClusters/{aws_cluster}/awsNodePools/{aws_node_pool}".format(
        project=project,
        location=location,
        aws_cluster=aws_cluster,
        aws_node_pool=aws_node_pool,
    )
    actual = AwsClustersClient.aws_node_pool_path(
        project, location, aws_cluster, aws_node_pool
    )
    assert expected == actual


def test_parse_aws_node_pool_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "aws_cluster": "squid",
        "aws_node_pool": "clam",
    }
    path = AwsClustersClient.aws_node_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_aws_node_pool_path(path)
    assert expected == actual


def test_aws_server_config_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}/awsServerConfig".format(
        project=project,
        location=location,
    )
    actual = AwsClustersClient.aws_server_config_path(project, location)
    assert expected == actual


def test_parse_aws_server_config_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = AwsClustersClient.aws_server_config_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_aws_server_config_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AwsClustersClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = AwsClustersClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = AwsClustersClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = AwsClustersClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = AwsClustersClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = AwsClustersClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = AwsClustersClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = AwsClustersClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = AwsClustersClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = AwsClustersClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AwsClustersClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AwsClustersTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AwsClustersClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AwsClustersTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AwsClustersClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = AwsClustersAsyncClient(
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
        client = AwsClustersClient(
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
        client = AwsClustersClient(
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
        (AwsClustersClient, transports.AwsClustersGrpcTransport),
        (AwsClustersAsyncClient, transports.AwsClustersGrpcAsyncIOTransport),
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
