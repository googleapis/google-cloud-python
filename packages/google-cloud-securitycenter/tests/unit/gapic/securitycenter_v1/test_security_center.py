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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.securitycenter_v1.services.security_center import (
    SecurityCenterAsyncClient,
    SecurityCenterClient,
    pagers,
    transports,
)
from google.cloud.securitycenter_v1.types import (
    access,
    bigquery_export,
    compliance,
    connection,
    contact_details,
    container,
    exfiltration,
)
from google.cloud.securitycenter_v1.types import (
    iam_binding,
    indicator,
    kubernetes,
    label,
    mitre_attack,
)
from google.cloud.securitycenter_v1.types import process, run_asset_discovery_response
from google.cloud.securitycenter_v1.types import external_system as gcs_external_system
from google.cloud.securitycenter_v1.types import (
    notification_config as gcs_notification_config,
)
from google.cloud.securitycenter_v1.types import (
    organization_settings as gcs_organization_settings,
)
from google.cloud.securitycenter_v1.types import security_marks as gcs_security_marks
from google.cloud.securitycenter_v1.types import external_system
from google.cloud.securitycenter_v1.types import file
from google.cloud.securitycenter_v1.types import finding
from google.cloud.securitycenter_v1.types import finding as gcs_finding
from google.cloud.securitycenter_v1.types import mute_config
from google.cloud.securitycenter_v1.types import mute_config as gcs_mute_config
from google.cloud.securitycenter_v1.types import notification_config
from google.cloud.securitycenter_v1.types import organization_settings
from google.cloud.securitycenter_v1.types import security_marks
from google.cloud.securitycenter_v1.types import securitycenter_service
from google.cloud.securitycenter_v1.types import source
from google.cloud.securitycenter_v1.types import source as gcs_source
from google.cloud.securitycenter_v1.types import vulnerability


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

    assert SecurityCenterClient._get_default_mtls_endpoint(None) is None
    assert (
        SecurityCenterClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SecurityCenterClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SecurityCenterClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SecurityCenterClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SecurityCenterClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (SecurityCenterClient, "grpc"),
        (SecurityCenterAsyncClient, "grpc_asyncio"),
    ],
)
def test_security_center_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("securitycenter.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.SecurityCenterGrpcTransport, "grpc"),
        (transports.SecurityCenterGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_security_center_client_service_account_always_use_jwt(
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
        (SecurityCenterClient, "grpc"),
        (SecurityCenterAsyncClient, "grpc_asyncio"),
    ],
)
def test_security_center_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("securitycenter.googleapis.com:443")


def test_security_center_client_get_transport_class():
    transport = SecurityCenterClient.get_transport_class()
    available_transports = [
        transports.SecurityCenterGrpcTransport,
    ]
    assert transport in available_transports

    transport = SecurityCenterClient.get_transport_class("grpc")
    assert transport == transports.SecurityCenterGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (SecurityCenterClient, transports.SecurityCenterGrpcTransport, "grpc"),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    SecurityCenterClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterClient),
)
@mock.patch.object(
    SecurityCenterAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterAsyncClient),
)
def test_security_center_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SecurityCenterClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SecurityCenterClient, "get_transport_class") as gtc:
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
        (SecurityCenterClient, transports.SecurityCenterGrpcTransport, "grpc", "true"),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (SecurityCenterClient, transports.SecurityCenterGrpcTransport, "grpc", "false"),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    SecurityCenterClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterClient),
)
@mock.patch.object(
    SecurityCenterAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_security_center_client_mtls_env_auto(
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
    "client_class", [SecurityCenterClient, SecurityCenterAsyncClient]
)
@mock.patch.object(
    SecurityCenterClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterClient),
)
@mock.patch.object(
    SecurityCenterAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(SecurityCenterAsyncClient),
)
def test_security_center_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (SecurityCenterClient, transports.SecurityCenterGrpcTransport, "grpc"),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_security_center_client_client_options_scopes(
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
            SecurityCenterClient,
            transports.SecurityCenterGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_security_center_client_client_options_credentials_file(
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


def test_security_center_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.securitycenter_v1.services.security_center.transports.SecurityCenterGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = SecurityCenterClient(
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
            SecurityCenterClient,
            transports.SecurityCenterGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            SecurityCenterAsyncClient,
            transports.SecurityCenterGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_security_center_client_create_channel_credentials_file(
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
            "securitycenter.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="securitycenter.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.BulkMuteFindingsRequest,
        dict,
    ],
)
def test_bulk_mute_findings(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.bulk_mute_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.BulkMuteFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_bulk_mute_findings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        client.bulk_mute_findings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.BulkMuteFindingsRequest()


@pytest.mark.asyncio
async def test_bulk_mute_findings_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.BulkMuteFindingsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.bulk_mute_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.BulkMuteFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_bulk_mute_findings_async_from_dict():
    await test_bulk_mute_findings_async(request_type=dict)


def test_bulk_mute_findings_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.BulkMuteFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.bulk_mute_findings(request)

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
async def test_bulk_mute_findings_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.BulkMuteFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.bulk_mute_findings(request)

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


def test_bulk_mute_findings_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.bulk_mute_findings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_bulk_mute_findings_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.bulk_mute_findings(
            securitycenter_service.BulkMuteFindingsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_bulk_mute_findings_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.bulk_mute_findings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.bulk_mute_findings(
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
async def test_bulk_mute_findings_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.bulk_mute_findings(
            securitycenter_service.BulkMuteFindingsRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.CreateSourceRequest,
        dict,
    ],
)
def test_create_source(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            canonical_name="canonical_name_value",
        )
        response = client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


def test_create_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        client.create_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateSourceRequest()


@pytest.mark.asyncio
async def test_create_source_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.CreateSourceRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_source.Source(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                canonical_name="canonical_name_value",
            )
        )
        response = await client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


@pytest.mark.asyncio
async def test_create_source_async_from_dict():
    await test_create_source_async(request_type=dict)


def test_create_source_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateSourceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        call.return_value = gcs_source.Source()
        client.create_source(request)

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
async def test_create_source_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateSourceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_source.Source())
        await client.create_source(request)

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


def test_create_source_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_source(
            parent="parent_value",
            source=gcs_source.Source(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = gcs_source.Source(name="name_value")
        assert arg == mock_val


def test_create_source_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_source(
            securitycenter_service.CreateSourceRequest(),
            parent="parent_value",
            source=gcs_source.Source(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_source_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_source.Source())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_source(
            parent="parent_value",
            source=gcs_source.Source(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = gcs_source.Source(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_source_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_source(
            securitycenter_service.CreateSourceRequest(),
            parent="parent_value",
            source=gcs_source.Source(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.CreateFindingRequest,
        dict,
    ],
)
def test_create_finding(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding(
            name="name_value",
            parent="parent_value",
            resource_name="resource_name_value",
            state=gcs_finding.Finding.State.ACTIVE,
            category="category_value",
            external_uri="external_uri_value",
            severity=gcs_finding.Finding.Severity.CRITICAL,
            canonical_name="canonical_name_value",
            mute=gcs_finding.Finding.Mute.MUTED,
            finding_class=gcs_finding.Finding.FindingClass.THREAT,
            mute_initiator="mute_initiator_value",
            description="description_value",
            next_steps="next_steps_value",
        )
        response = client.create_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == gcs_finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == gcs_finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == gcs_finding.Finding.Mute.MUTED
    assert response.finding_class == gcs_finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


def test_create_finding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        client.create_finding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateFindingRequest()


@pytest.mark.asyncio
async def test_create_finding_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.CreateFindingRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_finding.Finding(
                name="name_value",
                parent="parent_value",
                resource_name="resource_name_value",
                state=gcs_finding.Finding.State.ACTIVE,
                category="category_value",
                external_uri="external_uri_value",
                severity=gcs_finding.Finding.Severity.CRITICAL,
                canonical_name="canonical_name_value",
                mute=gcs_finding.Finding.Mute.MUTED,
                finding_class=gcs_finding.Finding.FindingClass.THREAT,
                mute_initiator="mute_initiator_value",
                description="description_value",
                next_steps="next_steps_value",
            )
        )
        response = await client.create_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == gcs_finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == gcs_finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == gcs_finding.Finding.Mute.MUTED
    assert response.finding_class == gcs_finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


@pytest.mark.asyncio
async def test_create_finding_async_from_dict():
    await test_create_finding_async(request_type=dict)


def test_create_finding_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateFindingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        call.return_value = gcs_finding.Finding()
        client.create_finding(request)

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
async def test_create_finding_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateFindingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_finding.Finding())
        await client.create_finding(request)

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


def test_create_finding_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_finding(
            parent="parent_value",
            finding_id="finding_id_value",
            finding=gcs_finding.Finding(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].finding_id
        mock_val = "finding_id_value"
        assert arg == mock_val
        arg = args[0].finding
        mock_val = gcs_finding.Finding(name="name_value")
        assert arg == mock_val


def test_create_finding_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_finding(
            securitycenter_service.CreateFindingRequest(),
            parent="parent_value",
            finding_id="finding_id_value",
            finding=gcs_finding.Finding(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_finding_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_finding.Finding())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_finding(
            parent="parent_value",
            finding_id="finding_id_value",
            finding=gcs_finding.Finding(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].finding_id
        mock_val = "finding_id_value"
        assert arg == mock_val
        arg = args[0].finding
        mock_val = gcs_finding.Finding(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_finding_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_finding(
            securitycenter_service.CreateFindingRequest(),
            parent="parent_value",
            finding_id="finding_id_value",
            finding=gcs_finding.Finding(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.CreateMuteConfigRequest,
        dict,
    ],
)
def test_create_mute_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            filter="filter_value",
            most_recent_editor="most_recent_editor_value",
        )
        response = client.create_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


def test_create_mute_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        client.create_mute_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateMuteConfigRequest()


@pytest.mark.asyncio
async def test_create_mute_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.CreateMuteConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                filter="filter_value",
                most_recent_editor="most_recent_editor_value",
            )
        )
        response = await client.create_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


@pytest.mark.asyncio
async def test_create_mute_config_async_from_dict():
    await test_create_mute_config_async(request_type=dict)


def test_create_mute_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateMuteConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        call.return_value = gcs_mute_config.MuteConfig()
        client.create_mute_config(request)

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
async def test_create_mute_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateMuteConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig()
        )
        await client.create_mute_config(request)

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


def test_create_mute_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_mute_config(
            parent="parent_value",
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            mute_config_id="mute_config_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].mute_config
        mock_val = gcs_mute_config.MuteConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].mute_config_id
        mock_val = "mute_config_id_value"
        assert arg == mock_val


def test_create_mute_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_mute_config(
            securitycenter_service.CreateMuteConfigRequest(),
            parent="parent_value",
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            mute_config_id="mute_config_id_value",
        )


@pytest.mark.asyncio
async def test_create_mute_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_mute_config(
            parent="parent_value",
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            mute_config_id="mute_config_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].mute_config
        mock_val = gcs_mute_config.MuteConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].mute_config_id
        mock_val = "mute_config_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_mute_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_mute_config(
            securitycenter_service.CreateMuteConfigRequest(),
            parent="parent_value",
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            mute_config_id="mute_config_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.CreateNotificationConfigRequest,
        dict,
    ],
)
def test_create_notification_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig(
            name="name_value",
            description="description_value",
            pubsub_topic="pubsub_topic_value",
            service_account="service_account_value",
            streaming_config=gcs_notification_config.NotificationConfig.StreamingConfig(
                filter="filter_value"
            ),
        )
        response = client.create_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


def test_create_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        client.create_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateNotificationConfigRequest()


@pytest.mark.asyncio
async def test_create_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.CreateNotificationConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig(
                name="name_value",
                description="description_value",
                pubsub_topic="pubsub_topic_value",
                service_account="service_account_value",
            )
        )
        response = await client.create_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_create_notification_config_async_from_dict():
    await test_create_notification_config_async(request_type=dict)


def test_create_notification_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateNotificationConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        call.return_value = gcs_notification_config.NotificationConfig()
        client.create_notification_config(request)

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
async def test_create_notification_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateNotificationConfigRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig()
        )
        await client.create_notification_config(request)

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


def test_create_notification_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_notification_config(
            parent="parent_value",
            config_id="config_id_value",
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].config_id
        mock_val = "config_id_value"
        assert arg == mock_val
        arg = args[0].notification_config
        mock_val = gcs_notification_config.NotificationConfig(name="name_value")
        assert arg == mock_val


def test_create_notification_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_notification_config(
            securitycenter_service.CreateNotificationConfigRequest(),
            parent="parent_value",
            config_id="config_id_value",
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_notification_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_notification_config(
            parent="parent_value",
            config_id="config_id_value",
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].config_id
        mock_val = "config_id_value"
        assert arg == mock_val
        arg = args[0].notification_config
        mock_val = gcs_notification_config.NotificationConfig(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_notification_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_notification_config(
            securitycenter_service.CreateNotificationConfigRequest(),
            parent="parent_value",
            config_id="config_id_value",
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.DeleteMuteConfigRequest,
        dict,
    ],
)
def test_delete_mute_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_mute_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        client.delete_mute_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteMuteConfigRequest()


@pytest.mark.asyncio
async def test_delete_mute_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.DeleteMuteConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_mute_config_async_from_dict():
    await test_delete_mute_config_async(request_type=dict)


def test_delete_mute_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteMuteConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        call.return_value = None
        client.delete_mute_config(request)

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
async def test_delete_mute_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteMuteConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_mute_config(request)

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


def test_delete_mute_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_mute_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_mute_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_mute_config(
            securitycenter_service.DeleteMuteConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_mute_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_mute_config(
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
async def test_delete_mute_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_mute_config(
            securitycenter_service.DeleteMuteConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.DeleteNotificationConfigRequest,
        dict,
    ],
)
def test_delete_notification_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        client.delete_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteNotificationConfigRequest()


@pytest.mark.asyncio
async def test_delete_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.DeleteNotificationConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_notification_config_async_from_dict():
    await test_delete_notification_config_async(request_type=dict)


def test_delete_notification_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteNotificationConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        call.return_value = None
        client.delete_notification_config(request)

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
async def test_delete_notification_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteNotificationConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_notification_config(request)

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


def test_delete_notification_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_notification_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_notification_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_notification_config(
            securitycenter_service.DeleteNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_notification_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_notification_config(
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
async def test_delete_notification_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_notification_config(
            securitycenter_service.DeleteNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GetBigQueryExportRequest,
        dict,
    ],
)
def test_get_big_query_export(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport(
            name="name_value",
            description="description_value",
            filter="filter_value",
            dataset="dataset_value",
            most_recent_editor="most_recent_editor_value",
            principal="principal_value",
        )
        response = client.get_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


def test_get_big_query_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        client.get_big_query_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetBigQueryExportRequest()


@pytest.mark.asyncio
async def test_get_big_query_export_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GetBigQueryExportRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport(
                name="name_value",
                description="description_value",
                filter="filter_value",
                dataset="dataset_value",
                most_recent_editor="most_recent_editor_value",
                principal="principal_value",
            )
        )
        response = await client.get_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


@pytest.mark.asyncio
async def test_get_big_query_export_async_from_dict():
    await test_get_big_query_export_async(request_type=dict)


def test_get_big_query_export_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetBigQueryExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        call.return_value = bigquery_export.BigQueryExport()
        client.get_big_query_export(request)

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
async def test_get_big_query_export_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetBigQueryExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        await client.get_big_query_export(request)

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


def test_get_big_query_export_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_big_query_export(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_big_query_export_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_big_query_export(
            securitycenter_service.GetBigQueryExportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_big_query_export_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_big_query_export(
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
async def test_get_big_query_export_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_big_query_export(
            securitycenter_service.GetBigQueryExportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterAsyncClient(
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
        securitycenter_service.GetMuteConfigRequest,
        dict,
    ],
)
def test_get_mute_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mute_config.MuteConfig(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            filter="filter_value",
            most_recent_editor="most_recent_editor_value",
        )
        response = client.get_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


def test_get_mute_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        client.get_mute_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetMuteConfigRequest()


@pytest.mark.asyncio
async def test_get_mute_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GetMuteConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mute_config.MuteConfig(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                filter="filter_value",
                most_recent_editor="most_recent_editor_value",
            )
        )
        response = await client.get_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


@pytest.mark.asyncio
async def test_get_mute_config_async_from_dict():
    await test_get_mute_config_async(request_type=dict)


def test_get_mute_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetMuteConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        call.return_value = mute_config.MuteConfig()
        client.get_mute_config(request)

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
async def test_get_mute_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetMuteConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mute_config.MuteConfig()
        )
        await client.get_mute_config(request)

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


def test_get_mute_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mute_config.MuteConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_mute_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_mute_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_mute_config(
            securitycenter_service.GetMuteConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_mute_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_mute_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = mute_config.MuteConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            mute_config.MuteConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_mute_config(
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
async def test_get_mute_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_mute_config(
            securitycenter_service.GetMuteConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GetNotificationConfigRequest,
        dict,
    ],
)
def test_get_notification_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_config.NotificationConfig(
            name="name_value",
            description="description_value",
            pubsub_topic="pubsub_topic_value",
            service_account="service_account_value",
            streaming_config=notification_config.NotificationConfig.StreamingConfig(
                filter="filter_value"
            ),
        )
        response = client.get_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


def test_get_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        client.get_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetNotificationConfigRequest()


@pytest.mark.asyncio
async def test_get_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GetNotificationConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_config.NotificationConfig(
                name="name_value",
                description="description_value",
                pubsub_topic="pubsub_topic_value",
                service_account="service_account_value",
            )
        )
        response = await client.get_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_notification_config_async_from_dict():
    await test_get_notification_config_async(request_type=dict)


def test_get_notification_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetNotificationConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        call.return_value = notification_config.NotificationConfig()
        client.get_notification_config(request)

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
async def test_get_notification_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetNotificationConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_config.NotificationConfig()
        )
        await client.get_notification_config(request)

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


def test_get_notification_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_config.NotificationConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_notification_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_notification_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_notification_config(
            securitycenter_service.GetNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_notification_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_config.NotificationConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_config.NotificationConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_notification_config(
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
async def test_get_notification_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_notification_config(
            securitycenter_service.GetNotificationConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GetOrganizationSettingsRequest,
        dict,
    ],
)
def test_get_organization_settings(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = organization_settings.OrganizationSettings(
            name="name_value",
            enable_asset_discovery=True,
        )
        response = client.get_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetOrganizationSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, organization_settings.OrganizationSettings)
    assert response.name == "name_value"
    assert response.enable_asset_discovery is True


def test_get_organization_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        client.get_organization_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetOrganizationSettingsRequest()


@pytest.mark.asyncio
async def test_get_organization_settings_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GetOrganizationSettingsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            organization_settings.OrganizationSettings(
                name="name_value",
                enable_asset_discovery=True,
            )
        )
        response = await client.get_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetOrganizationSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, organization_settings.OrganizationSettings)
    assert response.name == "name_value"
    assert response.enable_asset_discovery is True


@pytest.mark.asyncio
async def test_get_organization_settings_async_from_dict():
    await test_get_organization_settings_async(request_type=dict)


def test_get_organization_settings_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetOrganizationSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        call.return_value = organization_settings.OrganizationSettings()
        client.get_organization_settings(request)

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
async def test_get_organization_settings_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetOrganizationSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            organization_settings.OrganizationSettings()
        )
        await client.get_organization_settings(request)

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


def test_get_organization_settings_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = organization_settings.OrganizationSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_organization_settings(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_organization_settings_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_organization_settings(
            securitycenter_service.GetOrganizationSettingsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_organization_settings_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = organization_settings.OrganizationSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            organization_settings.OrganizationSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_organization_settings(
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
async def test_get_organization_settings_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_organization_settings(
            securitycenter_service.GetOrganizationSettingsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GetSourceRequest,
        dict,
    ],
)
def test_get_source(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = source.Source(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            canonical_name="canonical_name_value",
        )
        response = client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


def test_get_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        client.get_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetSourceRequest()


@pytest.mark.asyncio
async def test_get_source_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GetSourceRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            source.Source(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                canonical_name="canonical_name_value",
            )
        )
        response = await client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GetSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


@pytest.mark.asyncio
async def test_get_source_async_from_dict():
    await test_get_source_async(request_type=dict)


def test_get_source_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        call.return_value = source.Source()
        client.get_source(request)

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
async def test_get_source_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GetSourceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(source.Source())
        await client.get_source(request)

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


def test_get_source_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = source.Source()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_source_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_source(
            securitycenter_service.GetSourceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_source_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = source.Source()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(source.Source())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_source(
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
async def test_get_source_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_source(
            securitycenter_service.GetSourceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GroupAssetsRequest,
        dict,
    ],
)
def test_group_assets(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.GroupAssetsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.group_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.GroupAssetsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_group_assets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        client.group_assets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupAssetsRequest()


@pytest.mark.asyncio
async def test_group_assets_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GroupAssetsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.GroupAssetsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.group_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.GroupAssetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_group_assets_async_from_dict():
    await test_group_assets_async(request_type=dict)


def test_group_assets_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GroupAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        call.return_value = securitycenter_service.GroupAssetsResponse()
        client.group_assets(request)

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
async def test_group_assets_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GroupAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.GroupAssetsResponse()
        )
        await client.group_assets(request)

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


def test_group_assets_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.group_assets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, securitycenter_service.GroupResult) for i in results)


def test_group_assets_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.group_assets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_group_assets_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.group_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.group_assets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, securitycenter_service.GroupResult) for i in responses)


@pytest.mark.asyncio
async def test_group_assets_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.group_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupAssetsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.group_assets(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.GroupFindingsRequest,
        dict,
    ],
)
def test_group_findings(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.GroupFindingsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.group_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.GroupFindingsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_group_findings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        client.group_findings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupFindingsRequest()


@pytest.mark.asyncio
async def test_group_findings_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.GroupFindingsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.GroupFindingsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.group_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.GroupFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.GroupFindingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_group_findings_async_from_dict():
    await test_group_findings_async(request_type=dict)


def test_group_findings_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GroupFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        call.return_value = securitycenter_service.GroupFindingsResponse()
        client.group_findings(request)

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
async def test_group_findings_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.GroupFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.GroupFindingsResponse()
        )
        await client.group_findings(request)

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


def test_group_findings_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.GroupFindingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.group_findings(
            parent="parent_value",
            group_by="group_by_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].group_by
        mock_val = "group_by_value"
        assert arg == mock_val


def test_group_findings_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.group_findings(
            securitycenter_service.GroupFindingsRequest(),
            parent="parent_value",
            group_by="group_by_value",
        )


@pytest.mark.asyncio
async def test_group_findings_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.GroupFindingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.GroupFindingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.group_findings(
            parent="parent_value",
            group_by="group_by_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].group_by
        mock_val = "group_by_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_group_findings_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.group_findings(
            securitycenter_service.GroupFindingsRequest(),
            parent="parent_value",
            group_by="group_by_value",
        )


def test_group_findings_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.group_findings(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, securitycenter_service.GroupResult) for i in results)


def test_group_findings_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.group_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.group_findings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_group_findings_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.group_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.group_findings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, securitycenter_service.GroupResult) for i in responses)


