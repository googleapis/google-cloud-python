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
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.artifactregistry_v1.services.artifact_registry import (
    ArtifactRegistryAsyncClient,
    ArtifactRegistryClient,
    pagers,
    transports,
)
from google.cloud.artifactregistry_v1.types import apt_artifact, artifact, file, package
from google.cloud.artifactregistry_v1.types import vpcsc_config as gda_vpcsc_config
from google.cloud.artifactregistry_v1.types import repository
from google.cloud.artifactregistry_v1.types import repository as gda_repository
from google.cloud.artifactregistry_v1.types import service, settings
from google.cloud.artifactregistry_v1.types import tag
from google.cloud.artifactregistry_v1.types import tag as gda_tag
from google.cloud.artifactregistry_v1.types import version
from google.cloud.artifactregistry_v1.types import vpcsc_config
from google.cloud.artifactregistry_v1.types import yum_artifact


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

    assert ArtifactRegistryClient._get_default_mtls_endpoint(None) is None
    assert (
        ArtifactRegistryClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ArtifactRegistryClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ArtifactRegistryClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ArtifactRegistryClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ArtifactRegistryClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ArtifactRegistryClient, "grpc"),
        (ArtifactRegistryAsyncClient, "grpc_asyncio"),
        (ArtifactRegistryClient, "rest"),
    ],
)
def test_artifact_registry_client_from_service_account_info(
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
            "artifactregistry.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://artifactregistry.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ArtifactRegistryGrpcTransport, "grpc"),
        (transports.ArtifactRegistryGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.ArtifactRegistryRestTransport, "rest"),
    ],
)
def test_artifact_registry_client_service_account_always_use_jwt(
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
        (ArtifactRegistryClient, "grpc"),
        (ArtifactRegistryAsyncClient, "grpc_asyncio"),
        (ArtifactRegistryClient, "rest"),
    ],
)
def test_artifact_registry_client_from_service_account_file(
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
            "artifactregistry.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://artifactregistry.googleapis.com"
        )


def test_artifact_registry_client_get_transport_class():
    transport = ArtifactRegistryClient.get_transport_class()
    available_transports = [
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryRestTransport,
    ]
    assert transport in available_transports

    transport = ArtifactRegistryClient.get_transport_class("grpc")
    assert transport == transports.ArtifactRegistryGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ArtifactRegistryClient, transports.ArtifactRegistryGrpcTransport, "grpc"),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (ArtifactRegistryClient, transports.ArtifactRegistryRestTransport, "rest"),
    ],
)
@mock.patch.object(
    ArtifactRegistryClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryClient),
)
@mock.patch.object(
    ArtifactRegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryAsyncClient),
)
def test_artifact_registry_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ArtifactRegistryClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ArtifactRegistryClient, "get_transport_class") as gtc:
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
            ArtifactRegistryClient,
            transports.ArtifactRegistryGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ArtifactRegistryClient,
            transports.ArtifactRegistryGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            ArtifactRegistryClient,
            transports.ArtifactRegistryRestTransport,
            "rest",
            "true",
        ),
        (
            ArtifactRegistryClient,
            transports.ArtifactRegistryRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    ArtifactRegistryClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryClient),
)
@mock.patch.object(
    ArtifactRegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_artifact_registry_client_mtls_env_auto(
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
    "client_class", [ArtifactRegistryClient, ArtifactRegistryAsyncClient]
)
@mock.patch.object(
    ArtifactRegistryClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryClient),
)
@mock.patch.object(
    ArtifactRegistryAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ArtifactRegistryAsyncClient),
)
def test_artifact_registry_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (ArtifactRegistryClient, transports.ArtifactRegistryGrpcTransport, "grpc"),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (ArtifactRegistryClient, transports.ArtifactRegistryRestTransport, "rest"),
    ],
)
def test_artifact_registry_client_client_options_scopes(
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
            ArtifactRegistryClient,
            transports.ArtifactRegistryGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            ArtifactRegistryClient,
            transports.ArtifactRegistryRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_artifact_registry_client_client_options_credentials_file(
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


def test_artifact_registry_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.artifactregistry_v1.services.artifact_registry.transports.ArtifactRegistryGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ArtifactRegistryClient(
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
            ArtifactRegistryClient,
            transports.ArtifactRegistryGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ArtifactRegistryAsyncClient,
            transports.ArtifactRegistryGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_artifact_registry_client_create_channel_credentials_file(
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
            "artifactregistry.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=None,
            default_host="artifactregistry.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListDockerImagesRequest,
        dict,
    ],
)
def test_list_docker_images(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListDockerImagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_docker_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListDockerImagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDockerImagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_docker_images_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        client.list_docker_images()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListDockerImagesRequest()


@pytest.mark.asyncio
async def test_list_docker_images_async(
    transport: str = "grpc_asyncio", request_type=artifact.ListDockerImagesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListDockerImagesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_docker_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListDockerImagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDockerImagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_docker_images_async_from_dict():
    await test_list_docker_images_async(request_type=dict)


def test_list_docker_images_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListDockerImagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        call.return_value = artifact.ListDockerImagesResponse()
        client.list_docker_images(request)

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
async def test_list_docker_images_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListDockerImagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListDockerImagesResponse()
        )
        await client.list_docker_images(request)

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


def test_list_docker_images_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListDockerImagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_docker_images(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_docker_images_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_docker_images(
            artifact.ListDockerImagesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_docker_images_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListDockerImagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListDockerImagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_docker_images(
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
async def test_list_docker_images_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_docker_images(
            artifact.ListDockerImagesRequest(),
            parent="parent_value",
        )


def test_list_docker_images_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[],
                next_page_token="def",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_docker_images(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.DockerImage) for i in results)


def test_list_docker_images_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[],
                next_page_token="def",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_docker_images(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_docker_images_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[],
                next_page_token="def",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_docker_images(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, artifact.DockerImage) for i in responses)


@pytest.mark.asyncio
async def test_list_docker_images_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_docker_images),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[],
                next_page_token="def",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_docker_images(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetDockerImageRequest,
        dict,
    ],
)
def test_get_docker_image(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.DockerImage(
            name="name_value",
            uri="uri_value",
            tags=["tags_value"],
            image_size_bytes=1699,
            media_type="media_type_value",
        )
        response = client.get_docker_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetDockerImageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.DockerImage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.tags == ["tags_value"]
    assert response.image_size_bytes == 1699
    assert response.media_type == "media_type_value"


def test_get_docker_image_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        client.get_docker_image()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetDockerImageRequest()


@pytest.mark.asyncio
async def test_get_docker_image_async(
    transport: str = "grpc_asyncio", request_type=artifact.GetDockerImageRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.DockerImage(
                name="name_value",
                uri="uri_value",
                tags=["tags_value"],
                image_size_bytes=1699,
                media_type="media_type_value",
            )
        )
        response = await client.get_docker_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetDockerImageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.DockerImage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.tags == ["tags_value"]
    assert response.image_size_bytes == 1699
    assert response.media_type == "media_type_value"


@pytest.mark.asyncio
async def test_get_docker_image_async_from_dict():
    await test_get_docker_image_async(request_type=dict)


def test_get_docker_image_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetDockerImageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        call.return_value = artifact.DockerImage()
        client.get_docker_image(request)

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
async def test_get_docker_image_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetDockerImageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.DockerImage()
        )
        await client.get_docker_image(request)

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


def test_get_docker_image_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.DockerImage()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_docker_image(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_docker_image_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_docker_image(
            artifact.GetDockerImageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_docker_image_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_docker_image), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.DockerImage()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.DockerImage()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_docker_image(
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
async def test_get_docker_image_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_docker_image(
            artifact.GetDockerImageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListMavenArtifactsRequest,
        dict,
    ],
)
def test_list_maven_artifacts(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListMavenArtifactsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_maven_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListMavenArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMavenArtifactsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_maven_artifacts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        client.list_maven_artifacts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListMavenArtifactsRequest()


@pytest.mark.asyncio
async def test_list_maven_artifacts_async(
    transport: str = "grpc_asyncio", request_type=artifact.ListMavenArtifactsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListMavenArtifactsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_maven_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListMavenArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMavenArtifactsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_maven_artifacts_async_from_dict():
    await test_list_maven_artifacts_async(request_type=dict)


def test_list_maven_artifacts_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListMavenArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        call.return_value = artifact.ListMavenArtifactsResponse()
        client.list_maven_artifacts(request)

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
async def test_list_maven_artifacts_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListMavenArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListMavenArtifactsResponse()
        )
        await client.list_maven_artifacts(request)

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


def test_list_maven_artifacts_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListMavenArtifactsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_maven_artifacts(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_maven_artifacts_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_maven_artifacts(
            artifact.ListMavenArtifactsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_maven_artifacts_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListMavenArtifactsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListMavenArtifactsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_maven_artifacts(
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
async def test_list_maven_artifacts_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_maven_artifacts(
            artifact.ListMavenArtifactsRequest(),
            parent="parent_value",
        )


def test_list_maven_artifacts_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
                next_page_token="abc",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[],
                next_page_token="def",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_maven_artifacts(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.MavenArtifact) for i in results)


def test_list_maven_artifacts_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
                next_page_token="abc",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[],
                next_page_token="def",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_maven_artifacts(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_maven_artifacts_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
                next_page_token="abc",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[],
                next_page_token="def",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_maven_artifacts(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, artifact.MavenArtifact) for i in responses)


@pytest.mark.asyncio
async def test_list_maven_artifacts_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_maven_artifacts),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
                next_page_token="abc",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[],
                next_page_token="def",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_maven_artifacts(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetMavenArtifactRequest,
        dict,
    ],
)
def test_get_maven_artifact(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.MavenArtifact(
            name="name_value",
            pom_uri="pom_uri_value",
            group_id="group_id_value",
            artifact_id="artifact_id_value",
            version="version_value",
        )
        response = client.get_maven_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetMavenArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.MavenArtifact)
    assert response.name == "name_value"
    assert response.pom_uri == "pom_uri_value"
    assert response.group_id == "group_id_value"
    assert response.artifact_id == "artifact_id_value"
    assert response.version == "version_value"


def test_get_maven_artifact_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        client.get_maven_artifact()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetMavenArtifactRequest()


@pytest.mark.asyncio
async def test_get_maven_artifact_async(
    transport: str = "grpc_asyncio", request_type=artifact.GetMavenArtifactRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.MavenArtifact(
                name="name_value",
                pom_uri="pom_uri_value",
                group_id="group_id_value",
                artifact_id="artifact_id_value",
                version="version_value",
            )
        )
        response = await client.get_maven_artifact(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetMavenArtifactRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.MavenArtifact)
    assert response.name == "name_value"
    assert response.pom_uri == "pom_uri_value"
    assert response.group_id == "group_id_value"
    assert response.artifact_id == "artifact_id_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_get_maven_artifact_async_from_dict():
    await test_get_maven_artifact_async(request_type=dict)


def test_get_maven_artifact_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetMavenArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        call.return_value = artifact.MavenArtifact()
        client.get_maven_artifact(request)

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
async def test_get_maven_artifact_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetMavenArtifactRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.MavenArtifact()
        )
        await client.get_maven_artifact(request)

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


def test_get_maven_artifact_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.MavenArtifact()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_maven_artifact(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_maven_artifact_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_maven_artifact(
            artifact.GetMavenArtifactRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_maven_artifact_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_maven_artifact), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.MavenArtifact()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.MavenArtifact()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_maven_artifact(
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
async def test_get_maven_artifact_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_maven_artifact(
            artifact.GetMavenArtifactRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListNpmPackagesRequest,
        dict,
    ],
)
def test_list_npm_packages(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListNpmPackagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListNpmPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNpmPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_npm_packages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        client.list_npm_packages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListNpmPackagesRequest()


@pytest.mark.asyncio
async def test_list_npm_packages_async(
    transport: str = "grpc_asyncio", request_type=artifact.ListNpmPackagesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListNpmPackagesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_npm_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListNpmPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNpmPackagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_npm_packages_async_from_dict():
    await test_list_npm_packages_async(request_type=dict)


def test_list_npm_packages_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListNpmPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        call.return_value = artifact.ListNpmPackagesResponse()
        client.list_npm_packages(request)

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
async def test_list_npm_packages_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListNpmPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListNpmPackagesResponse()
        )
        await client.list_npm_packages(request)

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


def test_list_npm_packages_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListNpmPackagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_npm_packages(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_npm_packages_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_npm_packages(
            artifact.ListNpmPackagesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_npm_packages_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListNpmPackagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListNpmPackagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_npm_packages(
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
async def test_list_npm_packages_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_npm_packages(
            artifact.ListNpmPackagesRequest(),
            parent="parent_value",
        )


def test_list_npm_packages_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[],
                next_page_token="def",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_npm_packages(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.NpmPackage) for i in results)


def test_list_npm_packages_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[],
                next_page_token="def",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_npm_packages(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_npm_packages_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[],
                next_page_token="def",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_npm_packages(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, artifact.NpmPackage) for i in responses)


@pytest.mark.asyncio
async def test_list_npm_packages_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_npm_packages),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[],
                next_page_token="def",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_npm_packages(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetNpmPackageRequest,
        dict,
    ],
)
def test_get_npm_package(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.NpmPackage(
            name="name_value",
            package_name="package_name_value",
            version="version_value",
            tags=["tags_value"],
        )
        response = client.get_npm_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetNpmPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.NpmPackage)
    assert response.name == "name_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"
    assert response.tags == ["tags_value"]


def test_get_npm_package_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        client.get_npm_package()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetNpmPackageRequest()


@pytest.mark.asyncio
async def test_get_npm_package_async(
    transport: str = "grpc_asyncio", request_type=artifact.GetNpmPackageRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.NpmPackage(
                name="name_value",
                package_name="package_name_value",
                version="version_value",
                tags=["tags_value"],
            )
        )
        response = await client.get_npm_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetNpmPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.NpmPackage)
    assert response.name == "name_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"
    assert response.tags == ["tags_value"]


@pytest.mark.asyncio
async def test_get_npm_package_async_from_dict():
    await test_get_npm_package_async(request_type=dict)


def test_get_npm_package_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetNpmPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        call.return_value = artifact.NpmPackage()
        client.get_npm_package(request)

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
async def test_get_npm_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetNpmPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(artifact.NpmPackage())
        await client.get_npm_package(request)

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


def test_get_npm_package_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.NpmPackage()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_npm_package(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_npm_package_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_npm_package(
            artifact.GetNpmPackageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_npm_package_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_npm_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.NpmPackage()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(artifact.NpmPackage())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_npm_package(
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
async def test_get_npm_package_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_npm_package(
            artifact.GetNpmPackageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListPythonPackagesRequest,
        dict,
    ],
)
def test_list_python_packages(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListPythonPackagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_python_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListPythonPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPythonPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_python_packages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        client.list_python_packages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListPythonPackagesRequest()


@pytest.mark.asyncio
async def test_list_python_packages_async(
    transport: str = "grpc_asyncio", request_type=artifact.ListPythonPackagesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListPythonPackagesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_python_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.ListPythonPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPythonPackagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_python_packages_async_from_dict():
    await test_list_python_packages_async(request_type=dict)


def test_list_python_packages_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListPythonPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        call.return_value = artifact.ListPythonPackagesResponse()
        client.list_python_packages(request)

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
async def test_list_python_packages_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.ListPythonPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListPythonPackagesResponse()
        )
        await client.list_python_packages(request)

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


def test_list_python_packages_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListPythonPackagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_python_packages(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_python_packages_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_python_packages(
            artifact.ListPythonPackagesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_python_packages_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.ListPythonPackagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.ListPythonPackagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_python_packages(
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
async def test_list_python_packages_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_python_packages(
            artifact.ListPythonPackagesRequest(),
            parent="parent_value",
        )


def test_list_python_packages_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[],
                next_page_token="def",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_python_packages(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.PythonPackage) for i in results)


def test_list_python_packages_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[],
                next_page_token="def",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_python_packages(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_python_packages_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[],
                next_page_token="def",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_python_packages(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, artifact.PythonPackage) for i in responses)


@pytest.mark.asyncio
async def test_list_python_packages_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_python_packages),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[],
                next_page_token="def",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_python_packages(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetPythonPackageRequest,
        dict,
    ],
)
def test_get_python_package(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.PythonPackage(
            name="name_value",
            uri="uri_value",
            package_name="package_name_value",
            version="version_value",
        )
        response = client.get_python_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetPythonPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.PythonPackage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"


def test_get_python_package_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        client.get_python_package()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetPythonPackageRequest()


@pytest.mark.asyncio
async def test_get_python_package_async(
    transport: str = "grpc_asyncio", request_type=artifact.GetPythonPackageRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.PythonPackage(
                name="name_value",
                uri="uri_value",
                package_name="package_name_value",
                version="version_value",
            )
        )
        response = await client.get_python_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == artifact.GetPythonPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.PythonPackage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_get_python_package_async_from_dict():
    await test_get_python_package_async(request_type=dict)


def test_get_python_package_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetPythonPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        call.return_value = artifact.PythonPackage()
        client.get_python_package(request)

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
async def test_get_python_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = artifact.GetPythonPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.PythonPackage()
        )
        await client.get_python_package(request)

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


def test_get_python_package_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.PythonPackage()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_python_package(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_python_package_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_python_package(
            artifact.GetPythonPackageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_python_package_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_python_package), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = artifact.PythonPackage()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            artifact.PythonPackage()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_python_package(
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
async def test_get_python_package_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_python_package(
            artifact.GetPythonPackageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        apt_artifact.ImportAptArtifactsRequest,
        dict,
    ],
)
def test_import_apt_artifacts(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_apt_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_apt_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == apt_artifact.ImportAptArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_apt_artifacts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_apt_artifacts), "__call__"
    ) as call:
        client.import_apt_artifacts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == apt_artifact.ImportAptArtifactsRequest()


@pytest.mark.asyncio
async def test_import_apt_artifacts_async(
    transport: str = "grpc_asyncio", request_type=apt_artifact.ImportAptArtifactsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_apt_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_apt_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == apt_artifact.ImportAptArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_apt_artifacts_async_from_dict():
    await test_import_apt_artifacts_async(request_type=dict)


def test_import_apt_artifacts_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = apt_artifact.ImportAptArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_apt_artifacts), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_apt_artifacts(request)

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
async def test_import_apt_artifacts_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = apt_artifact.ImportAptArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_apt_artifacts), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_apt_artifacts(request)

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
        yum_artifact.ImportYumArtifactsRequest,
        dict,
    ],
)
def test_import_yum_artifacts(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_yum_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_yum_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == yum_artifact.ImportYumArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_yum_artifacts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_yum_artifacts), "__call__"
    ) as call:
        client.import_yum_artifacts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == yum_artifact.ImportYumArtifactsRequest()


@pytest.mark.asyncio
async def test_import_yum_artifacts_async(
    transport: str = "grpc_asyncio", request_type=yum_artifact.ImportYumArtifactsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_yum_artifacts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_yum_artifacts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == yum_artifact.ImportYumArtifactsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_yum_artifacts_async_from_dict():
    await test_import_yum_artifacts_async(request_type=dict)


def test_import_yum_artifacts_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = yum_artifact.ImportYumArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_yum_artifacts), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_yum_artifacts(request)

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
async def test_import_yum_artifacts_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = yum_artifact.ImportYumArtifactsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_yum_artifacts), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_yum_artifacts(request)

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
        repository.ListRepositoriesRequest,
        dict,
    ],
)
def test_list_repositories(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.ListRepositoriesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_repositories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.ListRepositoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_repositories_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        client.list_repositories()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.ListRepositoriesRequest()


@pytest.mark.asyncio
async def test_list_repositories_async(
    transport: str = "grpc_asyncio", request_type=repository.ListRepositoriesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.ListRepositoriesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_repositories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.ListRepositoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_repositories_async_from_dict():
    await test_list_repositories_async(request_type=dict)


def test_list_repositories_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.ListRepositoriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        call.return_value = repository.ListRepositoriesResponse()
        client.list_repositories(request)

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
async def test_list_repositories_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.ListRepositoriesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.ListRepositoriesResponse()
        )
        await client.list_repositories(request)

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


def test_list_repositories_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.ListRepositoriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_repositories(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_repositories_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_repositories(
            repository.ListRepositoriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_repositories_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.ListRepositoriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.ListRepositoriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_repositories(
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
async def test_list_repositories_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_repositories(
            repository.ListRepositoriesRequest(),
            parent="parent_value",
        )


def test_list_repositories_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                    repository.Repository(),
                ],
                next_page_token="abc",
            ),
            repository.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                ],
                next_page_token="ghi",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_repositories(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, repository.Repository) for i in results)


def test_list_repositories_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                    repository.Repository(),
                ],
                next_page_token="abc",
            ),
            repository.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                ],
                next_page_token="ghi",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_repositories(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_repositories_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                    repository.Repository(),
                ],
                next_page_token="abc",
            ),
            repository.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                ],
                next_page_token="ghi",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_repositories(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, repository.Repository) for i in responses)


