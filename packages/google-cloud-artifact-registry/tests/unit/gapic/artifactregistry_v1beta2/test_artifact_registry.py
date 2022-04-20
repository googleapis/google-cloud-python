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
import math
import os

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
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
import mock
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.artifactregistry_v1beta2.services.artifact_registry import (
    ArtifactRegistryAsyncClient,
    ArtifactRegistryClient,
    pagers,
    transports,
)
from google.cloud.artifactregistry_v1beta2.types import apt_artifact, file, package
from google.cloud.artifactregistry_v1beta2.types import repository as gda_repository
from google.cloud.artifactregistry_v1beta2.types import repository
from google.cloud.artifactregistry_v1beta2.types import service, settings
from google.cloud.artifactregistry_v1beta2.types import tag
from google.cloud.artifactregistry_v1beta2.types import tag as gda_tag
from google.cloud.artifactregistry_v1beta2.types import version, yum_artifact


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

        assert client.transport._host == ("artifactregistry.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ArtifactRegistryGrpcTransport, "grpc"),
        (transports.ArtifactRegistryGrpcAsyncIOTransport, "grpc_asyncio"),
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

        assert client.transport._host == ("artifactregistry.googleapis.com:443")


def test_artifact_registry_client_get_transport_class():
    transport = ArtifactRegistryClient.get_transport_class()
    available_transports = [
        transports.ArtifactRegistryGrpcTransport,
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
        )


def test_artifact_registry_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.artifactregistry_v1beta2.services.artifact_registry.transports.ArtifactRegistryGrpcTransport.__init__"
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_apt_artifacts_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = apt_artifact.ImportAptArtifactsRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_yum_artifacts_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = yum_artifact.ImportYumArtifactsRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_repositories_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.ListRepositoriesRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

        results = [i for i in pager]
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
        async for page_ in (
            await client.list_repositories(request={})
        ).pages:  # pragma: no branch
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
            maven_config=repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            ),
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.GetRepositoryRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.CreateRepositoryRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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
            maven_config=gda_repository.Repository.MavenRepositoryConfig(
                allow_snapshot_overwrites=True
            ),
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

    request.repository.name = "repository.name/value"

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
        "repository.name=repository.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_repository.UpdateRepositoryRequest()

    request.repository.name = "repository.name/value"

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
        "repository.name=repository.name/value",
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_repository_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = repository.DeleteRepositoryRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_packages_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.ListPackagesRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

        results = [i for i in pager]
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
        async for page_ in (
            await client.list_packages(request={})
        ).pages:  # pragma: no branch
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.GetPackageRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_package_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = package.DeletePackageRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_versions_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.ListVersionsRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

        results = [i for i in pager]
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
        async for page_ in (
            await client.list_versions(request={})
        ).pages:  # pragma: no branch
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_version_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.GetVersionRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_version_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = version.DeleteVersionRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_files_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.ListFilesRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

        results = [i for i in pager]
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
        async for page_ in (
            await client.list_files(request={})
        ).pages:  # pragma: no branch
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_file_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = file.GetFileRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tags_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.ListTagsRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

        results = [i for i in pager]
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
        async for page_ in (
            await client.list_tags(request={})
        ).pages:  # pragma: no branch
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tag_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.GetTagRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.parent = "parent/value"

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
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_tag_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.CreateTagRequest()

    request.parent = "parent/value"

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
        "parent=parent/value",
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

    request.tag.name = "tag.name/value"

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
        "tag.name=tag.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_tag_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gda_tag.UpdateTagRequest()

    request.tag.name = "tag.name/value"

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
        "tag.name=tag.name/value",
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_tag_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = tag.DeleteTagRequest()

    request.name = "name/value"

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
        "name=name/value",
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryAsyncClient(
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
    client = ArtifactRegistryAsyncClient(
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

    request.name = "name/value"

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
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_project_settings_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.GetProjectSettingsRequest()

    request.name = "name/value"

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
        "name=name/value",
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

    request.project_settings.name = "project_settings.name/value"

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
        "project_settings.name=project_settings.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_project_settings_field_headers_async():
    client = ArtifactRegistryAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = settings.UpdateProjectSettingsRequest()

    request.project_settings.name = "project_settings.name/value"

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
        "project_settings.name=project_settings.name/value",
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
        "google.cloud.artifactregistry_v1beta2.services.artifact_registry.transports.ArtifactRegistryTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ArtifactRegistryTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
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
        "google.cloud.artifactregistry_v1beta2.services.artifact_registry.transports.ArtifactRegistryTransport._prep_wrapped_messages"
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
        "google.cloud.artifactregistry_v1beta2.services.artifact_registry.transports.ArtifactRegistryTransport._prep_wrapped_messages"
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


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
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
    assert client.transport._host == ("artifactregistry.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
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
    assert client.transport._host == ("artifactregistry.googleapis.com:8000")


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


def test_file_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    file = "abalone"
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
        "project": "squid",
        "location": "clam",
        "repository": "whelk",
        "file": "octopus",
    }
    path = ArtifactRegistryClient.file_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_file_path(path)
    assert expected == actual


def test_project_settings_path():
    project = "oyster"
    expected = "projects/{project}/projectSettings".format(
        project=project,
    )
    actual = ArtifactRegistryClient.project_settings_path(project)
    assert expected == actual


def test_parse_project_settings_path():
    expected = {
        "project": "nudibranch",
    }
    path = ArtifactRegistryClient.project_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_project_settings_path(path)
    assert expected == actual


def test_repository_path():
    project = "cuttlefish"
    location = "mussel"
    repository = "winkle"
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
        "project": "nautilus",
        "location": "scallop",
        "repository": "abalone",
    }
    path = ArtifactRegistryClient.repository_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_repository_path(path)
    assert expected == actual


def test_tag_path():
    project = "squid"
    location = "clam"
    repository = "whelk"
    package = "octopus"
    tag = "oyster"
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
        "project": "nudibranch",
        "location": "cuttlefish",
        "repository": "mussel",
        "package": "winkle",
        "tag": "nautilus",
    }
    path = ArtifactRegistryClient.tag_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_tag_path(path)
    assert expected == actual


def test_version_path():
    project = "scallop"
    location = "abalone"
    repository = "squid"
    package = "clam"
    version = "whelk"
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
        "project": "octopus",
        "location": "oyster",
        "repository": "nudibranch",
        "package": "cuttlefish",
        "version": "mussel",
    }
    path = ArtifactRegistryClient.version_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_version_path(path)
    assert expected == actual


def test_yum_artifact_path():
    project = "winkle"
    location = "nautilus"
    repository = "scallop"
    yum_artifact = "abalone"
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
        "project": "squid",
        "location": "clam",
        "repository": "whelk",
        "yum_artifact": "octopus",
    }
    path = ArtifactRegistryClient.yum_artifact_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_yum_artifact_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ArtifactRegistryClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = ArtifactRegistryClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ArtifactRegistryClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = ArtifactRegistryClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ArtifactRegistryClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = ArtifactRegistryClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ArtifactRegistryClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = ArtifactRegistryClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ArtifactRegistryClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ArtifactRegistryClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
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


def test_transport_close():
    transports = {
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
            )