@pytest.mark.asyncio
async def test_group_findings_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.group_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[],
                next_page_token="def",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.GroupFindingsResponse(
                group_by_results=[
                    securitycenter_service.GroupResult(),
                    securitycenter_service.GroupResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.group_findings(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListAssetsRequest,
        dict,
    ],
)
def test_list_assets(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListAssetsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_assets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        client.list_assets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListAssetsRequest()


@pytest.mark.asyncio
async def test_list_assets_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListAssetsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListAssetsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_assets_async_from_dict():
    await test_list_assets_async(request_type=dict)


def test_list_assets_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        call.return_value = securitycenter_service.ListAssetsResponse()
        client.list_assets(request)

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
async def test_list_assets_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListAssetsResponse()
        )
        await client.list_assets(request)

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


def test_list_assets_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_assets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, securitycenter_service.ListAssetsResponse.ListAssetsResult)
            for i in results
        )


def test_list_assets_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_assets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_assets_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_assets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, securitycenter_service.ListAssetsResponse.ListAssetsResult)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_assets_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListAssetsResponse(
                list_assets_results=[
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                    securitycenter_service.ListAssetsResponse.ListAssetsResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_assets(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListFindingsRequest,
        dict,
    ],
)
def test_list_findings(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListFindingsResponse(
            next_page_token="next_page_token_value",
            total_size=1086,
        )
        response = client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFindingsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_findings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        client.list_findings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListFindingsRequest()


@pytest.mark.asyncio
async def test_list_findings_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListFindingsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListFindingsResponse(
                next_page_token="next_page_token_value",
                total_size=1086,
            )
        )
        response = await client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFindingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_findings_async_from_dict():
    await test_list_findings_async(request_type=dict)


def test_list_findings_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        call.return_value = securitycenter_service.ListFindingsResponse()
        client.list_findings(request)

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
async def test_list_findings_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListFindingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListFindingsResponse()
        )
        await client.list_findings(request)

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