@pytest.mark.asyncio
async def test_list_repositories_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_repositories),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                    repository.Repository(),
                ],
                next_page_token="abc",
            ),
            repository.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                ],
                next_page_token="ghi",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_repositories(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        repository.GetRepositoryRequest,
        dict,
    ],
)
def test_get_repository(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.Repository(
            name="name_value",
            format_=repository.Repository.Format.DOCKER,
            description="description_value",
            kms_key_name="kms_key_name_value",
        )
        response = client.get_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.GetRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_get_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        client.get_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.GetRepositoryRequest()


@pytest.mark.asyncio
async def test_get_repository_async(
    transport: str = "grpc_asyncio", request_type=repository.GetRepositoryRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.Repository(
                name="name_value",
                format_=repository.Repository.Format.DOCKER,
                description="description_value",
                kms_key_name="kms_key_name_value",
            )
        )
        response = await client.get_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.GetRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


@pytest.mark.asyncio
async def test_get_repository_async_from_dict():
    await test_get_repository_async(request_type=dict)


def test_get_repository_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.GetRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        call.return_value = repository.Repository()
        client.get_repository(request)

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
async def test_get_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.GetRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.Repository()
        )
        await client.get_repository(request)

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


def test_get_repository_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.Repository()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_repository(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_repository_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_repository(
            repository.GetRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_repository_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_repository), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = repository.Repository()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            repository.Repository()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_repository(
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
async def test_get_repository_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_repository(
            repository.GetRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_repository.CreateRepositoryRequest,
        dict,
    ],
)
def test_create_repository(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.CreateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        client.create_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.CreateRepositoryRequest()


@pytest.mark.asyncio
async def test_create_repository_async(
    transport: str = "grpc_asyncio", request_type=gda_repository.CreateRepositoryRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.CreateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_repository_async_from_dict():
    await test_create_repository_async(request_type=dict)


def test_create_repository_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.CreateRepositoryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_repository(request)

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
async def test_create_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.CreateRepositoryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_repository(request)

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


def test_create_repository_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_repository(
            parent="parent_value",
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].repository
        mock_val = gda_repository.Repository(
            maven_config=gda_repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            )
        )
        assert arg == mock_val
        arg = args[0].repository_id
        mock_val = "repository_id_value"
        assert arg == mock_val


def test_create_repository_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_repository(
            gda_repository.CreateRepositoryRequest(),
            parent="parent_value",
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )


@pytest.mark.asyncio
async def test_create_repository_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_repository(
            parent="parent_value",
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].repository
        mock_val = gda_repository.Repository(
            maven_config=gda_repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            )
        )
        assert arg == mock_val
        arg = args[0].repository_id
        mock_val = "repository_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_repository_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_repository(
            gda_repository.CreateRepositoryRequest(),
            parent="parent_value",
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_repository.UpdateRepositoryRequest,
        dict,
    ],
)
def test_update_repository(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_repository.Repository(
            name="name_value",
            format_=gda_repository.Repository.Format.DOCKER,
            description="description_value",
            kms_key_name="kms_key_name_value",
        )
        response = client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.UpdateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == gda_repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_update_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        client.update_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.UpdateRepositoryRequest()


@pytest.mark.asyncio
async def test_update_repository_async(
    transport: str = "grpc_asyncio", request_type=gda_repository.UpdateRepositoryRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_repository.Repository(
                name="name_value",
                format_=gda_repository.Repository.Format.DOCKER,
                description="description_value",
                kms_key_name="kms_key_name_value",
            )
        )
        response = await client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_repository.UpdateRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == gda_repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


@pytest.mark.asyncio
async def test_update_repository_async_from_dict():
    await test_update_repository_async(request_type=dict)


def test_update_repository_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.UpdateRepositoryRequest()

    request.repository.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        call.return_value = gda_repository.Repository()
        client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "repository.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.UpdateRepositoryRequest()

    request.repository.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_repository.Repository()
        )
        await client.update_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "repository.name=name_value",
    ) in kw["metadata"]