def test_list_findings_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_findings(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(
                i, securitycenter_service.ListFindingsResponse.ListFindingsResult
            )
            for i in results
        )


def test_list_findings_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_findings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_findings_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_findings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(
                i, securitycenter_service.ListFindingsResponse.ListFindingsResult
            )
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_findings_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[],
                next_page_token="def",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListFindingsResponse(
                list_findings_results=[
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                    securitycenter_service.ListFindingsResponse.ListFindingsResult(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_findings(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListMuteConfigsRequest,
        dict,
    ],
)
def test_list_mute_configs(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListMuteConfigsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_mute_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListMuteConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMuteConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_mute_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        client.list_mute_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListMuteConfigsRequest()


@pytest.mark.asyncio
async def test_list_mute_configs_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListMuteConfigsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListMuteConfigsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_mute_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListMuteConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMuteConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_mute_configs_async_from_dict():
    await test_list_mute_configs_async(request_type=dict)


def test_list_mute_configs_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListMuteConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        call.return_value = securitycenter_service.ListMuteConfigsResponse()
        client.list_mute_configs(request)

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
async def test_list_mute_configs_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListMuteConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListMuteConfigsResponse()
        )
        await client.list_mute_configs(request)

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


def test_list_mute_configs_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListMuteConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_mute_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_mute_configs_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_mute_configs(
            securitycenter_service.ListMuteConfigsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_mute_configs_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListMuteConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListMuteConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_mute_configs(
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
async def test_list_mute_configs_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_mute_configs(
            securitycenter_service.ListMuteConfigsRequest(),
            parent="parent_value",
        )


def test_list_mute_configs_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_mute_configs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, mute_config.MuteConfig) for i in results)


def test_list_mute_configs_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_mute_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_mute_configs_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_mute_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, mute_config.MuteConfig) for i in responses)


@pytest.mark.asyncio
async def test_list_mute_configs_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_mute_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListMuteConfigsResponse(
                mute_configs=[
                    mute_config.MuteConfig(),
                    mute_config.MuteConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_mute_configs(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListNotificationConfigsRequest,
        dict,
    ],
)
def test_list_notification_configs(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListNotificationConfigsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_notification_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListNotificationConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_notification_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        client.list_notification_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListNotificationConfigsRequest()


@pytest.mark.asyncio
async def test_list_notification_configs_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListNotificationConfigsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListNotificationConfigsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_notification_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListNotificationConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_notification_configs_async_from_dict():
    await test_list_notification_configs_async(request_type=dict)


def test_list_notification_configs_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListNotificationConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        call.return_value = securitycenter_service.ListNotificationConfigsResponse()
        client.list_notification_configs(request)

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
async def test_list_notification_configs_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListNotificationConfigsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListNotificationConfigsResponse()
        )
        await client.list_notification_configs(request)

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


def test_list_notification_configs_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListNotificationConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notification_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_notification_configs_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notification_configs(
            securitycenter_service.ListNotificationConfigsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_notification_configs_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListNotificationConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListNotificationConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notification_configs(
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
async def test_list_notification_configs_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notification_configs(
            securitycenter_service.ListNotificationConfigsRequest(),
            parent="parent_value",
        )


def test_list_notification_configs_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_notification_configs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, notification_config.NotificationConfig) for i in results
        )


def test_list_notification_configs_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_notification_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notification_configs_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_notification_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, notification_config.NotificationConfig) for i in responses
        )