def test_update_repository_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_repository.Repository()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_repository(
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].repository
        mock_val = gda_repository.Repository(
            maven_config=gda_repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_repository_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_repository(
            gda_repository.UpdateRepositoryRequest(),
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_repository_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_repository.Repository()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_repository.Repository()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_repository(
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].repository
        mock_val = gda_repository.Repository(
            maven_config=gda_repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_repository_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_repository(
            gda_repository.UpdateRepositoryRequest(),
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        repository.DeleteRepositoryRequest,
        dict,
    ],
)
def test_delete_repository(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.DeleteRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_repository_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        client.delete_repository()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.DeleteRepositoryRequest()


@pytest.mark.asyncio
async def test_delete_repository_async(
    transport: str = "grpc_asyncio", request_type=repository.DeleteRepositoryRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_repository(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == repository.DeleteRepositoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_repository_async_from_dict():
    await test_delete_repository_async(request_type=dict)


def test_delete_repository_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.DeleteRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_repository(request)

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
async def test_delete_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.DeleteRepositoryRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_repository(request)

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


def test_delete_repository_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_repository(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_repository_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_repository(
            repository.DeleteRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_repository_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_repository), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_repository(
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
async def test_delete_repository_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_repository(
            repository.DeleteRepositoryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        package.ListPackagesRequest,
        dict,
    ],
)
def test_list_packages(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.ListPackagesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.ListPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_packages_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        client.list_packages()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.ListPackagesRequest()


@pytest.mark.asyncio
async def test_list_packages_async(
    transport: str = "grpc_asyncio", request_type=package.ListPackagesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            package.ListPackagesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_packages(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.ListPackagesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPackagesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_packages_async_from_dict():
    await test_list_packages_async(request_type=dict)


def test_list_packages_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.ListPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        call.return_value = package.ListPackagesResponse()
        client.list_packages(request)

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
async def test_list_packages_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.ListPackagesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            package.ListPackagesResponse()
        )
        await client.list_packages(request)

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


def test_list_packages_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.ListPackagesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_packages(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_packages_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_packages(
            package.ListPackagesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_packages_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.ListPackagesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            package.ListPackagesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_packages(
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
async def test_list_packages_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_packages(
            package.ListPackagesRequest(),
            parent="parent_value",
        )


def test_list_packages_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                    package.Package(),
                ],
                next_page_token="abc",
            ),
            package.ListPackagesResponse(
                packages=[],
                next_page_token="def",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                ],
                next_page_token="ghi",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_packages(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, package.Package) for i in results)


def test_list_packages_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_packages), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                    package.Package(),
                ],
                next_page_token="abc",
            ),
            package.ListPackagesResponse(
                packages=[],
                next_page_token="def",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                ],
                next_page_token="ghi",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_packages(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_packages_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_packages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                    package.Package(),
                ],
                next_page_token="abc",
            ),
            package.ListPackagesResponse(
                packages=[],
                next_page_token="def",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                ],
                next_page_token="ghi",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_packages(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, package.Package) for i in responses)


@pytest.mark.asyncio
async def test_list_packages_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_packages), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                    package.Package(),
                ],
                next_page_token="abc",
            ),
            package.ListPackagesResponse(
                packages=[],
                next_page_token="def",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                ],
                next_page_token="ghi",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_packages(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        package.GetPackageRequest,
        dict,
    ],
)
def test_get_package(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.Package(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.get_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.GetPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, package.Package)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_package_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        client.get_package()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.GetPackageRequest()


@pytest.mark.asyncio
async def test_get_package_async(
    transport: str = "grpc_asyncio", request_type=package.GetPackageRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            package.Package(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.GetPackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, package.Package)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_package_async_from_dict():
    await test_get_package_async(request_type=dict)


def test_get_package_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.GetPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        call.return_value = package.Package()
        client.get_package(request)

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
async def test_get_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.GetPackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(package.Package())
        await client.get_package(request)

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


def test_get_package_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.Package()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_package(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_package_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_package(
            package.GetPackageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_package_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = package.Package()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(package.Package())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_package(
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
async def test_get_package_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_package(
            package.GetPackageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        package.DeletePackageRequest,
        dict,
    ],
)
def test_delete_package(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.DeletePackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_package_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        client.delete_package()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.DeletePackageRequest()


@pytest.mark.asyncio
async def test_delete_package_async(
    transport: str = "grpc_asyncio", request_type=package.DeletePackageRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_package(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == package.DeletePackageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_package_async_from_dict():
    await test_delete_package_async(request_type=dict)


def test_delete_package_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.DeletePackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_package(request)

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
async def test_delete_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.DeletePackageRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_package(request)

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


def test_delete_package_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_package(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_package_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_package(
            package.DeletePackageRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_package_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_package), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_package(
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
async def test_delete_package_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_package(
            package.DeletePackageRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        version.ListVersionsRequest,
        dict,
    ],
)
def test_list_versions(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.ListVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.ListVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        client.list_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.ListVersionsRequest()


@pytest.mark.asyncio
async def test_list_versions_async(
    transport: str = "grpc_asyncio", request_type=version.ListVersionsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            version.ListVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.ListVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_versions_async_from_dict():
    await test_list_versions_async(request_type=dict)


def test_list_versions_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.ListVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        call.return_value = version.ListVersionsResponse()
        client.list_versions(request)

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
async def test_list_versions_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.ListVersionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            version.ListVersionsResponse()
        )
        await client.list_versions(request)

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


def test_list_versions_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.ListVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_versions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_versions_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_versions(
            version.ListVersionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_versions_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.ListVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            version.ListVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_versions(
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
async def test_list_versions_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_versions(
            version.ListVersionsRequest(),
            parent="parent_value",
        )


def test_list_versions_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                    version.Version(),
                ],
                next_page_token="abc",
            ),
            version.ListVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                ],
                next_page_token="ghi",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_versions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, version.Version) for i in results)


def test_list_versions_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                    version.Version(),
                ],
                next_page_token="abc",
            ),
            version.ListVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                ],
                next_page_token="ghi",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_versions_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                    version.Version(),
                ],
                next_page_token="abc",
            ),
            version.ListVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                ],
                next_page_token="ghi",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, version.Version) for i in responses)


@pytest.mark.asyncio
async def test_list_versions_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                    version.Version(),
                ],
                next_page_token="abc",
            ),
            version.ListVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                ],
                next_page_token="ghi",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        version.GetVersionRequest,
        dict,
    ],
)
def test_get_version(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.Version(
            name="name_value",
            description="description_value",
        )
        response = client.get_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.GetVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, version.Version)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        client.get_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.GetVersionRequest()


@pytest.mark.asyncio
async def test_get_version_async(
    transport: str = "grpc_asyncio", request_type=version.GetVersionRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            version.Version(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.get_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.GetVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, version.Version)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_version_async_from_dict():
    await test_get_version_async(request_type=dict)


def test_get_version_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.GetVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        call.return_value = version.Version()
        client.get_version(request)

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
async def test_get_version_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.GetVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(version.Version())
        await client.get_version(request)

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


def test_get_version_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.Version()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_version_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_version(
            version.GetVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_version_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = version.Version()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(version.Version())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_version(
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
async def test_get_version_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_version(
            version.GetVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        version.DeleteVersionRequest,
        dict,
    ],
)
def test_delete_version(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.DeleteVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        client.delete_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.DeleteVersionRequest()


@pytest.mark.asyncio
async def test_delete_version_async(
    transport: str = "grpc_asyncio", request_type=version.DeleteVersionRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == version.DeleteVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_version_async_from_dict():
    await test_delete_version_async(request_type=dict)


def test_delete_version_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.DeleteVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_version(request)

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
async def test_delete_version_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.DeleteVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_version(request)

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


def test_delete_version_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_version_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_version(
            version.DeleteVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_version_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_version), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_version(
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
async def test_delete_version_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_version(
            version.DeleteVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        file.ListFilesRequest,
        dict,
    ],
)
def test_list_files(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.ListFilesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_files(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.ListFilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFilesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_files_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        client.list_files()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.ListFilesRequest()


@pytest.mark.asyncio
async def test_list_files_async(
    transport: str = "grpc_asyncio", request_type=file.ListFilesRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            file.ListFilesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_files(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.ListFilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFilesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_files_async_from_dict():
    await test_list_files_async(request_type=dict)


def test_list_files_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.ListFilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        call.return_value = file.ListFilesResponse()
        client.list_files(request)

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
async def test_list_files_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.ListFilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            file.ListFilesResponse()
        )
        await client.list_files(request)

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


def test_list_files_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.ListFilesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_files(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_files_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_files(
            file.ListFilesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_files_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.ListFilesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            file.ListFilesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_files(
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
async def test_list_files_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_files(
            file.ListFilesRequest(),
            parent="parent_value",
        )


def test_list_files_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                    file.File(),
                ],
                next_page_token="abc",
            ),
            file.ListFilesResponse(
                files=[],
                next_page_token="def",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                ],
                next_page_token="ghi",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_files(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, file.File) for i in results)


def test_list_files_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_files), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                    file.File(),
                ],
                next_page_token="abc",
            ),
            file.ListFilesResponse(
                files=[],
                next_page_token="def",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                ],
                next_page_token="ghi",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_files(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_files_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_files), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                    file.File(),
                ],
                next_page_token="abc",
            ),
            file.ListFilesResponse(
                files=[],
                next_page_token="def",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                ],
                next_page_token="ghi",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_files(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, file.File) for i in responses)


@pytest.mark.asyncio
async def test_list_files_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_files), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                    file.File(),
                ],
                next_page_token="abc",
            ),
            file.ListFilesResponse(
                files=[],
                next_page_token="def",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                ],
                next_page_token="ghi",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_files(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        file.GetFileRequest,
        dict,
    ],
)
def test_get_file(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.File(
            name="name_value",
            size_bytes=1089,
            owner="owner_value",
        )
        response = client.get_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.GetFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, file.File)
    assert response.name == "name_value"
    assert response.size_bytes == 1089
    assert response.owner == "owner_value"


def test_get_file_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        client.get_file()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.GetFileRequest()


@pytest.mark.asyncio
async def test_get_file_async(
    transport: str = "grpc_asyncio", request_type=file.GetFileRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            file.File(
                name="name_value",
                size_bytes=1089,
                owner="owner_value",
            )
        )
        response = await client.get_file(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == file.GetFileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, file.File)
    assert response.name == "name_value"
    assert response.size_bytes == 1089
    assert response.owner == "owner_value"


@pytest.mark.asyncio
async def test_get_file_async_from_dict():
    await test_get_file_async(request_type=dict)


def test_get_file_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.GetFileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        call.return_value = file.File()
        client.get_file(request)

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
async def test_get_file_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.GetFileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(file.File())
        await client.get_file(request)

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


def test_get_file_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.File()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_file(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_file_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_file(
            file.GetFileRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_file_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_file), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = file.File()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(file.File())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_file(
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
async def test_get_file_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_file(
            file.GetFileRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tag.ListTagsRequest,
        dict,
    ],
)
def test_list_tags(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.ListTagsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.ListTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tags_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        client.list_tags()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.ListTagsRequest()


@pytest.mark.asyncio
async def test_list_tags_async(
    transport: str = "grpc_asyncio", request_type=tag.ListTagsRequest
):
    client = ArtifactRegistryAsyncClient(
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
            tag.ListTagsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tags(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.ListTagsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tags_async_from_dict():
    await test_list_tags_async(request_type=dict)


def test_list_tags_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.ListTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = tag.ListTagsResponse()
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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.ListTagsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tag.ListTagsResponse()
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
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.ListTagsResponse()
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
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tags(
            tag.ListTagsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tags_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.ListTagsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tag.ListTagsResponse()
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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tags(
            tag.ListTagsRequest(),
            parent="parent_value",
        )


def test_list_tags_pager(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                    tag.Tag(),
                ],
                next_page_token="abc",
            ),
            tag.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                ],
                next_page_token="ghi",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
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
        assert all(isinstance(i, tag.Tag) for i in results)


def test_list_tags_pages(transport_name: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tags), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                    tag.Tag(),
                ],
                next_page_token="abc",
            ),
            tag.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                ],
                next_page_token="ghi",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tags(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tags_async_pager():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                    tag.Tag(),
                ],
                next_page_token="abc",
            ),
            tag.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                ],
                next_page_token="ghi",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
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
        assert all(isinstance(i, tag.Tag) for i in responses)


@pytest.mark.asyncio
async def test_list_tags_async_pages():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tags), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                    tag.Tag(),
                ],
                next_page_token="abc",
            ),
            tag.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                ],
                next_page_token="ghi",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
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
        tag.GetTagRequest,
        dict,
    ],
)
def test_get_tag(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.Tag(
            name="name_value",
            version="version_value",
        )
        response = client.get_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.GetTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


def test_get_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        client.get_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.GetTagRequest()


@pytest.mark.asyncio
async def test_get_tag_async(
    transport: str = "grpc_asyncio", request_type=tag.GetTagRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tag.Tag(
                name="name_value",
                version="version_value",
            )
        )
        response = await client.get_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.GetTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_get_tag_async_from_dict():
    await test_get_tag_async(request_type=dict)


def test_get_tag_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.GetTagRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        call.return_value = tag.Tag()
        client.get_tag(request)

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
async def test_get_tag_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.GetTagRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tag.Tag())
        await client.get_tag(request)

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


def test_get_tag_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.Tag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tag(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tag_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tag(
            tag.GetTagRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tag_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tag.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tag.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tag(
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
async def test_get_tag_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tag(
            tag.GetTagRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_tag.CreateTagRequest,
        dict,
    ],
)
def test_create_tag(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag(
            name="name_value",
            version="version_value",
        )
        response = client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.CreateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


def test_create_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        client.create_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.CreateTagRequest()


@pytest.mark.asyncio
async def test_create_tag_async(
    transport: str = "grpc_asyncio", request_type=gda_tag.CreateTagRequest
):
    client = ArtifactRegistryAsyncClient(
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
            gda_tag.Tag(
                name="name_value",
                version="version_value",
            )
        )
        response = await client.create_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.CreateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_create_tag_async_from_dict():
    await test_create_tag_async(request_type=dict)


def test_create_tag_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.CreateTagRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = gda_tag.Tag()
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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.CreateTagRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gda_tag.Tag())
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
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_tag(
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag
        mock_val = gda_tag.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].tag_id
        mock_val = "tag_id_value"
        assert arg == mock_val


def test_create_tag_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag(
            gda_tag.CreateTagRequest(),
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )


@pytest.mark.asyncio
async def test_create_tag_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gda_tag.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_tag(
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].tag
        mock_val = gda_tag.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].tag_id
        mock_val = "tag_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_tag_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_tag(
            gda_tag.CreateTagRequest(),
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_tag.UpdateTagRequest,
        dict,
    ],
)
def test_update_tag(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag(
            name="name_value",
            version="version_value",
        )
        response = client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.UpdateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


def test_update_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        client.update_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.UpdateTagRequest()


@pytest.mark.asyncio
async def test_update_tag_async(
    transport: str = "grpc_asyncio", request_type=gda_tag.UpdateTagRequest
):
    client = ArtifactRegistryAsyncClient(
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
            gda_tag.Tag(
                name="name_value",
                version="version_value",
            )
        )
        response = await client.update_tag(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_tag.UpdateTagRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_update_tag_async_from_dict():
    await test_update_tag_async(request_type=dict)


def test_update_tag_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.UpdateTagRequest()

    request.tag.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = gda_tag.Tag()
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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.UpdateTagRequest()

    request.tag.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gda_tag.Tag())
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
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_tag(
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag
        mock_val = gda_tag.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_tag_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag(
            gda_tag.UpdateTagRequest(),
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_tag_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_tag), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_tag.Tag()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gda_tag.Tag())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_tag(
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].tag
        mock_val = gda_tag.Tag(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_tag_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_tag(
            gda_tag.UpdateTagRequest(),
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        tag.DeleteTagRequest,
        dict,
    ],
)
def test_delete_tag(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
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
        assert args[0] == tag.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_tag_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_tag), "__call__") as call:
        client.delete_tag()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == tag.DeleteTagRequest()