@pytest.mark.asyncio
async def test_list_notification_configs_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[],
                next_page_token="def",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListNotificationConfigsResponse(
                notification_configs=[
                    notification_config.NotificationConfig(),
                    notification_config.NotificationConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_notification_configs(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListSourcesRequest,
        dict,
    ],
)
def test_list_sources(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListSourcesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListSourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSourcesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_sources_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        client.list_sources()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListSourcesRequest()


@pytest.mark.asyncio
async def test_list_sources_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListSourcesRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListSourcesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListSourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSourcesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_sources_async_from_dict():
    await test_list_sources_async(request_type=dict)


def test_list_sources_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListSourcesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        call.return_value = securitycenter_service.ListSourcesResponse()
        client.list_sources(request)

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
async def test_list_sources_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListSourcesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListSourcesResponse()
        )
        await client.list_sources(request)

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


def test_list_sources_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListSourcesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_sources(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_sources_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_sources(
            securitycenter_service.ListSourcesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_sources_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListSourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListSourcesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_sources(
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
async def test_list_sources_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_sources(
            securitycenter_service.ListSourcesRequest(),
            parent="parent_value",
        )


def test_list_sources_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                    source.Source(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_sources(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, source.Source) for i in results)


def test_list_sources_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                    source.Source(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_sources(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_sources_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sources), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                    source.Source(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_sources(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, source.Source) for i in responses)


@pytest.mark.asyncio
async def test_list_sources_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sources), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                    source.Source(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListSourcesResponse(
                sources=[
                    source.Source(),
                    source.Source(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_sources(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.RunAssetDiscoveryRequest,
        dict,
    ],
)
def test_run_asset_discovery(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_asset_discovery(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.RunAssetDiscoveryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_asset_discovery_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        client.run_asset_discovery()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.RunAssetDiscoveryRequest()


@pytest.mark.asyncio
async def test_run_asset_discovery_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.RunAssetDiscoveryRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_asset_discovery(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.RunAssetDiscoveryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_asset_discovery_async_from_dict():
    await test_run_asset_discovery_async(request_type=dict)


def test_run_asset_discovery_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.RunAssetDiscoveryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_asset_discovery(request)

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
async def test_run_asset_discovery_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.RunAssetDiscoveryRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.run_asset_discovery(request)

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


def test_run_asset_discovery_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_asset_discovery(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_run_asset_discovery_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_asset_discovery(
            securitycenter_service.RunAssetDiscoveryRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_run_asset_discovery_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_asset_discovery), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_asset_discovery(
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
async def test_run_asset_discovery_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_asset_discovery(
            securitycenter_service.RunAssetDiscoveryRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.SetFindingStateRequest,
        dict,
    ],
)
def test_set_finding_state(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding(
            name="name_value",
            parent="parent_value",
            resource_name="resource_name_value",
            state=finding.Finding.State.ACTIVE,
            category="category_value",
            external_uri="external_uri_value",
            severity=finding.Finding.Severity.CRITICAL,
            canonical_name="canonical_name_value",
            mute=finding.Finding.Mute.MUTED,
            finding_class=finding.Finding.FindingClass.THREAT,
            mute_initiator="mute_initiator_value",
            description="description_value",
            next_steps="next_steps_value",
        )
        response = client.set_finding_state(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetFindingStateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == finding.Finding.Mute.MUTED
    assert response.finding_class == finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


def test_set_finding_state_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        client.set_finding_state()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetFindingStateRequest()


@pytest.mark.asyncio
async def test_set_finding_state_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.SetFindingStateRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            finding.Finding(
                name="name_value",
                parent="parent_value",
                resource_name="resource_name_value",
                state=finding.Finding.State.ACTIVE,
                category="category_value",
                external_uri="external_uri_value",
                severity=finding.Finding.Severity.CRITICAL,
                canonical_name="canonical_name_value",
                mute=finding.Finding.Mute.MUTED,
                finding_class=finding.Finding.FindingClass.THREAT,
                mute_initiator="mute_initiator_value",
                description="description_value",
                next_steps="next_steps_value",
            )
        )
        response = await client.set_finding_state(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetFindingStateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == finding.Finding.Mute.MUTED
    assert response.finding_class == finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


@pytest.mark.asyncio
async def test_set_finding_state_async_from_dict():
    await test_set_finding_state_async(request_type=dict)


def test_set_finding_state_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.SetFindingStateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        call.return_value = finding.Finding()
        client.set_finding_state(request)

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
async def test_set_finding_state_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.SetFindingStateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        await client.set_finding_state(request)

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


def test_set_finding_state_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_finding_state(
            name="name_value",
            state=finding.Finding.State.ACTIVE,
            start_time=timestamp_pb2.Timestamp(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].state
        mock_val = finding.Finding.State.ACTIVE
        assert arg == mock_val
        assert TimestampRule().to_proto(args[0].start_time) == timestamp_pb2.Timestamp(
            seconds=751
        )


def test_set_finding_state_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_finding_state(
            securitycenter_service.SetFindingStateRequest(),
            name="name_value",
            state=finding.Finding.State.ACTIVE,
            start_time=timestamp_pb2.Timestamp(seconds=751),
        )


@pytest.mark.asyncio
async def test_set_finding_state_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.set_finding_state), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_finding_state(
            name="name_value",
            state=finding.Finding.State.ACTIVE,
            start_time=timestamp_pb2.Timestamp(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].state
        mock_val = finding.Finding.State.ACTIVE
        assert arg == mock_val
        assert TimestampRule().to_proto(args[0].start_time) == timestamp_pb2.Timestamp(
            seconds=751
        )


@pytest.mark.asyncio
async def test_set_finding_state_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_finding_state(
            securitycenter_service.SetFindingStateRequest(),
            name="name_value",
            state=finding.Finding.State.ACTIVE,
            start_time=timestamp_pb2.Timestamp(seconds=751),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.SetMuteRequest,
        dict,
    ],
)
def test_set_mute(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding(
            name="name_value",
            parent="parent_value",
            resource_name="resource_name_value",
            state=finding.Finding.State.ACTIVE,
            category="category_value",
            external_uri="external_uri_value",
            severity=finding.Finding.Severity.CRITICAL,
            canonical_name="canonical_name_value",
            mute=finding.Finding.Mute.MUTED,
            finding_class=finding.Finding.FindingClass.THREAT,
            mute_initiator="mute_initiator_value",
            description="description_value",
            next_steps="next_steps_value",
        )
        response = client.set_mute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetMuteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == finding.Finding.Mute.MUTED
    assert response.finding_class == finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


def test_set_mute_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        client.set_mute()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetMuteRequest()


@pytest.mark.asyncio
async def test_set_mute_async(
    transport: str = "grpc_asyncio", request_type=securitycenter_service.SetMuteRequest
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            finding.Finding(
                name="name_value",
                parent="parent_value",
                resource_name="resource_name_value",
                state=finding.Finding.State.ACTIVE,
                category="category_value",
                external_uri="external_uri_value",
                severity=finding.Finding.Severity.CRITICAL,
                canonical_name="canonical_name_value",
                mute=finding.Finding.Mute.MUTED,
                finding_class=finding.Finding.FindingClass.THREAT,
                mute_initiator="mute_initiator_value",
                description="description_value",
                next_steps="next_steps_value",
            )
        )
        response = await client.set_mute(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.SetMuteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == finding.Finding.Mute.MUTED
    assert response.finding_class == finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


@pytest.mark.asyncio
async def test_set_mute_async_from_dict():
    await test_set_mute_async(request_type=dict)


def test_set_mute_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.SetMuteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        call.return_value = finding.Finding()
        client.set_mute(request)

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
async def test_set_mute_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.SetMuteRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        await client.set_mute(request)

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


def test_set_mute_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_mute(
            name="name_value",
            mute=finding.Finding.Mute.MUTED,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].mute
        mock_val = finding.Finding.Mute.MUTED
        assert arg == mock_val


def test_set_mute_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_mute(
            securitycenter_service.SetMuteRequest(),
            name="name_value",
            mute=finding.Finding.Mute.MUTED,
        )


@pytest.mark.asyncio
async def test_set_mute_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_mute), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_mute(
            name="name_value",
            mute=finding.Finding.Mute.MUTED,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].mute
        mock_val = finding.Finding.Mute.MUTED
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_mute_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_mute(
            securitycenter_service.SetMuteRequest(),
            name="name_value",
            mute=finding.Finding.Mute.MUTED,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterClient(
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
    client = SecurityCenterAsyncClient(
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
    client = SecurityCenterAsyncClient(
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


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateExternalSystemRequest,
        dict,
    ],
)
def test_update_external_system(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_external_system.ExternalSystem(
            name="name_value",
            assignees=["assignees_value"],
            external_uid="external_uid_value",
            status="status_value",
        )
        response = client.update_external_system(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateExternalSystemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_external_system.ExternalSystem)
    assert response.name == "name_value"
    assert response.assignees == ["assignees_value"]
    assert response.external_uid == "external_uid_value"
    assert response.status == "status_value"


def test_update_external_system_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        client.update_external_system()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateExternalSystemRequest()


@pytest.mark.asyncio
async def test_update_external_system_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateExternalSystemRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_external_system.ExternalSystem(
                name="name_value",
                assignees=["assignees_value"],
                external_uid="external_uid_value",
                status="status_value",
            )
        )
        response = await client.update_external_system(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateExternalSystemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_external_system.ExternalSystem)
    assert response.name == "name_value"
    assert response.assignees == ["assignees_value"]
    assert response.external_uid == "external_uid_value"
    assert response.status == "status_value"


@pytest.mark.asyncio
async def test_update_external_system_async_from_dict():
    await test_update_external_system_async(request_type=dict)


def test_update_external_system_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateExternalSystemRequest()

    request.external_system.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        call.return_value = gcs_external_system.ExternalSystem()
        client.update_external_system(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "external_system.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_external_system_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateExternalSystemRequest()

    request.external_system.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_external_system.ExternalSystem()
        )
        await client.update_external_system(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "external_system.name=name_value",
    ) in kw["metadata"]


def test_update_external_system_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_external_system.ExternalSystem()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_external_system(
            external_system=gcs_external_system.ExternalSystem(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].external_system
        mock_val = gcs_external_system.ExternalSystem(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_external_system_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_external_system(
            securitycenter_service.UpdateExternalSystemRequest(),
            external_system=gcs_external_system.ExternalSystem(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_external_system_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_external_system), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_external_system.ExternalSystem()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_external_system.ExternalSystem()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_external_system(
            external_system=gcs_external_system.ExternalSystem(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].external_system
        mock_val = gcs_external_system.ExternalSystem(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_external_system_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_external_system(
            securitycenter_service.UpdateExternalSystemRequest(),
            external_system=gcs_external_system.ExternalSystem(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateFindingRequest,
        dict,
    ],
)
def test_update_finding(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding(
            name="name_value",
            parent="parent_value",
            resource_name="resource_name_value",
            state=gcs_finding.Finding.State.ACTIVE,
            category="category_value",
            external_uri="external_uri_value",
            severity=gcs_finding.Finding.Severity.CRITICAL,
            canonical_name="canonical_name_value",
            mute=gcs_finding.Finding.Mute.MUTED,
            finding_class=gcs_finding.Finding.FindingClass.THREAT,
            mute_initiator="mute_initiator_value",
            description="description_value",
            next_steps="next_steps_value",
        )
        response = client.update_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == gcs_finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == gcs_finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == gcs_finding.Finding.Mute.MUTED
    assert response.finding_class == gcs_finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


def test_update_finding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        client.update_finding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateFindingRequest()


@pytest.mark.asyncio
async def test_update_finding_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateFindingRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_finding.Finding(
                name="name_value",
                parent="parent_value",
                resource_name="resource_name_value",
                state=gcs_finding.Finding.State.ACTIVE,
                category="category_value",
                external_uri="external_uri_value",
                severity=gcs_finding.Finding.Severity.CRITICAL,
                canonical_name="canonical_name_value",
                mute=gcs_finding.Finding.Mute.MUTED,
                finding_class=gcs_finding.Finding.FindingClass.THREAT,
                mute_initiator="mute_initiator_value",
                description="description_value",
                next_steps="next_steps_value",
            )
        )
        response = await client.update_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_finding.Finding)
    assert response.name == "name_value"
    assert response.parent == "parent_value"
    assert response.resource_name == "resource_name_value"
    assert response.state == gcs_finding.Finding.State.ACTIVE
    assert response.category == "category_value"
    assert response.external_uri == "external_uri_value"
    assert response.severity == gcs_finding.Finding.Severity.CRITICAL
    assert response.canonical_name == "canonical_name_value"
    assert response.mute == gcs_finding.Finding.Mute.MUTED
    assert response.finding_class == gcs_finding.Finding.FindingClass.THREAT
    assert response.mute_initiator == "mute_initiator_value"
    assert response.description == "description_value"
    assert response.next_steps == "next_steps_value"


@pytest.mark.asyncio
async def test_update_finding_async_from_dict():
    await test_update_finding_async(request_type=dict)


def test_update_finding_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateFindingRequest()

    request.finding.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        call.return_value = gcs_finding.Finding()
        client.update_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "finding.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_finding_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateFindingRequest()

    request.finding.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_finding.Finding())
        await client.update_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "finding.name=name_value",
    ) in kw["metadata"]


def test_update_finding_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_finding(
            finding=gcs_finding.Finding(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].finding
        mock_val = gcs_finding.Finding(name="name_value")
        assert arg == mock_val


def test_update_finding_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_finding(
            securitycenter_service.UpdateFindingRequest(),
            finding=gcs_finding.Finding(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_finding_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_finding.Finding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_finding.Finding())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_finding(
            finding=gcs_finding.Finding(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].finding
        mock_val = gcs_finding.Finding(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_finding_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_finding(
            securitycenter_service.UpdateFindingRequest(),
            finding=gcs_finding.Finding(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateMuteConfigRequest,
        dict,
    ],
)
def test_update_mute_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            filter="filter_value",
            most_recent_editor="most_recent_editor_value",
        )
        response = client.update_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


def test_update_mute_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        client.update_mute_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateMuteConfigRequest()


@pytest.mark.asyncio
async def test_update_mute_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateMuteConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                filter="filter_value",
                most_recent_editor="most_recent_editor_value",
            )
        )
        response = await client.update_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateMuteConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_mute_config.MuteConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.most_recent_editor == "most_recent_editor_value"


@pytest.mark.asyncio
async def test_update_mute_config_async_from_dict():
    await test_update_mute_config_async(request_type=dict)


def test_update_mute_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateMuteConfigRequest()

    request.mute_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        call.return_value = gcs_mute_config.MuteConfig()
        client.update_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "mute_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_mute_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateMuteConfigRequest()

    request.mute_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig()
        )
        await client.update_mute_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "mute_config.name=name_value",
    ) in kw["metadata"]


def test_update_mute_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_mute_config(
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].mute_config
        mock_val = gcs_mute_config.MuteConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_mute_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_mute_config(
            securitycenter_service.UpdateMuteConfigRequest(),
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_mute_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_mute_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_mute_config.MuteConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_mute_config.MuteConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_mute_config(
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].mute_config
        mock_val = gcs_mute_config.MuteConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_mute_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_mute_config(
            securitycenter_service.UpdateMuteConfigRequest(),
            mute_config=gcs_mute_config.MuteConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateNotificationConfigRequest,
        dict,
    ],
)
def test_update_notification_config(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig(
            name="name_value",
            description="description_value",
            pubsub_topic="pubsub_topic_value",
            service_account="service_account_value",
            streaming_config=gcs_notification_config.NotificationConfig.StreamingConfig(
                filter="filter_value"
            ),
        )
        response = client.update_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


def test_update_notification_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        client.update_notification_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateNotificationConfigRequest()


@pytest.mark.asyncio
async def test_update_notification_config_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateNotificationConfigRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig(
                name="name_value",
                description="description_value",
                pubsub_topic="pubsub_topic_value",
                service_account="service_account_value",
            )
        )
        response = await client.update_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateNotificationConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_notification_config.NotificationConfig)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.pubsub_topic == "pubsub_topic_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_update_notification_config_async_from_dict():
    await test_update_notification_config_async(request_type=dict)


def test_update_notification_config_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateNotificationConfigRequest()

    request.notification_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        call.return_value = gcs_notification_config.NotificationConfig()
        client.update_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "notification_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_notification_config_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateNotificationConfigRequest()

    request.notification_config.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig()
        )
        await client.update_notification_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "notification_config.name=name_value",
    ) in kw["metadata"]


def test_update_notification_config_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_notification_config(
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].notification_config
        mock_val = gcs_notification_config.NotificationConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_notification_config_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_notification_config(
            securitycenter_service.UpdateNotificationConfigRequest(),
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_notification_config_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_notification_config.NotificationConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_notification_config.NotificationConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_notification_config(
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].notification_config
        mock_val = gcs_notification_config.NotificationConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_notification_config_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_notification_config(
            securitycenter_service.UpdateNotificationConfigRequest(),
            notification_config=gcs_notification_config.NotificationConfig(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateOrganizationSettingsRequest,
        dict,
    ],
)
def test_update_organization_settings(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_organization_settings.OrganizationSettings(
            name="name_value",
            enable_asset_discovery=True,
        )
        response = client.update_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateOrganizationSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_organization_settings.OrganizationSettings)
    assert response.name == "name_value"
    assert response.enable_asset_discovery is True


def test_update_organization_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        client.update_organization_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateOrganizationSettingsRequest()


@pytest.mark.asyncio
async def test_update_organization_settings_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateOrganizationSettingsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_organization_settings.OrganizationSettings(
                name="name_value",
                enable_asset_discovery=True,
            )
        )
        response = await client.update_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateOrganizationSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_organization_settings.OrganizationSettings)
    assert response.name == "name_value"
    assert response.enable_asset_discovery is True


@pytest.mark.asyncio
async def test_update_organization_settings_async_from_dict():
    await test_update_organization_settings_async(request_type=dict)


def test_update_organization_settings_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateOrganizationSettingsRequest()

    request.organization_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        call.return_value = gcs_organization_settings.OrganizationSettings()
        client.update_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "organization_settings.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_organization_settings_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateOrganizationSettingsRequest()

    request.organization_settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_organization_settings.OrganizationSettings()
        )
        await client.update_organization_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "organization_settings.name=name_value",
    ) in kw["metadata"]


def test_update_organization_settings_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_organization_settings.OrganizationSettings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_organization_settings(
            organization_settings=gcs_organization_settings.OrganizationSettings(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].organization_settings
        mock_val = gcs_organization_settings.OrganizationSettings(name="name_value")
        assert arg == mock_val


def test_update_organization_settings_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_organization_settings(
            securitycenter_service.UpdateOrganizationSettingsRequest(),
            organization_settings=gcs_organization_settings.OrganizationSettings(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_update_organization_settings_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_organization_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_organization_settings.OrganizationSettings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_organization_settings.OrganizationSettings()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_organization_settings(
            organization_settings=gcs_organization_settings.OrganizationSettings(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].organization_settings
        mock_val = gcs_organization_settings.OrganizationSettings(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_organization_settings_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_organization_settings(
            securitycenter_service.UpdateOrganizationSettingsRequest(),
            organization_settings=gcs_organization_settings.OrganizationSettings(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateSourceRequest,
        dict,
    ],
)
def test_update_source(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            canonical_name="canonical_name_value",
        )
        response = client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


def test_update_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        client.update_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSourceRequest()


@pytest.mark.asyncio
async def test_update_source_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateSourceRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_source.Source(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                canonical_name="canonical_name_value",
            )
        )
        response = await client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_source.Source)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.canonical_name == "canonical_name_value"


@pytest.mark.asyncio
async def test_update_source_async_from_dict():
    await test_update_source_async(request_type=dict)


def test_update_source_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateSourceRequest()

    request.source.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        call.return_value = gcs_source.Source()
        client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_source_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateSourceRequest()

    request.source.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_source.Source())
        await client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source.name=name_value",
    ) in kw["metadata"]


def test_update_source_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_source(
            source=gcs_source.Source(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = gcs_source.Source(name="name_value")
        assert arg == mock_val


def test_update_source_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_source(
            securitycenter_service.UpdateSourceRequest(),
            source=gcs_source.Source(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_source_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_source.Source()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_source.Source())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_source(
            source=gcs_source.Source(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = gcs_source.Source(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_source_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_source(
            securitycenter_service.UpdateSourceRequest(),
            source=gcs_source.Source(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateSecurityMarksRequest,
        dict,
    ],
)
def test_update_security_marks(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_security_marks.SecurityMarks(
            name="name_value",
            canonical_name="canonical_name_value",
        )
        response = client.update_security_marks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSecurityMarksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_security_marks.SecurityMarks)
    assert response.name == "name_value"
    assert response.canonical_name == "canonical_name_value"


def test_update_security_marks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        client.update_security_marks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSecurityMarksRequest()


@pytest.mark.asyncio
async def test_update_security_marks_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateSecurityMarksRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_security_marks.SecurityMarks(
                name="name_value",
                canonical_name="canonical_name_value",
            )
        )
        response = await client.update_security_marks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateSecurityMarksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_security_marks.SecurityMarks)
    assert response.name == "name_value"
    assert response.canonical_name == "canonical_name_value"


@pytest.mark.asyncio
async def test_update_security_marks_async_from_dict():
    await test_update_security_marks_async(request_type=dict)


def test_update_security_marks_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateSecurityMarksRequest()

    request.security_marks.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        call.return_value = gcs_security_marks.SecurityMarks()
        client.update_security_marks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_marks.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_security_marks_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateSecurityMarksRequest()

    request.security_marks.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_security_marks.SecurityMarks()
        )
        await client.update_security_marks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "security_marks.name=name_value",
    ) in kw["metadata"]


def test_update_security_marks_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_security_marks.SecurityMarks()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_security_marks(
            security_marks=gcs_security_marks.SecurityMarks(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_marks
        mock_val = gcs_security_marks.SecurityMarks(name="name_value")
        assert arg == mock_val


def test_update_security_marks_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_security_marks(
            securitycenter_service.UpdateSecurityMarksRequest(),
            security_marks=gcs_security_marks.SecurityMarks(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_security_marks_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_security_marks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_security_marks.SecurityMarks()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_security_marks.SecurityMarks()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_security_marks(
            security_marks=gcs_security_marks.SecurityMarks(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].security_marks
        mock_val = gcs_security_marks.SecurityMarks(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_security_marks_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_security_marks(
            securitycenter_service.UpdateSecurityMarksRequest(),
            security_marks=gcs_security_marks.SecurityMarks(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.CreateBigQueryExportRequest,
        dict,
    ],
)
def test_create_big_query_export(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport(
            name="name_value",
            description="description_value",
            filter="filter_value",
            dataset="dataset_value",
            most_recent_editor="most_recent_editor_value",
            principal="principal_value",
        )
        response = client.create_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


def test_create_big_query_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        client.create_big_query_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateBigQueryExportRequest()


@pytest.mark.asyncio
async def test_create_big_query_export_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.CreateBigQueryExportRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport(
                name="name_value",
                description="description_value",
                filter="filter_value",
                dataset="dataset_value",
                most_recent_editor="most_recent_editor_value",
                principal="principal_value",
            )
        )
        response = await client.create_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.CreateBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


@pytest.mark.asyncio
async def test_create_big_query_export_async_from_dict():
    await test_create_big_query_export_async(request_type=dict)


def test_create_big_query_export_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateBigQueryExportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        call.return_value = bigquery_export.BigQueryExport()
        client.create_big_query_export(request)

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
async def test_create_big_query_export_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.CreateBigQueryExportRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        await client.create_big_query_export(request)

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


def test_create_big_query_export_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_big_query_export(
            parent="parent_value",
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            big_query_export_id="big_query_export_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].big_query_export
        mock_val = bigquery_export.BigQueryExport(name="name_value")
        assert arg == mock_val
        arg = args[0].big_query_export_id
        mock_val = "big_query_export_id_value"
        assert arg == mock_val


def test_create_big_query_export_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_big_query_export(
            securitycenter_service.CreateBigQueryExportRequest(),
            parent="parent_value",
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            big_query_export_id="big_query_export_id_value",
        )


@pytest.mark.asyncio
async def test_create_big_query_export_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_big_query_export(
            parent="parent_value",
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            big_query_export_id="big_query_export_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].big_query_export
        mock_val = bigquery_export.BigQueryExport(name="name_value")
        assert arg == mock_val
        arg = args[0].big_query_export_id
        mock_val = "big_query_export_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_big_query_export_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_big_query_export(
            securitycenter_service.CreateBigQueryExportRequest(),
            parent="parent_value",
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            big_query_export_id="big_query_export_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.DeleteBigQueryExportRequest,
        dict,
    ],
)
def test_delete_big_query_export(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_big_query_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        client.delete_big_query_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteBigQueryExportRequest()


@pytest.mark.asyncio
async def test_delete_big_query_export_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.DeleteBigQueryExportRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.DeleteBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_big_query_export_async_from_dict():
    await test_delete_big_query_export_async(request_type=dict)


def test_delete_big_query_export_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteBigQueryExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        call.return_value = None
        client.delete_big_query_export(request)

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
async def test_delete_big_query_export_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.DeleteBigQueryExportRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_big_query_export(request)

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


def test_delete_big_query_export_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_big_query_export(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_big_query_export_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_big_query_export(
            securitycenter_service.DeleteBigQueryExportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_big_query_export_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_big_query_export(
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
async def test_delete_big_query_export_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_big_query_export(
            securitycenter_service.DeleteBigQueryExportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.UpdateBigQueryExportRequest,
        dict,
    ],
)
def test_update_big_query_export(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport(
            name="name_value",
            description="description_value",
            filter="filter_value",
            dataset="dataset_value",
            most_recent_editor="most_recent_editor_value",
            principal="principal_value",
        )
        response = client.update_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


def test_update_big_query_export_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        client.update_big_query_export()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateBigQueryExportRequest()


@pytest.mark.asyncio
async def test_update_big_query_export_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.UpdateBigQueryExportRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport(
                name="name_value",
                description="description_value",
                filter="filter_value",
                dataset="dataset_value",
                most_recent_editor="most_recent_editor_value",
                principal="principal_value",
            )
        )
        response = await client.update_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.UpdateBigQueryExportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, bigquery_export.BigQueryExport)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.filter == "filter_value"
    assert response.dataset == "dataset_value"
    assert response.most_recent_editor == "most_recent_editor_value"
    assert response.principal == "principal_value"


@pytest.mark.asyncio
async def test_update_big_query_export_async_from_dict():
    await test_update_big_query_export_async(request_type=dict)


def test_update_big_query_export_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateBigQueryExportRequest()

    request.big_query_export.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        call.return_value = bigquery_export.BigQueryExport()
        client.update_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "big_query_export.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_big_query_export_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.UpdateBigQueryExportRequest()

    request.big_query_export.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        await client.update_big_query_export(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "big_query_export.name=name_value",
    ) in kw["metadata"]


def test_update_big_query_export_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_big_query_export(
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].big_query_export
        mock_val = bigquery_export.BigQueryExport(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_big_query_export_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_big_query_export(
            securitycenter_service.UpdateBigQueryExportRequest(),
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_big_query_export_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_big_query_export), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = bigquery_export.BigQueryExport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            bigquery_export.BigQueryExport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_big_query_export(
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].big_query_export
        mock_val = bigquery_export.BigQueryExport(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_big_query_export_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_big_query_export(
            securitycenter_service.UpdateBigQueryExportRequest(),
            big_query_export=bigquery_export.BigQueryExport(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        securitycenter_service.ListBigQueryExportsRequest,
        dict,
    ],
)
def test_list_big_query_exports(request_type, transport: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListBigQueryExportsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_big_query_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListBigQueryExportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBigQueryExportsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_big_query_exports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        client.list_big_query_exports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListBigQueryExportsRequest()


@pytest.mark.asyncio
async def test_list_big_query_exports_async(
    transport: str = "grpc_asyncio",
    request_type=securitycenter_service.ListBigQueryExportsRequest,
):
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListBigQueryExportsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_big_query_exports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == securitycenter_service.ListBigQueryExportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBigQueryExportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_big_query_exports_async_from_dict():
    await test_list_big_query_exports_async(request_type=dict)


def test_list_big_query_exports_field_headers():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListBigQueryExportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        call.return_value = securitycenter_service.ListBigQueryExportsResponse()
        client.list_big_query_exports(request)

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
async def test_list_big_query_exports_field_headers_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = securitycenter_service.ListBigQueryExportsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListBigQueryExportsResponse()
        )
        await client.list_big_query_exports(request)

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


def test_list_big_query_exports_flattened():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListBigQueryExportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_big_query_exports(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_big_query_exports_flattened_error():
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_big_query_exports(
            securitycenter_service.ListBigQueryExportsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_big_query_exports_flattened_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = securitycenter_service.ListBigQueryExportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            securitycenter_service.ListBigQueryExportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_big_query_exports(
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
async def test_list_big_query_exports_flattened_error_async():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_big_query_exports(
            securitycenter_service.ListBigQueryExportsRequest(),
            parent="parent_value",
        )


def test_list_big_query_exports_pager(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[],
                next_page_token="def",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_big_query_exports(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, bigquery_export.BigQueryExport) for i in results)


def test_list_big_query_exports_pages(transport_name: str = "grpc"):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[],
                next_page_token="def",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_big_query_exports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_big_query_exports_async_pager():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[],
                next_page_token="def",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_big_query_exports(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, bigquery_export.BigQueryExport) for i in responses)


@pytest.mark.asyncio
async def test_list_big_query_exports_async_pages():
    client = SecurityCenterAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_big_query_exports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="abc",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[],
                next_page_token="def",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                ],
                next_page_token="ghi",
            ),
            securitycenter_service.ListBigQueryExportsResponse(
                big_query_exports=[
                    bigquery_export.BigQueryExport(),
                    bigquery_export.BigQueryExport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_big_query_exports(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SecurityCenterClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = SecurityCenterClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SecurityCenterClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = SecurityCenterClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SecurityCenterGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.SecurityCenterGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
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
    transport = SecurityCenterClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.SecurityCenterGrpcTransport,
    )


def test_security_center_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.SecurityCenterTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_security_center_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.securitycenter_v1.services.security_center.transports.SecurityCenterTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SecurityCenterTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "bulk_mute_findings",
        "create_source",
        "create_finding",
        "create_mute_config",
        "create_notification_config",
        "delete_mute_config",
        "delete_notification_config",
        "get_big_query_export",
        "get_iam_policy",
        "get_mute_config",
        "get_notification_config",
        "get_organization_settings",
        "get_source",
        "group_assets",
        "group_findings",
        "list_assets",
        "list_findings",
        "list_mute_configs",
        "list_notification_configs",
        "list_sources",
        "run_asset_discovery",
        "set_finding_state",
        "set_mute",
        "set_iam_policy",
        "test_iam_permissions",
        "update_external_system",
        "update_finding",
        "update_mute_config",
        "update_notification_config",
        "update_organization_settings",
        "update_source",
        "update_security_marks",
        "create_big_query_export",
        "delete_big_query_export",
        "update_big_query_export",
        "list_big_query_exports",
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


def test_security_center_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.securitycenter_v1.services.security_center.transports.SecurityCenterTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SecurityCenterTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_security_center_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.securitycenter_v1.services.security_center.transports.SecurityCenterTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SecurityCenterTransport()
        adc.assert_called_once()


def test_security_center_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SecurityCenterClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
    ],
)
def test_security_center_transport_auth_adc(transport_class):
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
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
    ],
)
def test_security_center_transport_auth_gdch_credentials(transport_class):
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
        (transports.SecurityCenterGrpcTransport, grpc_helpers),
        (transports.SecurityCenterGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_security_center_transport_create_channel(transport_class, grpc_helpers):
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
            "securitycenter.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="securitycenter.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
    ],
)
def test_security_center_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_security_center_host_no_port(transport_name):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="securitycenter.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("securitycenter.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_security_center_host_with_port(transport_name):
    client = SecurityCenterClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="securitycenter.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("securitycenter.googleapis.com:8000")


def test_security_center_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SecurityCenterGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_security_center_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.SecurityCenterGrpcAsyncIOTransport(
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
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
    ],
)
def test_security_center_transport_channel_mtls_with_client_cert_source(
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
        transports.SecurityCenterGrpcTransport,
        transports.SecurityCenterGrpcAsyncIOTransport,
    ],
)
def test_security_center_transport_channel_mtls_with_adc(transport_class):
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


def test_security_center_grpc_lro_client():
    client = SecurityCenterClient(
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


def test_security_center_grpc_lro_async_client():
    client = SecurityCenterAsyncClient(
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


def test_asset_path():
    organization = "squid"
    asset = "clam"
    expected = "organizations/{organization}/assets/{asset}".format(
        organization=organization,
        asset=asset,
    )
    actual = SecurityCenterClient.asset_path(organization, asset)
    assert expected == actual


def test_parse_asset_path():
    expected = {
        "organization": "whelk",
        "asset": "octopus",
    }
    path = SecurityCenterClient.asset_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_asset_path(path)
    assert expected == actual


def test_big_query_export_path():
    organization = "oyster"
    export = "nudibranch"
    expected = "organizations/{organization}/bigQueryExports/{export}".format(
        organization=organization,
        export=export,
    )
    actual = SecurityCenterClient.big_query_export_path(organization, export)
    assert expected == actual


def test_parse_big_query_export_path():
    expected = {
        "organization": "cuttlefish",
        "export": "mussel",
    }
    path = SecurityCenterClient.big_query_export_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_big_query_export_path(path)
    assert expected == actual


def test_external_system_path():
    organization = "winkle"
    source = "nautilus"
    finding = "scallop"
    externalsystem = "abalone"
    expected = "organizations/{organization}/sources/{source}/findings/{finding}/externalSystems/{externalsystem}".format(
        organization=organization,
        source=source,
        finding=finding,
        externalsystem=externalsystem,
    )
    actual = SecurityCenterClient.external_system_path(
        organization, source, finding, externalsystem
    )
    assert expected == actual


def test_parse_external_system_path():
    expected = {
        "organization": "squid",
        "source": "clam",
        "finding": "whelk",
        "externalsystem": "octopus",
    }
    path = SecurityCenterClient.external_system_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_external_system_path(path)
    assert expected == actual


def test_finding_path():
    organization = "oyster"
    source = "nudibranch"
    finding = "cuttlefish"
    expected = (
        "organizations/{organization}/sources/{source}/findings/{finding}".format(
            organization=organization,
            source=source,
            finding=finding,
        )
    )
    actual = SecurityCenterClient.finding_path(organization, source, finding)
    assert expected == actual


def test_parse_finding_path():
    expected = {
        "organization": "mussel",
        "source": "winkle",
        "finding": "nautilus",
    }
    path = SecurityCenterClient.finding_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_finding_path(path)
    assert expected == actual


def test_mute_config_path():
    organization = "scallop"
    mute_config = "abalone"
    expected = "organizations/{organization}/muteConfigs/{mute_config}".format(
        organization=organization,
        mute_config=mute_config,
    )
    actual = SecurityCenterClient.mute_config_path(organization, mute_config)
    assert expected == actual


def test_parse_mute_config_path():
    expected = {
        "organization": "squid",
        "mute_config": "clam",
    }
    path = SecurityCenterClient.mute_config_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_mute_config_path(path)
    assert expected == actual


def test_notification_config_path():
    organization = "whelk"
    notification_config = "octopus"
    expected = (
        "organizations/{organization}/notificationConfigs/{notification_config}".format(
            organization=organization,
            notification_config=notification_config,
        )
    )
    actual = SecurityCenterClient.notification_config_path(
        organization, notification_config
    )
    assert expected == actual


def test_parse_notification_config_path():
    expected = {
        "organization": "oyster",
        "notification_config": "nudibranch",
    }
    path = SecurityCenterClient.notification_config_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_notification_config_path(path)
    assert expected == actual


def test_organization_settings_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}/organizationSettings".format(
        organization=organization,
    )
    actual = SecurityCenterClient.organization_settings_path(organization)
    assert expected == actual


def test_parse_organization_settings_path():
    expected = {
        "organization": "mussel",
    }
    path = SecurityCenterClient.organization_settings_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_organization_settings_path(path)
    assert expected == actual


def test_security_marks_path():
    organization = "winkle"
    asset = "nautilus"
    expected = "organizations/{organization}/assets/{asset}/securityMarks".format(
        organization=organization,
        asset=asset,
    )
    actual = SecurityCenterClient.security_marks_path(organization, asset)
    assert expected == actual


def test_parse_security_marks_path():
    expected = {
        "organization": "scallop",
        "asset": "abalone",
    }
    path = SecurityCenterClient.security_marks_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_security_marks_path(path)
    assert expected == actual


def test_source_path():
    organization = "squid"
    source = "clam"
    expected = "organizations/{organization}/sources/{source}".format(
        organization=organization,
        source=source,
    )
    actual = SecurityCenterClient.source_path(organization, source)
    assert expected == actual


def test_parse_source_path():
    expected = {
        "organization": "whelk",
        "source": "octopus",
    }
    path = SecurityCenterClient.source_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_source_path(path)
    assert expected == actual


def test_topic_path():
    project = "oyster"
    topic = "nudibranch"
    expected = "projects/{project}/topics/{topic}".format(
        project=project,
        topic=topic,
    )
    actual = SecurityCenterClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "cuttlefish",
        "topic": "mussel",
    }
    path = SecurityCenterClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_topic_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SecurityCenterClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = SecurityCenterClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = SecurityCenterClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = SecurityCenterClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = SecurityCenterClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = SecurityCenterClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = SecurityCenterClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = SecurityCenterClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = SecurityCenterClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = SecurityCenterClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SecurityCenterClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SecurityCenterTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SecurityCenterClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SecurityCenterTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SecurityCenterClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = SecurityCenterAsyncClient(
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
        client = SecurityCenterClient(
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
        client = SecurityCenterClient(
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
        (SecurityCenterClient, transports.SecurityCenterGrpcTransport),
        (SecurityCenterAsyncClient, transports.SecurityCenterGrpcAsyncIOTransport),
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