@pytest.mark.asyncio
async def test_delete_tag_async(
    transport: str = "grpc_asyncio", request_type=tag.DeleteTagRequest
):
    client = ArtifactRegistryAsyncClient(
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
        assert args[0] == tag.DeleteTagRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_tag_async_from_dict():
    await test_delete_tag_async(request_type=dict)


def test_delete_tag_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.DeleteTagRequest()

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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.DeleteTagRequest()

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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag(
            tag.DeleteTagRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_tag_flattened_async():
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_tag(
            tag.DeleteTagRequest(),
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
        settings.GetProjectSettingsRequest,
        dict,
    ],
)
def test_get_project_settings(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings(
            name="name_value",
            legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
        )
        response = client.get_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.GetProjectSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


def test_get_project_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        client.get_project_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.GetProjectSettingsRequest()


@pytest.mark.asyncio
async def test_get_project_settings_async(
    transport: str = "grpc_asyncio", request_type=settings.GetProjectSettingsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings(
                name="name_value",
                legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
            )
        )
        response = await client.get_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.GetProjectSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


@pytest.mark.asyncio
async def test_get_project_settings_async_from_dict():
    await test_get_project_settings_async(request_type=dict)


def test_get_project_settings_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.GetProjectSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        call.return_value = settings.ProjectSettings()
        client.get_project_settings(request)

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
async def test_get_project_settings_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.GetProjectSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings()
        )
        await client.get_project_settings(request)

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


def test_get_project_settings_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_project_settings(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_project_settings_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_project_settings(
            settings.GetProjectSettingsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_project_settings_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_project_settings(
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
async def test_get_project_settings_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_project_settings(
            settings.GetProjectSettingsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        settings.UpdateProjectSettingsRequest,
        dict,
    ],
)
def test_update_project_settings(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings(
            name="name_value",
            legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
        )
        response = client.update_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.UpdateProjectSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


def test_update_project_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        client.update_project_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.UpdateProjectSettingsRequest()


@pytest.mark.asyncio
async def test_update_project_settings_async(
    transport: str = "grpc_asyncio", request_type=settings.UpdateProjectSettingsRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings(
                name="name_value",
                legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
            )
        )
        response = await client.update_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == settings.UpdateProjectSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


@pytest.mark.asyncio
async def test_update_project_settings_async_from_dict():
    await test_update_project_settings_async(request_type=dict)


def test_update_project_settings_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.UpdateProjectSettingsRequest()

    request.project_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        call.return_value = settings.ProjectSettings()
        client.update_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_settings.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_project_settings_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.UpdateProjectSettingsRequest()

    request.project_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings()
        )
        await client.update_project_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_settings.name=name_value",
    ) in kw["metadata"]


def test_update_project_settings_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_project_settings(
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_settings
        mock_val = settings.ProjectSettings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_project_settings_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_project_settings(
            settings.UpdateProjectSettingsRequest(),
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_project_settings_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_project_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = settings.ProjectSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            settings.ProjectSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_project_settings(
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_settings
        mock_val = settings.ProjectSettings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_project_settings_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_project_settings(
            settings.UpdateProjectSettingsRequest(),
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vpcsc_config.GetVPCSCConfigRequest,
        dict,
    ],
)
def test_get_vpcsc_config(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vpcsc_config.VPCSCConfig(
            name="name_value",
            vpcsc_policy=vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
        )
        response = client.get_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vpcsc_config.GetVPCSCConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


def test_get_vpcsc_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        client.get_vpcsc_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vpcsc_config.GetVPCSCConfigRequest()


@pytest.mark.asyncio
async def test_get_vpcsc_config_async(
    transport: str = "grpc_asyncio", request_type=vpcsc_config.GetVPCSCConfigRequest
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vpcsc_config.VPCSCConfig(
                name="name_value",
                vpcsc_policy=vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
            )
        )
        response = await client.get_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vpcsc_config.GetVPCSCConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


@pytest.mark.asyncio
async def test_get_vpcsc_config_async_from_dict():
    await test_get_vpcsc_config_async(request_type=dict)


def test_get_vpcsc_config_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vpcsc_config.GetVPCSCConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        call.return_value = vpcsc_config.VPCSCConfig()
        client.get_vpcsc_config(request)

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
async def test_get_vpcsc_config_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vpcsc_config.GetVPCSCConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vpcsc_config.VPCSCConfig()
        )
        await client.get_vpcsc_config(request)

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


def test_get_vpcsc_config_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vpcsc_config.VPCSCConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vpcsc_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_vpcsc_config_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vpcsc_config(
            vpcsc_config.GetVPCSCConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vpcsc_config_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vpcsc_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vpcsc_config.VPCSCConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vpcsc_config.VPCSCConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vpcsc_config(
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
async def test_get_vpcsc_config_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vpcsc_config(
            vpcsc_config.GetVPCSCConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_vpcsc_config.UpdateVPCSCConfigRequest,
        dict,
    ],
)
def test_update_vpcsc_config(request_type, transport: str = "grpc"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_vpcsc_config.VPCSCConfig(
            name="name_value",
            vpcsc_policy=gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
        )
        response = client.update_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_vpcsc_config.UpdateVPCSCConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


def test_update_vpcsc_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        client.update_vpcsc_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_vpcsc_config.UpdateVPCSCConfigRequest()


@pytest.mark.asyncio
async def test_update_vpcsc_config_async(
    transport: str = "grpc_asyncio",
    request_type=gda_vpcsc_config.UpdateVPCSCConfigRequest,
):
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_vpcsc_config.VPCSCConfig(
                name="name_value",
                vpcsc_policy=gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
            )
        )
        response = await client.update_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gda_vpcsc_config.UpdateVPCSCConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


@pytest.mark.asyncio
async def test_update_vpcsc_config_async_from_dict():
    await test_update_vpcsc_config_async(request_type=dict)


def test_update_vpcsc_config_field_headers():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_vpcsc_config.UpdateVPCSCConfigRequest()

    request.vpcsc_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        call.return_value = gda_vpcsc_config.VPCSCConfig()
        client.update_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "vpcsc_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_vpcsc_config_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_vpcsc_config.UpdateVPCSCConfigRequest()

    request.vpcsc_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_vpcsc_config.VPCSCConfig()
        )
        await client.update_vpcsc_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "vpcsc_config.name=name_value",
    ) in kw["metadata"]


def test_update_vpcsc_config_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_vpcsc_config.VPCSCConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_vpcsc_config(
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].vpcsc_config
        mock_val = gda_vpcsc_config.VPCSCConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_vpcsc_config_flattened_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_vpcsc_config(
            gda_vpcsc_config.UpdateVPCSCConfigRequest(),
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_vpcsc_config_flattened_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_vpcsc_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gda_vpcsc_config.VPCSCConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gda_vpcsc_config.VPCSCConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_vpcsc_config(
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].vpcsc_config
        mock_val = gda_vpcsc_config.VPCSCConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_vpcsc_config_flattened_error_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_vpcsc_config(
            gda_vpcsc_config.UpdateVPCSCConfigRequest(),
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListDockerImagesRequest,
        dict,
    ],
)
def test_list_docker_images_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListDockerImagesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListDockerImagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_docker_images(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDockerImagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_docker_images_rest_required_fields(
    request_type=artifact.ListDockerImagesRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_docker_images._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_docker_images._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.ListDockerImagesResponse()
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

            pb_return_value = artifact.ListDockerImagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_docker_images(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_docker_images_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_docker_images._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_docker_images_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_docker_images"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_docker_images"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.ListDockerImagesRequest.pb(
            artifact.ListDockerImagesRequest()
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
        req.return_value._content = artifact.ListDockerImagesResponse.to_json(
            artifact.ListDockerImagesResponse()
        )

        request = artifact.ListDockerImagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.ListDockerImagesResponse()

        client.list_docker_images(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_docker_images_rest_bad_request(
    transport: str = "rest", request_type=artifact.ListDockerImagesRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_docker_images(request)


def test_list_docker_images_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListDockerImagesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListDockerImagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_docker_images(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/dockerImages"
            % client.transport._host,
            args[1],
        )


def test_list_docker_images_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_docker_images(
            artifact.ListDockerImagesRequest(),
            parent="parent_value",
        )


def test_list_docker_images_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[],
                next_page_token="def",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListDockerImagesResponse(
                docker_images=[
                    artifact.DockerImage(),
                    artifact.DockerImage(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(artifact.ListDockerImagesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_docker_images(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.DockerImage) for i in results)

        pages = list(client.list_docker_images(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetDockerImageRequest,
        dict,
    ],
)
def test_get_docker_image_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/dockerImages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.DockerImage(
            name="name_value",
            uri="uri_value",
            tags=["tags_value"],
            image_size_bytes=1699,
            media_type="media_type_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.DockerImage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_docker_image(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.DockerImage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.tags == ["tags_value"]
    assert response.image_size_bytes == 1699
    assert response.media_type == "media_type_value"


def test_get_docker_image_rest_required_fields(
    request_type=artifact.GetDockerImageRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_docker_image._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_docker_image._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.DockerImage()
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

            pb_return_value = artifact.DockerImage.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_docker_image(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_docker_image_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_docker_image._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_docker_image_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_docker_image"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_docker_image"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.GetDockerImageRequest.pb(artifact.GetDockerImageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = artifact.DockerImage.to_json(artifact.DockerImage())

        request = artifact.GetDockerImageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.DockerImage()

        client.get_docker_image(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_docker_image_rest_bad_request(
    transport: str = "rest", request_type=artifact.GetDockerImageRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/dockerImages/sample4"
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
        client.get_docker_image(request)


def test_get_docker_image_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.DockerImage()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/dockerImages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.DockerImage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_docker_image(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/dockerImages/*}"
            % client.transport._host,
            args[1],
        )


def test_get_docker_image_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_docker_image(
            artifact.GetDockerImageRequest(),
            name="name_value",
        )


def test_get_docker_image_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListMavenArtifactsRequest,
        dict,
    ],
)
def test_list_maven_artifacts_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListMavenArtifactsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListMavenArtifactsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_maven_artifacts(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMavenArtifactsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_maven_artifacts_rest_required_fields(
    request_type=artifact.ListMavenArtifactsRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_maven_artifacts._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_maven_artifacts._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.ListMavenArtifactsResponse()
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

            pb_return_value = artifact.ListMavenArtifactsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_maven_artifacts(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_maven_artifacts_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_maven_artifacts._get_unset_required_fields({})
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
def test_list_maven_artifacts_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_maven_artifacts"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_maven_artifacts"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.ListMavenArtifactsRequest.pb(
            artifact.ListMavenArtifactsRequest()
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
        req.return_value._content = artifact.ListMavenArtifactsResponse.to_json(
            artifact.ListMavenArtifactsResponse()
        )

        request = artifact.ListMavenArtifactsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.ListMavenArtifactsResponse()

        client.list_maven_artifacts(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_maven_artifacts_rest_bad_request(
    transport: str = "rest", request_type=artifact.ListMavenArtifactsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_maven_artifacts(request)


def test_list_maven_artifacts_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListMavenArtifactsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListMavenArtifactsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_maven_artifacts(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/mavenArtifacts"
            % client.transport._host,
            args[1],
        )


def test_list_maven_artifacts_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_maven_artifacts(
            artifact.ListMavenArtifactsRequest(),
            parent="parent_value",
        )


def test_list_maven_artifacts_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
                next_page_token="abc",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[],
                next_page_token="def",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListMavenArtifactsResponse(
                maven_artifacts=[
                    artifact.MavenArtifact(),
                    artifact.MavenArtifact(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            artifact.ListMavenArtifactsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_maven_artifacts(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.MavenArtifact) for i in results)

        pages = list(client.list_maven_artifacts(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetMavenArtifactRequest,
        dict,
    ],
)
def test_get_maven_artifact_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/mavenArtifacts/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.MavenArtifact(
            name="name_value",
            pom_uri="pom_uri_value",
            group_id="group_id_value",
            artifact_id="artifact_id_value",
            version="version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.MavenArtifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_maven_artifact(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.MavenArtifact)
    assert response.name == "name_value"
    assert response.pom_uri == "pom_uri_value"
    assert response.group_id == "group_id_value"
    assert response.artifact_id == "artifact_id_value"
    assert response.version == "version_value"


def test_get_maven_artifact_rest_required_fields(
    request_type=artifact.GetMavenArtifactRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_maven_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_maven_artifact._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.MavenArtifact()
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

            pb_return_value = artifact.MavenArtifact.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_maven_artifact(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_maven_artifact_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_maven_artifact._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_maven_artifact_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_maven_artifact"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_maven_artifact"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.GetMavenArtifactRequest.pb(
            artifact.GetMavenArtifactRequest()
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
        req.return_value._content = artifact.MavenArtifact.to_json(
            artifact.MavenArtifact()
        )

        request = artifact.GetMavenArtifactRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.MavenArtifact()

        client.get_maven_artifact(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_maven_artifact_rest_bad_request(
    transport: str = "rest", request_type=artifact.GetMavenArtifactRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/mavenArtifacts/sample4"
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
        client.get_maven_artifact(request)


def test_get_maven_artifact_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.MavenArtifact()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/mavenArtifacts/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.MavenArtifact.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_maven_artifact(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/mavenArtifacts/*}"
            % client.transport._host,
            args[1],
        )


def test_get_maven_artifact_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_maven_artifact(
            artifact.GetMavenArtifactRequest(),
            name="name_value",
        )


def test_get_maven_artifact_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListNpmPackagesRequest,
        dict,
    ],
)
def test_list_npm_packages_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListNpmPackagesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListNpmPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_npm_packages(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNpmPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_npm_packages_rest_required_fields(
    request_type=artifact.ListNpmPackagesRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_npm_packages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_npm_packages._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.ListNpmPackagesResponse()
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

            pb_return_value = artifact.ListNpmPackagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_npm_packages(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_npm_packages_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_npm_packages._get_unset_required_fields({})
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
def test_list_npm_packages_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_npm_packages"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_npm_packages"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.ListNpmPackagesRequest.pb(
            artifact.ListNpmPackagesRequest()
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
        req.return_value._content = artifact.ListNpmPackagesResponse.to_json(
            artifact.ListNpmPackagesResponse()
        )

        request = artifact.ListNpmPackagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.ListNpmPackagesResponse()

        client.list_npm_packages(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_npm_packages_rest_bad_request(
    transport: str = "rest", request_type=artifact.ListNpmPackagesRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_npm_packages(request)


def test_list_npm_packages_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListNpmPackagesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListNpmPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_npm_packages(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/npmPackages"
            % client.transport._host,
            args[1],
        )


def test_list_npm_packages_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_npm_packages(
            artifact.ListNpmPackagesRequest(),
            parent="parent_value",
        )


def test_list_npm_packages_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[],
                next_page_token="def",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListNpmPackagesResponse(
                npm_packages=[
                    artifact.NpmPackage(),
                    artifact.NpmPackage(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(artifact.ListNpmPackagesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_npm_packages(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.NpmPackage) for i in results)

        pages = list(client.list_npm_packages(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetNpmPackageRequest,
        dict,
    ],
)
def test_get_npm_package_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/npmPackages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.NpmPackage(
            name="name_value",
            package_name="package_name_value",
            version="version_value",
            tags=["tags_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.NpmPackage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_npm_package(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.NpmPackage)
    assert response.name == "name_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"
    assert response.tags == ["tags_value"]


def test_get_npm_package_rest_required_fields(
    request_type=artifact.GetNpmPackageRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_npm_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_npm_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.NpmPackage()
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

            pb_return_value = artifact.NpmPackage.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_npm_package(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_npm_package_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_npm_package._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_npm_package_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_npm_package"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_npm_package"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.GetNpmPackageRequest.pb(artifact.GetNpmPackageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = artifact.NpmPackage.to_json(artifact.NpmPackage())

        request = artifact.GetNpmPackageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.NpmPackage()

        client.get_npm_package(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_npm_package_rest_bad_request(
    transport: str = "rest", request_type=artifact.GetNpmPackageRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/npmPackages/sample4"
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
        client.get_npm_package(request)


def test_get_npm_package_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.NpmPackage()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/npmPackages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.NpmPackage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_npm_package(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/npmPackages/*}"
            % client.transport._host,
            args[1],
        )


def test_get_npm_package_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_npm_package(
            artifact.GetNpmPackageRequest(),
            name="name_value",
        )


def test_get_npm_package_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.ListPythonPackagesRequest,
        dict,
    ],
)
def test_list_python_packages_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListPythonPackagesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListPythonPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_python_packages(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPythonPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_python_packages_rest_required_fields(
    request_type=artifact.ListPythonPackagesRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_python_packages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_python_packages._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.ListPythonPackagesResponse()
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

            pb_return_value = artifact.ListPythonPackagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_python_packages(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_python_packages_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_python_packages._get_unset_required_fields({})
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
def test_list_python_packages_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_python_packages"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_python_packages"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.ListPythonPackagesRequest.pb(
            artifact.ListPythonPackagesRequest()
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
        req.return_value._content = artifact.ListPythonPackagesResponse.to_json(
            artifact.ListPythonPackagesResponse()
        )

        request = artifact.ListPythonPackagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.ListPythonPackagesResponse()

        client.list_python_packages(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_python_packages_rest_bad_request(
    transport: str = "rest", request_type=artifact.ListPythonPackagesRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_python_packages(request)


def test_list_python_packages_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.ListPythonPackagesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.ListPythonPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_python_packages(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/pythonPackages"
            % client.transport._host,
            args[1],
        )


def test_list_python_packages_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_python_packages(
            artifact.ListPythonPackagesRequest(),
            parent="parent_value",
        )


def test_list_python_packages_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
                next_page_token="abc",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[],
                next_page_token="def",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                ],
                next_page_token="ghi",
            ),
            artifact.ListPythonPackagesResponse(
                python_packages=[
                    artifact.PythonPackage(),
                    artifact.PythonPackage(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            artifact.ListPythonPackagesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_python_packages(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, artifact.PythonPackage) for i in results)

        pages = list(client.list_python_packages(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        artifact.GetPythonPackageRequest,
        dict,
    ],
)
def test_get_python_package_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/pythonPackages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.PythonPackage(
            name="name_value",
            uri="uri_value",
            package_name="package_name_value",
            version="version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.PythonPackage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_python_package(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, artifact.PythonPackage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"
    assert response.package_name == "package_name_value"
    assert response.version == "version_value"


def test_get_python_package_rest_required_fields(
    request_type=artifact.GetPythonPackageRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_python_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_python_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = artifact.PythonPackage()
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

            pb_return_value = artifact.PythonPackage.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_python_package(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_python_package_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_python_package._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_python_package_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_python_package"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_python_package"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = artifact.GetPythonPackageRequest.pb(
            artifact.GetPythonPackageRequest()
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
        req.return_value._content = artifact.PythonPackage.to_json(
            artifact.PythonPackage()
        )

        request = artifact.GetPythonPackageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = artifact.PythonPackage()

        client.get_python_package(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_python_package_rest_bad_request(
    transport: str = "rest", request_type=artifact.GetPythonPackageRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/pythonPackages/sample4"
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
        client.get_python_package(request)


def test_get_python_package_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = artifact.PythonPackage()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/pythonPackages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = artifact.PythonPackage.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_python_package(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/pythonPackages/*}"
            % client.transport._host,
            args[1],
        )


def test_get_python_package_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_python_package(
            artifact.GetPythonPackageRequest(),
            name="name_value",
        )


def test_get_python_package_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        apt_artifact.ImportAptArtifactsRequest,
        dict,
    ],
)
def test_import_apt_artifacts_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        response = client.import_apt_artifacts(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_import_apt_artifacts_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_import_apt_artifacts"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_import_apt_artifacts"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = apt_artifact.ImportAptArtifactsRequest.pb(
            apt_artifact.ImportAptArtifactsRequest()
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

        request = apt_artifact.ImportAptArtifactsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.import_apt_artifacts(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_import_apt_artifacts_rest_bad_request(
    transport: str = "rest", request_type=apt_artifact.ImportAptArtifactsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.import_apt_artifacts(request)


def test_import_apt_artifacts_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        yum_artifact.ImportYumArtifactsRequest,
        dict,
    ],
)
def test_import_yum_artifacts_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        response = client.import_yum_artifacts(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_import_yum_artifacts_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_import_yum_artifacts"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_import_yum_artifacts"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = yum_artifact.ImportYumArtifactsRequest.pb(
            yum_artifact.ImportYumArtifactsRequest()
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

        request = yum_artifact.ImportYumArtifactsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.import_yum_artifacts(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_import_yum_artifacts_rest_bad_request(
    transport: str = "rest", request_type=yum_artifact.ImportYumArtifactsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.import_yum_artifacts(request)


def test_import_yum_artifacts_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        repository.ListRepositoriesRequest,
        dict,
    ],
)
def test_list_repositories_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = repository.ListRepositoriesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = repository.ListRepositoriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_repositories(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRepositoriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_repositories_rest_required_fields(
    request_type=repository.ListRepositoriesRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_repositories._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_repositories._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = repository.ListRepositoriesResponse()
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

            pb_return_value = repository.ListRepositoriesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_repositories(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_repositories_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_repositories._get_unset_required_fields({})
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
def test_list_repositories_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_repositories"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_repositories"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = repository.ListRepositoriesRequest.pb(
            repository.ListRepositoriesRequest()
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
        req.return_value._content = repository.ListRepositoriesResponse.to_json(
            repository.ListRepositoriesResponse()
        )

        request = repository.ListRepositoriesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = repository.ListRepositoriesResponse()

        client.list_repositories(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_repositories_rest_bad_request(
    transport: str = "rest", request_type=repository.ListRepositoriesRequest
):
    client = ArtifactRegistryClient(
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
        client.list_repositories(request)


def test_list_repositories_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = repository.ListRepositoriesResponse()

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
        pb_return_value = repository.ListRepositoriesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_repositories(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/repositories"
            % client.transport._host,
            args[1],
        )


def test_list_repositories_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_repositories(
            repository.ListRepositoriesRequest(),
            parent="parent_value",
        )


def test_list_repositories_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                    repository.Repository(),
                ],
                next_page_token="abc",
            ),
            repository.ListRepositoriesResponse(
                repositories=[],
                next_page_token="def",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                ],
                next_page_token="ghi",
            ),
            repository.ListRepositoriesResponse(
                repositories=[
                    repository.Repository(),
                    repository.Repository(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            repository.ListRepositoriesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_repositories(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, repository.Repository) for i in results)

        pages = list(client.list_repositories(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        repository.GetRepositoryRequest,
        dict,
    ],
)
def test_get_repository_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = repository.Repository(
            name="name_value",
            format_=repository.Repository.Format.DOCKER,
            description="description_value",
            kms_key_name="kms_key_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = repository.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_repository(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


def test_get_repository_rest_required_fields(
    request_type=repository.GetRepositoryRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = repository.Repository()
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

            pb_return_value = repository.Repository.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_repository_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_repository_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_repository"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = repository.GetRepositoryRequest.pb(
            repository.GetRepositoryRequest()
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
        req.return_value._content = repository.Repository.to_json(
            repository.Repository()
        )

        request = repository.GetRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = repository.Repository()

        client.get_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_repository_rest_bad_request(
    transport: str = "rest", request_type=repository.GetRepositoryRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.get_repository(request)


def test_get_repository_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = repository.Repository()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = repository.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_get_repository_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_repository(
            repository.GetRepositoryRequest(),
            name="name_value",
        )


def test_get_repository_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_repository.CreateRepositoryRequest,
        dict,
    ],
)
def test_create_repository_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["repository"] = {
        "maven_config": {"allow_snapshot_overwrites": True, "version_policy": 1},
        "name": "name_value",
        "format_": 1,
        "description": "description_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "kms_key_name": "kms_key_name_value",
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
        response = client.create_repository(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_repository_rest_required_fields(
    request_type=gda_repository.CreateRepositoryRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).create_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_repository._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("repository_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = ArtifactRegistryClient(
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

            response = client.create_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_repository_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(("repositoryId",)) & set(("parent",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_repository_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_create_repository"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_create_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gda_repository.CreateRepositoryRequest.pb(
            gda_repository.CreateRepositoryRequest()
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

        request = gda_repository.CreateRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_repository_rest_bad_request(
    transport: str = "rest", request_type=gda_repository.CreateRepositoryRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["repository"] = {
        "maven_config": {"allow_snapshot_overwrites": True, "version_policy": 1},
        "name": "name_value",
        "format_": 1,
        "description": "description_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "kms_key_name": "kms_key_name_value",
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
        client.create_repository(request)


def test_create_repository_rest_flattened():
    client = ArtifactRegistryClient(
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
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/repositories"
            % client.transport._host,
            args[1],
        )


def test_create_repository_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_repository(
            gda_repository.CreateRepositoryRequest(),
            parent="parent_value",
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            repository_id="repository_id_value",
        )


def test_create_repository_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_repository.UpdateRepositoryRequest,
        dict,
    ],
)
def test_update_repository_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "repository": {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }
    }
    request_init["repository"] = {
        "maven_config": {"allow_snapshot_overwrites": True, "version_policy": 1},
        "name": "projects/sample1/locations/sample2/repositories/sample3",
        "format_": 1,
        "description": "description_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "kms_key_name": "kms_key_name_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_repository.Repository(
            name="name_value",
            format_=gda_repository.Repository.Format.DOCKER,
            description="description_value",
            kms_key_name="kms_key_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_repository.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_repository(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_repository.Repository)
    assert response.name == "name_value"
    assert response.format_ == gda_repository.Repository.Format.DOCKER
    assert response.description == "description_value"
    assert response.kms_key_name == "kms_key_name_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_repository_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_update_repository"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_update_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gda_repository.UpdateRepositoryRequest.pb(
            gda_repository.UpdateRepositoryRequest()
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
        req.return_value._content = gda_repository.Repository.to_json(
            gda_repository.Repository()
        )

        request = gda_repository.UpdateRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gda_repository.Repository()

        client.update_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_repository_rest_bad_request(
    transport: str = "rest", request_type=gda_repository.UpdateRepositoryRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "repository": {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
        }
    }
    request_init["repository"] = {
        "maven_config": {"allow_snapshot_overwrites": True, "version_policy": 1},
        "name": "projects/sample1/locations/sample2/repositories/sample3",
        "format_": 1,
        "description": "description_value",
        "labels": {},
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "kms_key_name": "kms_key_name_value",
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
        client.update_repository(request)


def test_update_repository_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_repository.Repository()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "repository": {
                "name": "projects/sample1/locations/sample2/repositories/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_repository.Repository.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{repository.name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_update_repository_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_repository(
            gda_repository.UpdateRepositoryRequest(),
            repository=gda_repository.Repository(
                maven_config=gda_repository.Repository.MavenRepositoryConfig(
                    allow_snapshot_overwrites=True
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_repository_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        repository.DeleteRepositoryRequest,
        dict,
    ],
)
def test_delete_repository_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        response = client.delete_repository(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_repository_rest_required_fields(
    request_type=repository.DeleteRepositoryRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).delete_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_repository._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
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

            response = client.delete_repository(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_repository_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_repository._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_repository_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_delete_repository"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_delete_repository"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = repository.DeleteRepositoryRequest.pb(
            repository.DeleteRepositoryRequest()
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

        request = repository.DeleteRepositoryRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_repository(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_repository_rest_bad_request(
    transport: str = "rest", request_type=repository.DeleteRepositoryRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.delete_repository(request)


def test_delete_repository_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3"
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

        client.delete_repository(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_repository_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_repository(
            repository.DeleteRepositoryRequest(),
            name="name_value",
        )


def test_delete_repository_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        package.ListPackagesRequest,
        dict,
    ],
)
def test_list_packages_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = package.ListPackagesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = package.ListPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_packages(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPackagesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_packages_rest_required_fields(request_type=package.ListPackagesRequest):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_packages._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_packages._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = package.ListPackagesResponse()
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

            pb_return_value = package.ListPackagesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_packages(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_packages_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_packages._get_unset_required_fields({})
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
def test_list_packages_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_packages"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_packages"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = package.ListPackagesRequest.pb(package.ListPackagesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = package.ListPackagesResponse.to_json(
            package.ListPackagesResponse()
        )

        request = package.ListPackagesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = package.ListPackagesResponse()

        client.list_packages(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_packages_rest_bad_request(
    transport: str = "rest", request_type=package.ListPackagesRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_packages(request)


def test_list_packages_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = package.ListPackagesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = package.ListPackagesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_packages(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/packages"
            % client.transport._host,
            args[1],
        )


def test_list_packages_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_packages(
            package.ListPackagesRequest(),
            parent="parent_value",
        )


def test_list_packages_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                    package.Package(),
                ],
                next_page_token="abc",
            ),
            package.ListPackagesResponse(
                packages=[],
                next_page_token="def",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                ],
                next_page_token="ghi",
            ),
            package.ListPackagesResponse(
                packages=[
                    package.Package(),
                    package.Package(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(package.ListPackagesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_packages(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, package.Package) for i in results)

        pages = list(client.list_packages(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        package.GetPackageRequest,
        dict,
    ],
)
def test_get_package_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = package.Package(
            name="name_value",
            display_name="display_name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = package.Package.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_package(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, package.Package)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_package_rest_required_fields(request_type=package.GetPackageRequest):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = package.Package()
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

            pb_return_value = package.Package.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_package(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_package_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_package._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_package_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_package"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_package"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = package.GetPackageRequest.pb(package.GetPackageRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = package.Package.to_json(package.Package())

        request = package.GetPackageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = package.Package()

        client.get_package(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_package_rest_bad_request(
    transport: str = "rest", request_type=package.GetPackageRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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
        client.get_package(request)


def test_get_package_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = package.Package()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = package.Package.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_package(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*}"
            % client.transport._host,
            args[1],
        )


def test_get_package_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_package(
            package.GetPackageRequest(),
            name="name_value",
        )


def test_get_package_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        package.DeletePackageRequest,
        dict,
    ],
)
def test_delete_package_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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
        response = client.delete_package(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_package_rest_required_fields(request_type=package.DeletePackageRequest):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).delete_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_package._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
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

            response = client.delete_package(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_package_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_package._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_package_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_delete_package"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_delete_package"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = package.DeletePackageRequest.pb(package.DeletePackageRequest())
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

        request = package.DeletePackageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_package(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_package_rest_bad_request(
    transport: str = "rest", request_type=package.DeletePackageRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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
        client.delete_package(request)


def test_delete_package_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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

        client.delete_package(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_package_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_package(
            package.DeletePackageRequest(),
            name="name_value",
        )


def test_delete_package_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        version.ListVersionsRequest,
        dict,
    ],
)
def test_list_versions_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = version.ListVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = version.ListVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVersionsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_versions_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_versions"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = version.ListVersionsRequest.pb(version.ListVersionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = version.ListVersionsResponse.to_json(
            version.ListVersionsResponse()
        )

        request = version.ListVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = version.ListVersionsResponse()

        client.list_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_versions_rest_bad_request(
    transport: str = "rest", request_type=version.ListVersionsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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
        client.list_versions(request)


def test_list_versions_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = version.ListVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = version.ListVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/versions"
            % client.transport._host,
            args[1],
        )


def test_list_versions_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_versions(
            version.ListVersionsRequest(),
            parent="parent_value",
        )


def test_list_versions_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                    version.Version(),
                ],
                next_page_token="abc",
            ),
            version.ListVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                ],
                next_page_token="ghi",
            ),
            version.ListVersionsResponse(
                versions=[
                    version.Version(),
                    version.Version(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(version.ListVersionsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        pager = client.list_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, version.Version) for i in results)

        pages = list(client.list_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        version.GetVersionRequest,
        dict,
    ],
)
def test_get_version_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = version.Version(
            name="name_value",
            description="description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = version.Version.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_version(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, version.Version)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_version_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_version"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = version.GetVersionRequest.pb(version.GetVersionRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = version.Version.to_json(version.Version())

        request = version.GetVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = version.Version()

        client.get_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_version_rest_bad_request(
    transport: str = "rest", request_type=version.GetVersionRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
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
        client.get_version(request)


def test_get_version_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = version.Version()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = version.Version.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_version_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_version(
            version.GetVersionRequest(),
            name="name_value",
        )


def test_get_version_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        version.DeleteVersionRequest,
        dict,
    ],
)
def test_delete_version_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
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
        response = client.delete_version(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_version_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_delete_version"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_delete_version"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = version.DeleteVersionRequest.pb(version.DeleteVersionRequest())
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

        request = version.DeleteVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_version_rest_bad_request(
    transport: str = "rest", request_type=version.DeleteVersionRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
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
        client.delete_version(request)


def test_delete_version_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/versions/sample5"
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

        client.delete_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*/versions/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_version_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_version(
            version.DeleteVersionRequest(),
            name="name_value",
        )


def test_delete_version_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        file.ListFilesRequest,
        dict,
    ],
)
def test_list_files_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = file.ListFilesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = file.ListFilesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_files(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFilesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_files_rest_required_fields(request_type=file.ListFilesRequest):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).list_files._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_files._get_unset_required_fields(jsonified_request)
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

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = file.ListFilesResponse()
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

            pb_return_value = file.ListFilesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_files(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_files_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_files._get_unset_required_fields({})
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
def test_list_files_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_files"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_files"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = file.ListFilesRequest.pb(file.ListFilesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = file.ListFilesResponse.to_json(
            file.ListFilesResponse()
        )

        request = file.ListFilesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = file.ListFilesResponse()

        client.list_files(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_files_rest_bad_request(
    transport: str = "rest", request_type=file.ListFilesRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/repositories/sample3"}
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
        client.list_files(request)


def test_list_files_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = file.ListFilesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = file.ListFilesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_files(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*}/files"
            % client.transport._host,
            args[1],
        )


def test_list_files_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_files(
            file.ListFilesRequest(),
            parent="parent_value",
        )


def test_list_files_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                    file.File(),
                ],
                next_page_token="abc",
            ),
            file.ListFilesResponse(
                files=[],
                next_page_token="def",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                ],
                next_page_token="ghi",
            ),
            file.ListFilesResponse(
                files=[
                    file.File(),
                    file.File(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(file.ListFilesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3"
        }

        pager = client.list_files(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, file.File) for i in results)

        pages = list(client.list_files(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        file.GetFileRequest,
        dict,
    ],
)
def test_get_file_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/files/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = file.File(
            name="name_value",
            size_bytes=1089,
            owner="owner_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = file.File.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_file(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, file.File)
    assert response.name == "name_value"
    assert response.size_bytes == 1089
    assert response.owner == "owner_value"


def test_get_file_rest_required_fields(request_type=file.GetFileRequest):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_file._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = file.File()
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

            pb_return_value = file.File.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_file(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_file_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_file._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_file_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_file"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_file"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = file.GetFileRequest.pb(file.GetFileRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = file.File.to_json(file.File())

        request = file.GetFileRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = file.File()

        client.get_file(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_file_rest_bad_request(
    transport: str = "rest", request_type=file.GetFileRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/files/sample4"
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
        client.get_file(request)


def test_get_file_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = file.File()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/files/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = file.File.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_file(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/files/**}"
            % client.transport._host,
            args[1],
        )


def test_get_file_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_file(
            file.GetFileRequest(),
            name="name_value",
        )


def test_get_file_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tag.ListTagsRequest,
        dict,
    ],
)
def test_list_tags_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tag.ListTagsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tag.ListTagsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tags(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTagsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tags_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_list_tags"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_list_tags"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tag.ListTagsRequest.pb(tag.ListTagsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tag.ListTagsResponse.to_json(tag.ListTagsResponse())

        request = tag.ListTagsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tag.ListTagsResponse()

        client.list_tags(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tags_rest_bad_request(
    transport: str = "rest", request_type=tag.ListTagsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
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
        client.list_tags(request)


def test_list_tags_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tag.ListTagsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tag.ListTagsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tags(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/tags"
            % client.transport._host,
            args[1],
        )


def test_list_tags_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tags(
            tag.ListTagsRequest(),
            parent="parent_value",
        )


def test_list_tags_rest_pager(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                    tag.Tag(),
                ],
                next_page_token="abc",
            ),
            tag.ListTagsResponse(
                tags=[],
                next_page_token="def",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                ],
                next_page_token="ghi",
            ),
            tag.ListTagsResponse(
                tags=[
                    tag.Tag(),
                    tag.Tag(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(tag.ListTagsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        pager = client.list_tags(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tag.Tag) for i in results)

        pages = list(client.list_tags(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        tag.GetTagRequest,
        dict,
    ],
)
def test_get_tag_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tag.Tag(
            name="name_value",
            version="version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_tag(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_tag_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_tag"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_tag"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = tag.GetTagRequest.pb(tag.GetTagRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = tag.Tag.to_json(tag.Tag())

        request = tag.GetTagRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = tag.Tag()

        client.get_tag(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_tag_rest_bad_request(
    transport: str = "rest", request_type=tag.GetTagRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
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
        client.get_tag(request)


def test_get_tag_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = tag.Tag()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_tag(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*/tags/*}"
            % client.transport._host,
            args[1],
        )


def test_get_tag_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tag(
            tag.GetTagRequest(),
            name="name_value",
        )


def test_get_tag_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_tag.CreateTagRequest,
        dict,
    ],
)
def test_create_tag_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
    }
    request_init["tag"] = {"name": "name_value", "version": "version_value"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_tag.Tag(
            name="name_value",
            version="version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_tag(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_tag_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_create_tag"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_create_tag"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gda_tag.CreateTagRequest.pb(gda_tag.CreateTagRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gda_tag.Tag.to_json(gda_tag.Tag())

        request = gda_tag.CreateTagRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gda_tag.Tag()

        client.create_tag(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_tag_rest_bad_request(
    transport: str = "rest", request_type=gda_tag.CreateTagRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
    }
    request_init["tag"] = {"name": "name_value", "version": "version_value"}
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
        client.create_tag(request)


def test_create_tag_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_tag.Tag()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_tag(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/repositories/*/packages/*}/tags"
            % client.transport._host,
            args[1],
        )


def test_create_tag_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_tag(
            gda_tag.CreateTagRequest(),
            parent="parent_value",
            tag=gda_tag.Tag(name="name_value"),
            tag_id="tag_id_value",
        )


def test_create_tag_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_tag.UpdateTagRequest,
        dict,
    ],
)
def test_update_tag_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tag": {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
        }
    }
    request_init["tag"] = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5",
        "version": "version_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_tag.Tag(
            name="name_value",
            version="version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_tag(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_tag.Tag)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_tag_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_update_tag"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_update_tag"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gda_tag.UpdateTagRequest.pb(gda_tag.UpdateTagRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gda_tag.Tag.to_json(gda_tag.Tag())

        request = gda_tag.UpdateTagRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gda_tag.Tag()

        client.update_tag(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_tag_rest_bad_request(
    transport: str = "rest", request_type=gda_tag.UpdateTagRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "tag": {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
        }
    }
    request_init["tag"] = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5",
        "version": "version_value",
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
        client.update_tag(request)


def test_update_tag_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_tag.Tag()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "tag": {
                "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_tag.Tag.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_tag(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{tag.name=projects/*/locations/*/repositories/*/packages/*/tags/*}"
            % client.transport._host,
            args[1],
        )


def test_update_tag_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_tag(
            gda_tag.UpdateTagRequest(),
            tag=gda_tag.Tag(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_tag_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        tag.DeleteTagRequest,
        dict,
    ],
)
def test_delete_tag_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
    }
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
        response = client.delete_tag(request)

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_tag_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_delete_tag"
    ) as pre:
        pre.assert_not_called()
        pb_message = tag.DeleteTagRequest.pb(tag.DeleteTagRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = tag.DeleteTagRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_tag(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_tag_rest_bad_request(
    transport: str = "rest", request_type=tag.DeleteTagRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
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
        client.delete_tag(request)


def test_delete_tag_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/repositories/sample3/packages/sample4/tags/sample5"
        }

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

        client.delete_tag(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/repositories/*/packages/*/tags/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_tag_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_tag(
            tag.DeleteTagRequest(),
            name="name_value",
        )


def test_delete_tag_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_rest_required_fields(
    request_type=iam_policy_pb2.SetIamPolicyRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

    request_init = {}
    request_init["resource"] = ""
    request = request_type(**request_init)
    pb_request = request
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
    ).set_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).set_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = policy_pb2.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.set_iam_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_set_iam_policy_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.set_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "resource",
                "policy",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_set_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_set_iam_policy"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_set_iam_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.SetIamPolicyRequest()
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(policy_pb2.Policy())

        request = iam_policy_pb2.SetIamPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = policy_pb2.Policy()

        client.set_iam_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
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
        client.set_iam_policy(request)


def test_set_iam_policy_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_rest_required_fields(
    request_type=iam_policy_pb2.GetIamPolicyRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

    request_init = {}
    request_init["resource"] = ""
    request = request_type(**request_init)
    pb_request = request
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
    ).get_iam_policy._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_iam_policy._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("options",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = policy_pb2.Policy()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_iam_policy(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_iam_policy_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_iam_policy._get_unset_required_fields({})
    assert set(unset_fields) == (set(("options",)) & set(("resource",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_iam_policy_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_iam_policy"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_iam_policy"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.GetIamPolicyRequest()
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(policy_pb2.Policy())

        request = iam_policy_pb2.GetIamPolicyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = policy_pb2.Policy()

        client.get_iam_policy(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
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
        client.get_iam_policy(request)


def test_get_iam_policy_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = return_value
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_rest_required_fields(
    request_type=iam_policy_pb2.TestIamPermissionsRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

    request_init = {}
    request_init["resource"] = ""
    request_init["permissions"] = ""
    request = request_type(**request_init)
    pb_request = request
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
    ).test_iam_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"
    jsonified_request["permissions"] = "permissions_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).test_iam_permissions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"
    assert "permissions" in jsonified_request
    assert jsonified_request["permissions"] == "permissions_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = iam_policy_pb2.TestIamPermissionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = return_value
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.test_iam_permissions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_test_iam_permissions_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.test_iam_permissions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "resource",
                "permissions",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_test_iam_permissions_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_test_iam_permissions"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_test_iam_permissions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = iam_policy_pb2.TestIamPermissionsRequest()
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
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        request = iam_policy_pb2.TestIamPermissionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "resource": "projects/sample1/locations/sample2/repositories/sample3"
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
        client.test_iam_permissions(request)


def test_test_iam_permissions_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        settings.GetProjectSettingsRequest,
        dict,
    ],
)
def test_get_project_settings_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/projectSettings"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = settings.ProjectSettings(
            name="name_value",
            legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = settings.ProjectSettings.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_project_settings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


def test_get_project_settings_rest_required_fields(
    request_type=settings.GetProjectSettingsRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_project_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_project_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = settings.ProjectSettings()
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

            pb_return_value = settings.ProjectSettings.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_project_settings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_project_settings_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_project_settings._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_project_settings_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_project_settings"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_project_settings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = settings.GetProjectSettingsRequest.pb(
            settings.GetProjectSettingsRequest()
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
        req.return_value._content = settings.ProjectSettings.to_json(
            settings.ProjectSettings()
        )

        request = settings.GetProjectSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = settings.ProjectSettings()

        client.get_project_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_project_settings_rest_bad_request(
    transport: str = "rest", request_type=settings.GetProjectSettingsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/projectSettings"}
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
        client.get_project_settings(request)


def test_get_project_settings_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = settings.ProjectSettings()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/projectSettings"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = settings.ProjectSettings.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_project_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/projectSettings}" % client.transport._host, args[1]
        )


def test_get_project_settings_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_project_settings(
            settings.GetProjectSettingsRequest(),
            name="name_value",
        )


def test_get_project_settings_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        settings.UpdateProjectSettingsRequest,
        dict,
    ],
)
def test_update_project_settings_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"project_settings": {"name": "projects/sample1/projectSettings"}}
    request_init["project_settings"] = {
        "name": "projects/sample1/projectSettings",
        "legacy_redirection_state": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = settings.ProjectSettings(
            name="name_value",
            legacy_redirection_state=settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = settings.ProjectSettings.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_project_settings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, settings.ProjectSettings)
    assert response.name == "name_value"
    assert (
        response.legacy_redirection_state
        == settings.ProjectSettings.RedirectionState.REDIRECTION_FROM_GCR_IO_DISABLED
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_project_settings_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_update_project_settings"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_update_project_settings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = settings.UpdateProjectSettingsRequest.pb(
            settings.UpdateProjectSettingsRequest()
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
        req.return_value._content = settings.ProjectSettings.to_json(
            settings.ProjectSettings()
        )

        request = settings.UpdateProjectSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = settings.ProjectSettings()

        client.update_project_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_project_settings_rest_bad_request(
    transport: str = "rest", request_type=settings.UpdateProjectSettingsRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project_settings": {"name": "projects/sample1/projectSettings"}}
    request_init["project_settings"] = {
        "name": "projects/sample1/projectSettings",
        "legacy_redirection_state": 1,
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
        client.update_project_settings(request)


def test_update_project_settings_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = settings.ProjectSettings()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project_settings": {"name": "projects/sample1/projectSettings"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = settings.ProjectSettings.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_project_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{project_settings.name=projects/*/projectSettings}"
            % client.transport._host,
            args[1],
        )


def test_update_project_settings_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_project_settings(
            settings.UpdateProjectSettingsRequest(),
            project_settings=settings.ProjectSettings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_project_settings_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        vpcsc_config.GetVPCSCConfigRequest,
        dict,
    ],
)
def test_get_vpcsc_config_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpcscConfig"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = vpcsc_config.VPCSCConfig(
            name="name_value",
            vpcsc_policy=vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = vpcsc_config.VPCSCConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_vpcsc_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


def test_get_vpcsc_config_rest_required_fields(
    request_type=vpcsc_config.GetVPCSCConfigRequest,
):
    transport_class = transports.ArtifactRegistryRestTransport

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
    ).get_vpcsc_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vpcsc_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = vpcsc_config.VPCSCConfig()
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

            pb_return_value = vpcsc_config.VPCSCConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_vpcsc_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_vpcsc_config_rest_unset_required_fields():
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_vpcsc_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_vpcsc_config_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_get_vpcsc_config"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_get_vpcsc_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = vpcsc_config.GetVPCSCConfigRequest.pb(
            vpcsc_config.GetVPCSCConfigRequest()
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
        req.return_value._content = vpcsc_config.VPCSCConfig.to_json(
            vpcsc_config.VPCSCConfig()
        )

        request = vpcsc_config.GetVPCSCConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = vpcsc_config.VPCSCConfig()

        client.get_vpcsc_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_vpcsc_config_rest_bad_request(
    transport: str = "rest", request_type=vpcsc_config.GetVPCSCConfigRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpcscConfig"}
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
        client.get_vpcsc_config(request)


def test_get_vpcsc_config_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = vpcsc_config.VPCSCConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/vpcscConfig"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = vpcsc_config.VPCSCConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_vpcsc_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vpcscConfig}" % client.transport._host,
            args[1],
        )


def test_get_vpcsc_config_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vpcsc_config(
            vpcsc_config.GetVPCSCConfigRequest(),
            name="name_value",
        )


def test_get_vpcsc_config_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gda_vpcsc_config.UpdateVPCSCConfigRequest,
        dict,
    ],
)
def test_update_vpcsc_config_rest(request_type):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "vpcsc_config": {"name": "projects/sample1/locations/sample2/vpcscConfig"}
    }
    request_init["vpcsc_config"] = {
        "name": "projects/sample1/locations/sample2/vpcscConfig",
        "vpcsc_policy": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_vpcsc_config.VPCSCConfig(
            name="name_value",
            vpcsc_policy=gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_vpcsc_config.VPCSCConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_vpcsc_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gda_vpcsc_config.VPCSCConfig)
    assert response.name == "name_value"
    assert response.vpcsc_policy == gda_vpcsc_config.VPCSCConfig.VPCSCPolicy.DENY


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_vpcsc_config_rest_interceptors(null_interceptor):
    transport = transports.ArtifactRegistryRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.ArtifactRegistryRestInterceptor(),
    )
    client = ArtifactRegistryClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "post_update_vpcsc_config"
    ) as post, mock.patch.object(
        transports.ArtifactRegistryRestInterceptor, "pre_update_vpcsc_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gda_vpcsc_config.UpdateVPCSCConfigRequest.pb(
            gda_vpcsc_config.UpdateVPCSCConfigRequest()
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
        req.return_value._content = gda_vpcsc_config.VPCSCConfig.to_json(
            gda_vpcsc_config.VPCSCConfig()
        )

        request = gda_vpcsc_config.UpdateVPCSCConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gda_vpcsc_config.VPCSCConfig()

        client.update_vpcsc_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_vpcsc_config_rest_bad_request(
    transport: str = "rest", request_type=gda_vpcsc_config.UpdateVPCSCConfigRequest
):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "vpcsc_config": {"name": "projects/sample1/locations/sample2/vpcscConfig"}
    }
    request_init["vpcsc_config"] = {
        "name": "projects/sample1/locations/sample2/vpcscConfig",
        "vpcsc_policy": 1,
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
        client.update_vpcsc_config(request)


def test_update_vpcsc_config_rest_flattened():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gda_vpcsc_config.VPCSCConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "vpcsc_config": {"name": "projects/sample1/locations/sample2/vpcscConfig"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gda_vpcsc_config.VPCSCConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_vpcsc_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{vpcsc_config.name=projects/*/locations/*/vpcscConfig}"
            % client.transport._host,
            args[1],
        )


def test_update_vpcsc_config_rest_flattened_error(transport: str = "rest"):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_vpcsc_config(
            gda_vpcsc_config.UpdateVPCSCConfigRequest(),
            vpcsc_config=gda_vpcsc_config.VPCSCConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_vpcsc_config_rest_error():
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ArtifactRegistryClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ArtifactRegistryClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ArtifactRegistryClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ArtifactRegistryClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ArtifactRegistryClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ArtifactRegistryClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ArtifactRegistryGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ArtifactRegistryGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
        transports.ArtifactRegistryRestTransport,
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
    transport = ArtifactRegistryClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ArtifactRegistryGrpcTransport,
    )


def test_artifact_registry_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ArtifactRegistryTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_artifact_registry_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.artifactregistry_v1.services.artifact_registry.transports.ArtifactRegistryTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ArtifactRegistryTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_docker_images",
        "get_docker_image",
        "list_maven_artifacts",
        "get_maven_artifact",
        "list_npm_packages",
        "get_npm_package",
        "list_python_packages",
        "get_python_package",
        "import_apt_artifacts",
        "import_yum_artifacts",
        "list_repositories",
        "get_repository",
        "create_repository",
        "update_repository",
        "delete_repository",
        "list_packages",
        "get_package",
        "delete_package",
        "list_versions",
        "get_version",
        "delete_version",
        "list_files",
        "get_file",
        "list_tags",
        "get_tag",
        "create_tag",
        "update_tag",
        "delete_tag",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_project_settings",
        "update_project_settings",
        "get_vpcsc_config",
        "update_vpcsc_config",
        "get_location",
        "list_locations",
        "get_operation",
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


def test_artifact_registry_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.artifactregistry_v1.services.artifact_registry.transports.ArtifactRegistryTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ArtifactRegistryTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id="octopus",
        )


def test_artifact_registry_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.artifactregistry_v1.services.artifact_registry.transports.ArtifactRegistryTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ArtifactRegistryTransport()
        adc.assert_called_once()


def test_artifact_registry_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ArtifactRegistryClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
    ],
)
def test_artifact_registry_transport_auth_adc(transport_class):
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
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
        transports.ArtifactRegistryRestTransport,
    ],
)
def test_artifact_registry_transport_auth_gdch_credentials(transport_class):
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
        (transports.ArtifactRegistryGrpcTransport, grpc_helpers),
        (transports.ArtifactRegistryGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_artifact_registry_transport_create_channel(transport_class, grpc_helpers):
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
            "artifactregistry.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
            ),
            scopes=["1", "2"],
            default_host="artifactregistry.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
    ],
)
def test_artifact_registry_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_artifact_registry_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.ArtifactRegistryRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_artifact_registry_rest_lro_client():
    client = ArtifactRegistryClient(
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
def test_artifact_registry_host_no_port(transport_name):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="artifactregistry.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "artifactregistry.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://artifactregistry.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_artifact_registry_host_with_port(transport_name):
    client = ArtifactRegistryClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="artifactregistry.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "artifactregistry.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://artifactregistry.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_artifact_registry_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = ArtifactRegistryClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = ArtifactRegistryClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_docker_images._session
    session2 = client2.transport.list_docker_images._session
    assert session1 != session2
    session1 = client1.transport.get_docker_image._session
    session2 = client2.transport.get_docker_image._session
    assert session1 != session2
    session1 = client1.transport.list_maven_artifacts._session
    session2 = client2.transport.list_maven_artifacts._session
    assert session1 != session2
    session1 = client1.transport.get_maven_artifact._session
    session2 = client2.transport.get_maven_artifact._session
    assert session1 != session2
    session1 = client1.transport.list_npm_packages._session
    session2 = client2.transport.list_npm_packages._session
    assert session1 != session2
    session1 = client1.transport.get_npm_package._session
    session2 = client2.transport.get_npm_package._session
    assert session1 != session2
    session1 = client1.transport.list_python_packages._session
    session2 = client2.transport.list_python_packages._session
    assert session1 != session2
    session1 = client1.transport.get_python_package._session
    session2 = client2.transport.get_python_package._session
    assert session1 != session2
    session1 = client1.transport.import_apt_artifacts._session
    session2 = client2.transport.import_apt_artifacts._session
    assert session1 != session2
    session1 = client1.transport.import_yum_artifacts._session
    session2 = client2.transport.import_yum_artifacts._session
    assert session1 != session2
    session1 = client1.transport.list_repositories._session
    session2 = client2.transport.list_repositories._session
    assert session1 != session2
    session1 = client1.transport.get_repository._session
    session2 = client2.transport.get_repository._session
    assert session1 != session2
    session1 = client1.transport.create_repository._session
    session2 = client2.transport.create_repository._session
    assert session1 != session2
    session1 = client1.transport.update_repository._session
    session2 = client2.transport.update_repository._session
    assert session1 != session2
    session1 = client1.transport.delete_repository._session
    session2 = client2.transport.delete_repository._session
    assert session1 != session2
    session1 = client1.transport.list_packages._session
    session2 = client2.transport.list_packages._session
    assert session1 != session2
    session1 = client1.transport.get_package._session
    session2 = client2.transport.get_package._session
    assert session1 != session2
    session1 = client1.transport.delete_package._session
    session2 = client2.transport.delete_package._session
    assert session1 != session2
    session1 = client1.transport.list_versions._session
    session2 = client2.transport.list_versions._session
    assert session1 != session2
    session1 = client1.transport.get_version._session
    session2 = client2.transport.get_version._session
    assert session1 != session2
    session1 = client1.transport.delete_version._session
    session2 = client2.transport.delete_version._session
    assert session1 != session2
    session1 = client1.transport.list_files._session
    session2 = client2.transport.list_files._session
    assert session1 != session2
    session1 = client1.transport.get_file._session
    session2 = client2.transport.get_file._session
    assert session1 != session2
    session1 = client1.transport.list_tags._session
    session2 = client2.transport.list_tags._session
    assert session1 != session2
    session1 = client1.transport.get_tag._session
    session2 = client2.transport.get_tag._session
    assert session1 != session2
    session1 = client1.transport.create_tag._session
    session2 = client2.transport.create_tag._session
    assert session1 != session2
    session1 = client1.transport.update_tag._session
    session2 = client2.transport.update_tag._session
    assert session1 != session2
    session1 = client1.transport.delete_tag._session
    session2 = client2.transport.delete_tag._session
    assert session1 != session2
    session1 = client1.transport.set_iam_policy._session
    session2 = client2.transport.set_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.get_iam_policy._session
    session2 = client2.transport.get_iam_policy._session
    assert session1 != session2
    session1 = client1.transport.test_iam_permissions._session
    session2 = client2.transport.test_iam_permissions._session
    assert session1 != session2
    session1 = client1.transport.get_project_settings._session
    session2 = client2.transport.get_project_settings._session
    assert session1 != session2
    session1 = client1.transport.update_project_settings._session
    session2 = client2.transport.update_project_settings._session
    assert session1 != session2
    session1 = client1.transport.get_vpcsc_config._session
    session2 = client2.transport.get_vpcsc_config._session
    assert session1 != session2
    session1 = client1.transport.update_vpcsc_config._session
    session2 = client2.transport.update_vpcsc_config._session
    assert session1 != session2


def test_artifact_registry_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ArtifactRegistryGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_artifact_registry_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ArtifactRegistryGrpcAsyncIOTransport(
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
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
    ],
)
def test_artifact_registry_transport_channel_mtls_with_client_cert_source(
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
        transports.ArtifactRegistryGrpcTransport,
        transports.ArtifactRegistryGrpcAsyncIOTransport,
    ],
)
def test_artifact_registry_transport_channel_mtls_with_adc(transport_class):
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


def test_artifact_registry_grpc_lro_client():
    client = ArtifactRegistryClient(
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


def test_artifact_registry_grpc_lro_async_client():
    client = ArtifactRegistryAsyncClient(
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


def test_apt_artifact_path():
    project = "squid"
    location = "clam"
    repository = "whelk"
    apt_artifact = "octopus"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/aptArtifacts/{apt_artifact}".format(
        project=project,
        location=location,
        repository=repository,
        apt_artifact=apt_artifact,
    )
    actual = ArtifactRegistryClient.apt_artifact_path(
        project, location, repository, apt_artifact
    )
    assert expected == actual


def test_parse_apt_artifact_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "repository": "cuttlefish",
        "apt_artifact": "mussel",
    }
    path = ArtifactRegistryClient.apt_artifact_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_apt_artifact_path(path)
    assert expected == actual


def test_docker_image_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    docker_image = "abalone"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/dockerImages/{docker_image}".format(
        project=project,
        location=location,
        repository=repository,
        docker_image=docker_image,
    )
    actual = ArtifactRegistryClient.docker_image_path(
        project, location, repository, docker_image
    )
    assert expected == actual


def test_parse_docker_image_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "repository": "whelk",
        "docker_image": "octopus",
    }
    path = ArtifactRegistryClient.docker_image_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_docker_image_path(path)
    assert expected == actual


def test_file_path():
    project = "oyster"
    location = "nudibranch"
    repository = "cuttlefish"
    file = "mussel"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/files/{file}".format(
        project=project,
        location=location,
        repository=repository,
        file=file,
    )
    actual = ArtifactRegistryClient.file_path(project, location, repository, file)
    assert expected == actual


def test_parse_file_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "repository": "scallop",
        "file": "abalone",
    }
    path = ArtifactRegistryClient.file_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_file_path(path)
    assert expected == actual


def test_maven_artifact_path():
    project = "squid"
    location = "clam"
    repository = "whelk"
    maven_artifact = "octopus"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/mavenArtifacts/{maven_artifact}".format(
        project=project,
        location=location,
        repository=repository,
        maven_artifact=maven_artifact,
    )
    actual = ArtifactRegistryClient.maven_artifact_path(
        project, location, repository, maven_artifact
    )
    assert expected == actual


def test_parse_maven_artifact_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "repository": "cuttlefish",
        "maven_artifact": "mussel",
    }
    path = ArtifactRegistryClient.maven_artifact_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_maven_artifact_path(path)
    assert expected == actual


def test_npm_package_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    npm_package = "abalone"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/npmPackages/{npm_package}".format(
        project=project,
        location=location,
        repository=repository,
        npm_package=npm_package,
    )
    actual = ArtifactRegistryClient.npm_package_path(
        project, location, repository, npm_package
    )
    assert expected == actual


def test_parse_npm_package_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "repository": "whelk",
        "npm_package": "octopus",
    }
    path = ArtifactRegistryClient.npm_package_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_npm_package_path(path)
    assert expected == actual


def test_package_path():
    project = "oyster"
    location = "nudibranch"
    repository = "cuttlefish"
    package = "mussel"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/packages/{package}".format(
        project=project,
        location=location,
        repository=repository,
        package=package,
    )
    actual = ArtifactRegistryClient.package_path(project, location, repository, package)
    assert expected == actual


def test_parse_package_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "repository": "scallop",
        "package": "abalone",
    }
    path = ArtifactRegistryClient.package_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_package_path(path)
    assert expected == actual


def test_project_settings_path():
    project = "squid"
    expected = "projects/{project}/projectSettings".format(
        project=project,
    )
    actual = ArtifactRegistryClient.project_settings_path(project)
    assert expected == actual


def test_parse_project_settings_path():
    expected = {
        "project": "clam",
    }
    path = ArtifactRegistryClient.project_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_project_settings_path(path)
    assert expected == actual


def test_python_package_path():
    project = "whelk"
    location = "octopus"
    repository = "oyster"
    python_package = "nudibranch"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/pythonPackages/{python_package}".format(
        project=project,
        location=location,
        repository=repository,
        python_package=python_package,
    )
    actual = ArtifactRegistryClient.python_package_path(
        project, location, repository, python_package
    )
    assert expected == actual


def test_parse_python_package_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "repository": "winkle",
        "python_package": "nautilus",
    }
    path = ArtifactRegistryClient.python_package_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_python_package_path(path)
    assert expected == actual


def test_repository_path():
    project = "scallop"
    location = "abalone"
    repository = "squid"
    expected = (
        "projects/{project}/locations/{location}/repositories/{repository}".format(
            project=project,
            location=location,
            repository=repository,
        )
    )
    actual = ArtifactRegistryClient.repository_path(project, location, repository)
    assert expected == actual


def test_parse_repository_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "repository": "octopus",
    }
    path = ArtifactRegistryClient.repository_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_repository_path(path)
    assert expected == actual


def test_tag_path():
    project = "oyster"
    location = "nudibranch"
    repository = "cuttlefish"
    package = "mussel"
    tag = "winkle"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/packages/{package}/tags/{tag}".format(
        project=project,
        location=location,
        repository=repository,
        package=package,
        tag=tag,
    )
    actual = ArtifactRegistryClient.tag_path(
        project, location, repository, package, tag
    )
    assert expected == actual


def test_parse_tag_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "repository": "abalone",
        "package": "squid",
        "tag": "clam",
    }
    path = ArtifactRegistryClient.tag_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_tag_path(path)
    assert expected == actual


def test_version_path():
    project = "whelk"
    location = "octopus"
    repository = "oyster"
    package = "nudibranch"
    version = "cuttlefish"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/packages/{package}/versions/{version}".format(
        project=project,
        location=location,
        repository=repository,
        package=package,
        version=version,
    )
    actual = ArtifactRegistryClient.version_path(
        project, location, repository, package, version
    )
    assert expected == actual


def test_parse_version_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "repository": "nautilus",
        "package": "scallop",
        "version": "abalone",
    }
    path = ArtifactRegistryClient.version_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_version_path(path)
    assert expected == actual


def test_vpcsc_config_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}/vpcscConfig".format(
        project=project,
        location=location,
    )
    actual = ArtifactRegistryClient.vpcsc_config_path(project, location)
    assert expected == actual


def test_parse_vpcsc_config_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = ArtifactRegistryClient.vpcsc_config_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_vpcsc_config_path(path)
    assert expected == actual


def test_yum_artifact_path():
    project = "oyster"
    location = "nudibranch"
    repository = "cuttlefish"
    yum_artifact = "mussel"
    expected = "projects/{project}/locations/{location}/repositories/{repository}/yumArtifacts/{yum_artifact}".format(
        project=project,
        location=location,
        repository=repository,
        yum_artifact=yum_artifact,
    )
    actual = ArtifactRegistryClient.yum_artifact_path(
        project, location, repository, yum_artifact
    )
    assert expected == actual


def test_parse_yum_artifact_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "repository": "scallop",
        "yum_artifact": "abalone",
    }
    path = ArtifactRegistryClient.yum_artifact_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_yum_artifact_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ArtifactRegistryClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = ArtifactRegistryClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ArtifactRegistryClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = ArtifactRegistryClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ArtifactRegistryClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = ArtifactRegistryClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ArtifactRegistryClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = ArtifactRegistryClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ArtifactRegistryClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = ArtifactRegistryClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ArtifactRegistryTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ArtifactRegistryClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ArtifactRegistryTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ArtifactRegistryClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryClient(
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


def test_get_operation(transport: str = "grpc"):
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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


def test_list_locations(transport: str = "grpc"):
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryClient(
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
    client = ArtifactRegistryAsyncClient(
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
        client = ArtifactRegistryClient(
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
        client = ArtifactRegistryClient(
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
        (ArtifactRegistryClient, transports.ArtifactRegistryGrpcTransport),
        (ArtifactRegistryAsyncClient, transports.ArtifactRegistryGrpcAsyncIOTransport),
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
