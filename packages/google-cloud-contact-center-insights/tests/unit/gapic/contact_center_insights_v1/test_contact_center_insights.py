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
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.contact_center_insights_v1.services.contact_center_insights import (
    ContactCenterInsightsAsyncClient,
    ContactCenterInsightsClient,
    pagers,
    transports,
)
from google.cloud.contact_center_insights_v1.types import (
    contact_center_insights,
    resources,
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

    assert ContactCenterInsightsClient._get_default_mtls_endpoint(None) is None
    assert (
        ContactCenterInsightsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ContactCenterInsightsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ContactCenterInsightsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ContactCenterInsightsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ContactCenterInsightsClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ContactCenterInsightsClient, "grpc"),
        (ContactCenterInsightsAsyncClient, "grpc_asyncio"),
    ],
)
def test_contact_center_insights_client_from_service_account_info(
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

        assert client.transport._host == ("contactcenterinsights.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ContactCenterInsightsGrpcTransport, "grpc"),
        (transports.ContactCenterInsightsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_contact_center_insights_client_service_account_always_use_jwt(
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
        (ContactCenterInsightsClient, "grpc"),
        (ContactCenterInsightsAsyncClient, "grpc_asyncio"),
    ],
)
def test_contact_center_insights_client_from_service_account_file(
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

        assert client.transport._host == ("contactcenterinsights.googleapis.com:443")


def test_contact_center_insights_client_get_transport_class():
    transport = ContactCenterInsightsClient.get_transport_class()
    available_transports = [
        transports.ContactCenterInsightsGrpcTransport,
    ]
    assert transport in available_transports

    transport = ContactCenterInsightsClient.get_transport_class("grpc")
    assert transport == transports.ContactCenterInsightsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ContactCenterInsightsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsClient),
)
@mock.patch.object(
    ContactCenterInsightsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsAsyncClient),
)
def test_contact_center_insights_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ContactCenterInsightsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ContactCenterInsightsClient, "get_transport_class") as gtc:
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
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ContactCenterInsightsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsClient),
)
@mock.patch.object(
    ContactCenterInsightsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_contact_center_insights_client_mtls_env_auto(
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
    "client_class", [ContactCenterInsightsClient, ContactCenterInsightsAsyncClient]
)
@mock.patch.object(
    ContactCenterInsightsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsClient),
)
@mock.patch.object(
    ContactCenterInsightsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ContactCenterInsightsAsyncClient),
)
def test_contact_center_insights_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_contact_center_insights_client_client_options_scopes(
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
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_contact_center_insights_client_client_options_credentials_file(
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


def test_contact_center_insights_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.contact_center_insights_v1.services.contact_center_insights.transports.ContactCenterInsightsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ContactCenterInsightsClient(
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
            ContactCenterInsightsClient,
            transports.ContactCenterInsightsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_contact_center_insights_client_create_channel_credentials_file(
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
            "contactcenterinsights.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="contactcenterinsights.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CreateConversationRequest,
        dict,
    ],
)
def test_create_conversation(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation(
            name="name_value",
            language_code="language_code_value",
            agent_id="agent_id_value",
            medium=resources.Conversation.Medium.PHONE_CALL,
            turn_count=1105,
            obfuscated_user_id="obfuscated_user_id_value",
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706),
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


def test_create_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        client.create_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateConversationRequest()


@pytest.mark.asyncio
async def test_create_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CreateConversationRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation(
                name="name_value",
                language_code="language_code_value",
                agent_id="agent_id_value",
                medium=resources.Conversation.Medium.PHONE_CALL,
                turn_count=1105,
                obfuscated_user_id="obfuscated_user_id_value",
            )
        )
        response = await client.create_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


@pytest.mark.asyncio
async def test_create_conversation_async_from_dict():
    await test_create_conversation_async(request_type=dict)


def test_create_conversation_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateConversationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        call.return_value = resources.Conversation()
        client.create_conversation(request)

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
async def test_create_conversation_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateConversationRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        await client.create_conversation(request)

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


def test_create_conversation_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversation(
            parent="parent_value",
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            conversation_id="conversation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversation
        mock_val = resources.Conversation(
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
        )
        assert arg == mock_val
        arg = args[0].conversation_id
        mock_val = "conversation_id_value"
        assert arg == mock_val


def test_create_conversation_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversation(
            contact_center_insights.CreateConversationRequest(),
            parent="parent_value",
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            conversation_id="conversation_id_value",
        )


@pytest.mark.asyncio
async def test_create_conversation_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversation(
            parent="parent_value",
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            conversation_id="conversation_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversation
        mock_val = resources.Conversation(
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
        )
        assert arg == mock_val
        arg = args[0].conversation_id
        mock_val = "conversation_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_conversation_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversation(
            contact_center_insights.CreateConversationRequest(),
            parent="parent_value",
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            conversation_id="conversation_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdateConversationRequest,
        dict,
    ],
)
def test_update_conversation(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation(
            name="name_value",
            language_code="language_code_value",
            agent_id="agent_id_value",
            medium=resources.Conversation.Medium.PHONE_CALL,
            turn_count=1105,
            obfuscated_user_id="obfuscated_user_id_value",
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706),
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.update_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


def test_update_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        client.update_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateConversationRequest()


@pytest.mark.asyncio
async def test_update_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdateConversationRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation(
                name="name_value",
                language_code="language_code_value",
                agent_id="agent_id_value",
                medium=resources.Conversation.Medium.PHONE_CALL,
                turn_count=1105,
                obfuscated_user_id="obfuscated_user_id_value",
            )
        )
        response = await client.update_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


@pytest.mark.asyncio
async def test_update_conversation_async_from_dict():
    await test_update_conversation_async(request_type=dict)


def test_update_conversation_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateConversationRequest()

    request.conversation.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        call.return_value = resources.Conversation()
        client.update_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversation.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_conversation_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateConversationRequest()

    request.conversation.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        await client.update_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversation.name=name_value",
    ) in kw["metadata"]


def test_update_conversation_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_conversation(
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversation
        mock_val = resources.Conversation(
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_conversation_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_conversation(
            contact_center_insights.UpdateConversationRequest(),
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_conversation_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_conversation(
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversation
        mock_val = resources.Conversation(
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_conversation_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_conversation(
            contact_center_insights.UpdateConversationRequest(),
            conversation=resources.Conversation(
                call_metadata=resources.Conversation.CallMetadata(customer_channel=1706)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetConversationRequest,
        dict,
    ],
)
def test_get_conversation(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation(
            name="name_value",
            language_code="language_code_value",
            agent_id="agent_id_value",
            medium=resources.Conversation.Medium.PHONE_CALL,
            turn_count=1105,
            obfuscated_user_id="obfuscated_user_id_value",
            call_metadata=resources.Conversation.CallMetadata(customer_channel=1706),
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


def test_get_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        client.get_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetConversationRequest()


@pytest.mark.asyncio
async def test_get_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetConversationRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation(
                name="name_value",
                language_code="language_code_value",
                agent_id="agent_id_value",
                medium=resources.Conversation.Medium.PHONE_CALL,
                turn_count=1105,
                obfuscated_user_id="obfuscated_user_id_value",
            )
        )
        response = await client.get_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetConversationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Conversation)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"
    assert response.agent_id == "agent_id_value"
    assert response.medium == resources.Conversation.Medium.PHONE_CALL
    assert response.turn_count == 1105
    assert response.obfuscated_user_id == "obfuscated_user_id_value"


@pytest.mark.asyncio
async def test_get_conversation_async_from_dict():
    await test_get_conversation_async(request_type=dict)


def test_get_conversation_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetConversationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        call.return_value = resources.Conversation()
        client.get_conversation(request)

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
async def test_get_conversation_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetConversationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        await client.get_conversation(request)

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


def test_get_conversation_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversation(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_conversation_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversation(
            contact_center_insights.GetConversationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversation_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_conversation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Conversation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Conversation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversation(
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
async def test_get_conversation_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversation(
            contact_center_insights.GetConversationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListConversationsRequest,
        dict,
    ],
)
def test_list_conversations(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListConversationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListConversationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_conversations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        client.list_conversations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListConversationsRequest()


@pytest.mark.asyncio
async def test_list_conversations_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListConversationsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListConversationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_conversations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListConversationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_conversations_async_from_dict():
    await test_list_conversations_async(request_type=dict)


def test_list_conversations_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListConversationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        call.return_value = contact_center_insights.ListConversationsResponse()
        client.list_conversations(request)

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
async def test_list_conversations_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListConversationsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListConversationsResponse()
        )
        await client.list_conversations(request)

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


def test_list_conversations_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListConversationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_conversations_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversations(
            contact_center_insights.ListConversationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversations_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListConversationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListConversationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversations(
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
async def test_list_conversations_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversations(
            contact_center_insights.ListConversationsRequest(),
            parent="parent_value",
        )


def test_list_conversations_pager(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                    resources.Conversation(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[],
                next_page_token="def",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversations(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Conversation) for i in results)


def test_list_conversations_pages(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                    resources.Conversation(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[],
                next_page_token="def",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversations_async_pager():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                    resources.Conversation(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[],
                next_page_token="def",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Conversation) for i in responses)


@pytest.mark.asyncio
async def test_list_conversations_async_pages():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                    resources.Conversation(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[],
                next_page_token="def",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListConversationsResponse(
                conversations=[
                    resources.Conversation(),
                    resources.Conversation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_conversations(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeleteConversationRequest,
        dict,
    ],
)
def test_delete_conversation(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteConversationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_conversation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        client.delete_conversation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteConversationRequest()


@pytest.mark.asyncio
async def test_delete_conversation_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeleteConversationRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_conversation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteConversationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_conversation_async_from_dict():
    await test_delete_conversation_async(request_type=dict)


def test_delete_conversation_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteConversationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        call.return_value = None
        client.delete_conversation(request)

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
async def test_delete_conversation_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteConversationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_conversation(request)

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


def test_delete_conversation_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_conversation(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_conversation_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversation(
            contact_center_insights.DeleteConversationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_conversation_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_conversation(
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
async def test_delete_conversation_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_conversation(
            contact_center_insights.DeleteConversationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CreateAnalysisRequest,
        dict,
    ],
)
def test_create_analysis(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_analysis_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        client.create_analysis()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateAnalysisRequest()


@pytest.mark.asyncio
async def test_create_analysis_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CreateAnalysisRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_analysis_async_from_dict():
    await test_create_analysis_async(request_type=dict)


def test_create_analysis_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateAnalysisRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_analysis(request)

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
async def test_create_analysis_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateAnalysisRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_analysis(request)

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


def test_create_analysis_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_analysis(
            parent="parent_value",
            analysis=resources.Analysis(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].analysis
        mock_val = resources.Analysis(name="name_value")
        assert arg == mock_val


def test_create_analysis_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_analysis(
            contact_center_insights.CreateAnalysisRequest(),
            parent="parent_value",
            analysis=resources.Analysis(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_analysis_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_analysis(
            parent="parent_value",
            analysis=resources.Analysis(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].analysis
        mock_val = resources.Analysis(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_analysis_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_analysis(
            contact_center_insights.CreateAnalysisRequest(),
            parent="parent_value",
            analysis=resources.Analysis(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetAnalysisRequest,
        dict,
    ],
)
def test_get_analysis(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Analysis(
            name="name_value",
        )
        response = client.get_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Analysis)
    assert response.name == "name_value"


def test_get_analysis_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        client.get_analysis()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetAnalysisRequest()


@pytest.mark.asyncio
async def test_get_analysis_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetAnalysisRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Analysis(
                name="name_value",
            )
        )
        response = await client.get_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Analysis)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_analysis_async_from_dict():
    await test_get_analysis_async(request_type=dict)


def test_get_analysis_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetAnalysisRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        call.return_value = resources.Analysis()
        client.get_analysis(request)

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
async def test_get_analysis_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetAnalysisRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Analysis())
        await client.get_analysis(request)

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


def test_get_analysis_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Analysis()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_analysis(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_analysis_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_analysis(
            contact_center_insights.GetAnalysisRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_analysis_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Analysis()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Analysis())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_analysis(
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
async def test_get_analysis_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_analysis(
            contact_center_insights.GetAnalysisRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListAnalysesRequest,
        dict,
    ],
)
def test_list_analyses(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListAnalysesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_analyses(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListAnalysesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnalysesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_analyses_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        client.list_analyses()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListAnalysesRequest()


@pytest.mark.asyncio
async def test_list_analyses_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListAnalysesRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListAnalysesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_analyses(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListAnalysesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAnalysesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_analyses_async_from_dict():
    await test_list_analyses_async(request_type=dict)


def test_list_analyses_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListAnalysesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        call.return_value = contact_center_insights.ListAnalysesResponse()
        client.list_analyses(request)

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
async def test_list_analyses_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListAnalysesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListAnalysesResponse()
        )
        await client.list_analyses(request)

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


def test_list_analyses_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListAnalysesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_analyses(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_analyses_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_analyses(
            contact_center_insights.ListAnalysesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_analyses_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListAnalysesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListAnalysesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_analyses(
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
async def test_list_analyses_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_analyses(
            contact_center_insights.ListAnalysesRequest(),
            parent="parent_value",
        )


def test_list_analyses_pager(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                    resources.Analysis(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[],
                next_page_token="def",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_analyses(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Analysis) for i in results)


def test_list_analyses_pages(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_analyses), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                    resources.Analysis(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[],
                next_page_token="def",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_analyses(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_analyses_async_pager():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analyses), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                    resources.Analysis(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[],
                next_page_token="def",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_analyses(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Analysis) for i in responses)


@pytest.mark.asyncio
async def test_list_analyses_async_pages():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_analyses), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                    resources.Analysis(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[],
                next_page_token="def",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListAnalysesResponse(
                analyses=[
                    resources.Analysis(),
                    resources.Analysis(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_analyses(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeleteAnalysisRequest,
        dict,
    ],
)
def test_delete_analysis(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_analysis_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        client.delete_analysis()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteAnalysisRequest()


@pytest.mark.asyncio
async def test_delete_analysis_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeleteAnalysisRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_analysis(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteAnalysisRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_analysis_async_from_dict():
    await test_delete_analysis_async(request_type=dict)


def test_delete_analysis_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteAnalysisRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        call.return_value = None
        client.delete_analysis(request)

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
async def test_delete_analysis_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteAnalysisRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_analysis(request)

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


def test_delete_analysis_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_analysis(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_analysis_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_analysis(
            contact_center_insights.DeleteAnalysisRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_analysis_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_analysis), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_analysis(
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
async def test_delete_analysis_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_analysis(
            contact_center_insights.DeleteAnalysisRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ExportInsightsDataRequest,
        dict,
    ],
)
def test_export_insights_data(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_insights_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ExportInsightsDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_insights_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        client.export_insights_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ExportInsightsDataRequest()


@pytest.mark.asyncio
async def test_export_insights_data_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ExportInsightsDataRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_insights_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ExportInsightsDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_insights_data_async_from_dict():
    await test_export_insights_data_async(request_type=dict)


def test_export_insights_data_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ExportInsightsDataRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_insights_data(request)

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
async def test_export_insights_data_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ExportInsightsDataRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_insights_data(request)

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


def test_export_insights_data_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_insights_data(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_export_insights_data_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_insights_data(
            contact_center_insights.ExportInsightsDataRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_export_insights_data_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_insights_data), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_insights_data(
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
async def test_export_insights_data_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_insights_data(
            contact_center_insights.ExportInsightsDataRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CreateIssueModelRequest,
        dict,
    ],
)
def test_create_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        client.create_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateIssueModelRequest()


@pytest.mark.asyncio
async def test_create_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CreateIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_issue_model_async_from_dict():
    await test_create_issue_model_async(request_type=dict)


def test_create_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateIssueModelRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_issue_model(request)

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
async def test_create_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateIssueModelRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_issue_model(request)

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


def test_create_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_issue_model(
            parent="parent_value",
            issue_model=resources.IssueModel(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].issue_model
        mock_val = resources.IssueModel(name="name_value")
        assert arg == mock_val


def test_create_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_issue_model(
            contact_center_insights.CreateIssueModelRequest(),
            parent="parent_value",
            issue_model=resources.IssueModel(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_issue_model(
            parent="parent_value",
            issue_model=resources.IssueModel(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].issue_model
        mock_val = resources.IssueModel(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_issue_model(
            contact_center_insights.CreateIssueModelRequest(),
            parent="parent_value",
            issue_model=resources.IssueModel(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdateIssueModelRequest,
        dict,
    ],
)
def test_update_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel(
            name="name_value",
            display_name="display_name_value",
            state=resources.IssueModel.State.UNDEPLOYED,
        )
        response = client.update_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IssueModel)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.IssueModel.State.UNDEPLOYED


def test_update_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        client.update_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueModelRequest()


@pytest.mark.asyncio
async def test_update_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdateIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel(
                name="name_value",
                display_name="display_name_value",
                state=resources.IssueModel.State.UNDEPLOYED,
            )
        )
        response = await client.update_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IssueModel)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.IssueModel.State.UNDEPLOYED


@pytest.mark.asyncio
async def test_update_issue_model_async_from_dict():
    await test_update_issue_model_async(request_type=dict)


def test_update_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateIssueModelRequest()

    request.issue_model.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        call.return_value = resources.IssueModel()
        client.update_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue_model.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateIssueModelRequest()

    request.issue_model.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel()
        )
        await client.update_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue_model.name=name_value",
    ) in kw["metadata"]


def test_update_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_issue_model(
            issue_model=resources.IssueModel(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue_model
        mock_val = resources.IssueModel(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_issue_model(
            contact_center_insights.UpdateIssueModelRequest(),
            issue_model=resources.IssueModel(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_issue_model(
            issue_model=resources.IssueModel(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue_model
        mock_val = resources.IssueModel(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_issue_model(
            contact_center_insights.UpdateIssueModelRequest(),
            issue_model=resources.IssueModel(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetIssueModelRequest,
        dict,
    ],
)
def test_get_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel(
            name="name_value",
            display_name="display_name_value",
            state=resources.IssueModel.State.UNDEPLOYED,
        )
        response = client.get_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IssueModel)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.IssueModel.State.UNDEPLOYED


def test_get_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        client.get_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueModelRequest()


@pytest.mark.asyncio
async def test_get_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel(
                name="name_value",
                display_name="display_name_value",
                state=resources.IssueModel.State.UNDEPLOYED,
            )
        )
        response = await client.get_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.IssueModel)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.IssueModel.State.UNDEPLOYED


@pytest.mark.asyncio
async def test_get_issue_model_async_from_dict():
    await test_get_issue_model_async(request_type=dict)


def test_get_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        call.return_value = resources.IssueModel()
        client.get_issue_model(request)

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
async def test_get_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel()
        )
        await client.get_issue_model(request)

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


def test_get_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_issue_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_issue_model(
            contact_center_insights.GetIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.IssueModel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.IssueModel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_issue_model(
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
async def test_get_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_issue_model(
            contact_center_insights.GetIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListIssueModelsRequest,
        dict,
    ],
)
def test_list_issue_models(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssueModelsResponse()
        response = client.list_issue_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssueModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.ListIssueModelsResponse)


def test_list_issue_models_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        client.list_issue_models()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssueModelsRequest()


@pytest.mark.asyncio
async def test_list_issue_models_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListIssueModelsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssueModelsResponse()
        )
        response = await client.list_issue_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssueModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.ListIssueModelsResponse)


@pytest.mark.asyncio
async def test_list_issue_models_async_from_dict():
    await test_list_issue_models_async(request_type=dict)


def test_list_issue_models_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListIssueModelsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        call.return_value = contact_center_insights.ListIssueModelsResponse()
        client.list_issue_models(request)

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
async def test_list_issue_models_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListIssueModelsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssueModelsResponse()
        )
        await client.list_issue_models(request)

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


def test_list_issue_models_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssueModelsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_issue_models(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_issue_models_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_issue_models(
            contact_center_insights.ListIssueModelsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_issue_models_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_issue_models), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssueModelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssueModelsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_issue_models(
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
async def test_list_issue_models_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_issue_models(
            contact_center_insights.ListIssueModelsRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeleteIssueModelRequest,
        dict,
    ],
)
def test_delete_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        client.delete_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteIssueModelRequest()


@pytest.mark.asyncio
async def test_delete_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeleteIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_issue_model_async_from_dict():
    await test_delete_issue_model_async(request_type=dict)


def test_delete_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_issue_model(request)

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
async def test_delete_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_issue_model(request)

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


def test_delete_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_issue_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_issue_model(
            contact_center_insights.DeleteIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_issue_model(
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
async def test_delete_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_issue_model(
            contact_center_insights.DeleteIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeployIssueModelRequest,
        dict,
    ],
)
def test_deploy_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.deploy_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeployIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_deploy_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        client.deploy_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeployIssueModelRequest()


@pytest.mark.asyncio
async def test_deploy_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeployIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.deploy_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeployIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_deploy_issue_model_async_from_dict():
    await test_deploy_issue_model_async(request_type=dict)


def test_deploy_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeployIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.deploy_issue_model(request)

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
async def test_deploy_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeployIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.deploy_issue_model(request)

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


def test_deploy_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.deploy_issue_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_deploy_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.deploy_issue_model(
            contact_center_insights.DeployIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_deploy_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.deploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.deploy_issue_model(
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
async def test_deploy_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.deploy_issue_model(
            contact_center_insights.DeployIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UndeployIssueModelRequest,
        dict,
    ],
)
def test_undeploy_issue_model(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undeploy_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UndeployIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undeploy_issue_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        client.undeploy_issue_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UndeployIssueModelRequest()


@pytest.mark.asyncio
async def test_undeploy_issue_model_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UndeployIssueModelRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undeploy_issue_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UndeployIssueModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undeploy_issue_model_async_from_dict():
    await test_undeploy_issue_model_async(request_type=dict)


def test_undeploy_issue_model_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UndeployIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undeploy_issue_model(request)

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
async def test_undeploy_issue_model_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UndeployIssueModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undeploy_issue_model(request)

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


def test_undeploy_issue_model_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undeploy_issue_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_undeploy_issue_model_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undeploy_issue_model(
            contact_center_insights.UndeployIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_undeploy_issue_model_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undeploy_issue_model), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undeploy_issue_model(
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
async def test_undeploy_issue_model_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undeploy_issue_model(
            contact_center_insights.UndeployIssueModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetIssueRequest,
        dict,
    ],
)
def test_get_issue(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.get_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Issue)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_issue_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        client.get_issue()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueRequest()


@pytest.mark.asyncio
async def test_get_issue_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetIssueRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Issue(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetIssueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Issue)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_issue_async_from_dict():
    await test_get_issue_async(request_type=dict)


def test_get_issue_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetIssueRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        call.return_value = resources.Issue()
        client.get_issue(request)

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
async def test_get_issue_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetIssueRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Issue())
        await client.get_issue(request)

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


def test_get_issue_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_issue(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_issue_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_issue(
            contact_center_insights.GetIssueRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_issue_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Issue())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_issue(
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
async def test_get_issue_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_issue(
            contact_center_insights.GetIssueRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListIssuesRequest,
        dict,
    ],
)
def test_list_issues(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssuesResponse()
        response = client.list_issues(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssuesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.ListIssuesResponse)


def test_list_issues_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        client.list_issues()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssuesRequest()


@pytest.mark.asyncio
async def test_list_issues_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListIssuesRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssuesResponse()
        )
        response = await client.list_issues(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListIssuesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.ListIssuesResponse)


@pytest.mark.asyncio
async def test_list_issues_async_from_dict():
    await test_list_issues_async(request_type=dict)


def test_list_issues_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListIssuesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        call.return_value = contact_center_insights.ListIssuesResponse()
        client.list_issues(request)

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
async def test_list_issues_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListIssuesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssuesResponse()
        )
        await client.list_issues(request)

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


def test_list_issues_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssuesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_issues(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_issues_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_issues(
            contact_center_insights.ListIssuesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_issues_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_issues), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListIssuesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListIssuesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_issues(
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
async def test_list_issues_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_issues(
            contact_center_insights.ListIssuesRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdateIssueRequest,
        dict,
    ],
)
def test_update_issue(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue(
            name="name_value",
            display_name="display_name_value",
        )
        response = client.update_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Issue)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_update_issue_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        client.update_issue()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueRequest()


@pytest.mark.asyncio
async def test_update_issue_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdateIssueRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Issue(
                name="name_value",
                display_name="display_name_value",
            )
        )
        response = await client.update_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateIssueRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Issue)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_issue_async_from_dict():
    await test_update_issue_async(request_type=dict)


def test_update_issue_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateIssueRequest()

    request.issue.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        call.return_value = resources.Issue()
        client.update_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_issue_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateIssueRequest()

    request.issue.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Issue())
        await client.update_issue(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue.name=name_value",
    ) in kw["metadata"]


def test_update_issue_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_issue(
            issue=resources.Issue(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue
        mock_val = resources.Issue(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_issue_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_issue(
            contact_center_insights.UpdateIssueRequest(),
            issue=resources.Issue(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_issue_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_issue), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Issue()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Issue())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_issue(
            issue=resources.Issue(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue
        mock_val = resources.Issue(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_issue_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_issue(
            contact_center_insights.UpdateIssueRequest(),
            issue=resources.Issue(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CalculateIssueModelStatsRequest,
        dict,
    ],
)
def test_calculate_issue_model_stats(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateIssueModelStatsResponse()
        response = client.calculate_issue_model_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateIssueModelStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, contact_center_insights.CalculateIssueModelStatsResponse
    )


def test_calculate_issue_model_stats_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        client.calculate_issue_model_stats()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateIssueModelStatsRequest()


@pytest.mark.asyncio
async def test_calculate_issue_model_stats_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CalculateIssueModelStatsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateIssueModelStatsResponse()
        )
        response = await client.calculate_issue_model_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateIssueModelStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, contact_center_insights.CalculateIssueModelStatsResponse
    )


@pytest.mark.asyncio
async def test_calculate_issue_model_stats_async_from_dict():
    await test_calculate_issue_model_stats_async(request_type=dict)


def test_calculate_issue_model_stats_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CalculateIssueModelStatsRequest()

    request.issue_model = "issue_model_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        call.return_value = contact_center_insights.CalculateIssueModelStatsResponse()
        client.calculate_issue_model_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue_model=issue_model_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_calculate_issue_model_stats_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CalculateIssueModelStatsRequest()

    request.issue_model = "issue_model_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateIssueModelStatsResponse()
        )
        await client.calculate_issue_model_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "issue_model=issue_model_value",
    ) in kw["metadata"]


def test_calculate_issue_model_stats_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateIssueModelStatsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.calculate_issue_model_stats(
            issue_model="issue_model_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue_model
        mock_val = "issue_model_value"
        assert arg == mock_val


def test_calculate_issue_model_stats_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.calculate_issue_model_stats(
            contact_center_insights.CalculateIssueModelStatsRequest(),
            issue_model="issue_model_value",
        )


@pytest.mark.asyncio
async def test_calculate_issue_model_stats_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.calculate_issue_model_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateIssueModelStatsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateIssueModelStatsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.calculate_issue_model_stats(
            issue_model="issue_model_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].issue_model
        mock_val = "issue_model_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_calculate_issue_model_stats_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.calculate_issue_model_stats(
            contact_center_insights.CalculateIssueModelStatsRequest(),
            issue_model="issue_model_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CreatePhraseMatcherRequest,
        dict,
    ],
)
def test_create_phrase_matcher(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher(
            name="name_value",
            revision_id="revision_id_value",
            version_tag="version_tag_value",
            display_name="display_name_value",
            type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
            active=True,
            role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
        )
        response = client.create_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreatePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


def test_create_phrase_matcher_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        client.create_phrase_matcher()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreatePhraseMatcherRequest()


@pytest.mark.asyncio
async def test_create_phrase_matcher_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CreatePhraseMatcherRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher(
                name="name_value",
                revision_id="revision_id_value",
                version_tag="version_tag_value",
                display_name="display_name_value",
                type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
                active=True,
                role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
            )
        )
        response = await client.create_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreatePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


@pytest.mark.asyncio
async def test_create_phrase_matcher_async_from_dict():
    await test_create_phrase_matcher_async(request_type=dict)


def test_create_phrase_matcher_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreatePhraseMatcherRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        call.return_value = resources.PhraseMatcher()
        client.create_phrase_matcher(request)

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
async def test_create_phrase_matcher_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreatePhraseMatcherRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        await client.create_phrase_matcher(request)

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


def test_create_phrase_matcher_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_phrase_matcher(
            parent="parent_value",
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_matcher
        mock_val = resources.PhraseMatcher(name="name_value")
        assert arg == mock_val


def test_create_phrase_matcher_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_phrase_matcher(
            contact_center_insights.CreatePhraseMatcherRequest(),
            parent="parent_value",
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_phrase_matcher_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_phrase_matcher(
            parent="parent_value",
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_matcher
        mock_val = resources.PhraseMatcher(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_phrase_matcher_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_phrase_matcher(
            contact_center_insights.CreatePhraseMatcherRequest(),
            parent="parent_value",
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetPhraseMatcherRequest,
        dict,
    ],
)
def test_get_phrase_matcher(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher(
            name="name_value",
            revision_id="revision_id_value",
            version_tag="version_tag_value",
            display_name="display_name_value",
            type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
            active=True,
            role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
        )
        response = client.get_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetPhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


def test_get_phrase_matcher_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        client.get_phrase_matcher()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetPhraseMatcherRequest()


@pytest.mark.asyncio
async def test_get_phrase_matcher_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetPhraseMatcherRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher(
                name="name_value",
                revision_id="revision_id_value",
                version_tag="version_tag_value",
                display_name="display_name_value",
                type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
                active=True,
                role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
            )
        )
        response = await client.get_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetPhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


@pytest.mark.asyncio
async def test_get_phrase_matcher_async_from_dict():
    await test_get_phrase_matcher_async(request_type=dict)


def test_get_phrase_matcher_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetPhraseMatcherRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        call.return_value = resources.PhraseMatcher()
        client.get_phrase_matcher(request)

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
async def test_get_phrase_matcher_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetPhraseMatcherRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        await client.get_phrase_matcher(request)

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


def test_get_phrase_matcher_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_phrase_matcher(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_phrase_matcher_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_phrase_matcher(
            contact_center_insights.GetPhraseMatcherRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_phrase_matcher_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_phrase_matcher(
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
async def test_get_phrase_matcher_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_phrase_matcher(
            contact_center_insights.GetPhraseMatcherRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListPhraseMatchersRequest,
        dict,
    ],
)
def test_list_phrase_matchers(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListPhraseMatchersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_phrase_matchers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListPhraseMatchersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseMatchersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_phrase_matchers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        client.list_phrase_matchers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListPhraseMatchersRequest()


@pytest.mark.asyncio
async def test_list_phrase_matchers_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListPhraseMatchersRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListPhraseMatchersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_phrase_matchers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListPhraseMatchersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseMatchersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_phrase_matchers_async_from_dict():
    await test_list_phrase_matchers_async(request_type=dict)


def test_list_phrase_matchers_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListPhraseMatchersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        call.return_value = contact_center_insights.ListPhraseMatchersResponse()
        client.list_phrase_matchers(request)

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
async def test_list_phrase_matchers_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListPhraseMatchersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListPhraseMatchersResponse()
        )
        await client.list_phrase_matchers(request)

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


def test_list_phrase_matchers_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListPhraseMatchersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_phrase_matchers(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_phrase_matchers_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_phrase_matchers(
            contact_center_insights.ListPhraseMatchersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_phrase_matchers_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListPhraseMatchersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListPhraseMatchersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_phrase_matchers(
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
async def test_list_phrase_matchers_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_phrase_matchers(
            contact_center_insights.ListPhraseMatchersRequest(),
            parent="parent_value",
        )


def test_list_phrase_matchers_pager(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[],
                next_page_token="def",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_phrase_matchers(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.PhraseMatcher) for i in results)


def test_list_phrase_matchers_pages(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[],
                next_page_token="def",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_phrase_matchers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_phrase_matchers_async_pager():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[],
                next_page_token="def",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_phrase_matchers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.PhraseMatcher) for i in responses)


@pytest.mark.asyncio
async def test_list_phrase_matchers_async_pages():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_matchers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[],
                next_page_token="def",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListPhraseMatchersResponse(
                phrase_matchers=[
                    resources.PhraseMatcher(),
                    resources.PhraseMatcher(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_phrase_matchers(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeletePhraseMatcherRequest,
        dict,
    ],
)
def test_delete_phrase_matcher(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeletePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_phrase_matcher_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        client.delete_phrase_matcher()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeletePhraseMatcherRequest()


@pytest.mark.asyncio
async def test_delete_phrase_matcher_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeletePhraseMatcherRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeletePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_phrase_matcher_async_from_dict():
    await test_delete_phrase_matcher_async(request_type=dict)


def test_delete_phrase_matcher_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeletePhraseMatcherRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        call.return_value = None
        client.delete_phrase_matcher(request)

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
async def test_delete_phrase_matcher_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeletePhraseMatcherRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_phrase_matcher(request)

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


def test_delete_phrase_matcher_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_phrase_matcher(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_phrase_matcher_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_phrase_matcher(
            contact_center_insights.DeletePhraseMatcherRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_phrase_matcher_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_phrase_matcher(
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
async def test_delete_phrase_matcher_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_phrase_matcher(
            contact_center_insights.DeletePhraseMatcherRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdatePhraseMatcherRequest,
        dict,
    ],
)
def test_update_phrase_matcher(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher(
            name="name_value",
            revision_id="revision_id_value",
            version_tag="version_tag_value",
            display_name="display_name_value",
            type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
            active=True,
            role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
        )
        response = client.update_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdatePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


def test_update_phrase_matcher_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        client.update_phrase_matcher()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdatePhraseMatcherRequest()


@pytest.mark.asyncio
async def test_update_phrase_matcher_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdatePhraseMatcherRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher(
                name="name_value",
                revision_id="revision_id_value",
                version_tag="version_tag_value",
                display_name="display_name_value",
                type_=resources.PhraseMatcher.PhraseMatcherType.ALL_OF,
                active=True,
                role_match=resources.ConversationParticipant.Role.HUMAN_AGENT,
            )
        )
        response = await client.update_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdatePhraseMatcherRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PhraseMatcher)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.version_tag == "version_tag_value"
    assert response.display_name == "display_name_value"
    assert response.type_ == resources.PhraseMatcher.PhraseMatcherType.ALL_OF
    assert response.active is True
    assert response.role_match == resources.ConversationParticipant.Role.HUMAN_AGENT


@pytest.mark.asyncio
async def test_update_phrase_matcher_async_from_dict():
    await test_update_phrase_matcher_async(request_type=dict)


def test_update_phrase_matcher_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdatePhraseMatcherRequest()

    request.phrase_matcher.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        call.return_value = resources.PhraseMatcher()
        client.update_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "phrase_matcher.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_phrase_matcher_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdatePhraseMatcherRequest()

    request.phrase_matcher.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        await client.update_phrase_matcher(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "phrase_matcher.name=name_value",
    ) in kw["metadata"]


def test_update_phrase_matcher_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_phrase_matcher(
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_matcher
        mock_val = resources.PhraseMatcher(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_phrase_matcher_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_phrase_matcher(
            contact_center_insights.UpdatePhraseMatcherRequest(),
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_phrase_matcher_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_matcher), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PhraseMatcher()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.PhraseMatcher()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_phrase_matcher(
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_matcher
        mock_val = resources.PhraseMatcher(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_phrase_matcher_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_phrase_matcher(
            contact_center_insights.UpdatePhraseMatcherRequest(),
            phrase_matcher=resources.PhraseMatcher(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CalculateStatsRequest,
        dict,
    ],
)
def test_calculate_stats(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateStatsResponse(
            average_turn_count=1931,
            conversation_count=1955,
        )
        response = client.calculate_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.CalculateStatsResponse)
    assert response.average_turn_count == 1931
    assert response.conversation_count == 1955


def test_calculate_stats_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        client.calculate_stats()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateStatsRequest()


@pytest.mark.asyncio
async def test_calculate_stats_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CalculateStatsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateStatsResponse(
                average_turn_count=1931,
                conversation_count=1955,
            )
        )
        response = await client.calculate_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CalculateStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, contact_center_insights.CalculateStatsResponse)
    assert response.average_turn_count == 1931
    assert response.conversation_count == 1955


@pytest.mark.asyncio
async def test_calculate_stats_async_from_dict():
    await test_calculate_stats_async(request_type=dict)


def test_calculate_stats_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CalculateStatsRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        call.return_value = contact_center_insights.CalculateStatsResponse()
        client.calculate_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_calculate_stats_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CalculateStatsRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateStatsResponse()
        )
        await client.calculate_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_calculate_stats_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateStatsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.calculate_stats(
            location="location_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val


def test_calculate_stats_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.calculate_stats(
            contact_center_insights.CalculateStatsRequest(),
            location="location_value",
        )


@pytest.mark.asyncio
async def test_calculate_stats_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.calculate_stats), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.CalculateStatsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.CalculateStatsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.calculate_stats(
            location="location_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_calculate_stats_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.calculate_stats(
            contact_center_insights.CalculateStatsRequest(),
            location="location_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetSettingsRequest,
        dict,
    ],
)
def test_get_settings(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings(
            name="name_value",
            language_code="language_code_value",
        )
        response = client.get_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Settings)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"


def test_get_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        client.get_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetSettingsRequest()


@pytest.mark.asyncio
async def test_get_settings_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.GetSettingsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Settings(
                name="name_value",
                language_code="language_code_value",
            )
        )
        response = await client.get_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Settings)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"


@pytest.mark.asyncio
async def test_get_settings_async_from_dict():
    await test_get_settings_async(request_type=dict)


def test_get_settings_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        call.return_value = resources.Settings()
        client.get_settings(request)

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
async def test_get_settings_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetSettingsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Settings())
        await client.get_settings(request)

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


def test_get_settings_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_settings(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_settings_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_settings(
            contact_center_insights.GetSettingsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_settings_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Settings())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_settings(
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
async def test_get_settings_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_settings(
            contact_center_insights.GetSettingsRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdateSettingsRequest,
        dict,
    ],
)
def test_update_settings(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings(
            name="name_value",
            language_code="language_code_value",
        )
        response = client.update_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Settings)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"


def test_update_settings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        client.update_settings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateSettingsRequest()


@pytest.mark.asyncio
async def test_update_settings_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdateSettingsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Settings(
                name="name_value",
                language_code="language_code_value",
            )
        )
        response = await client.update_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateSettingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Settings)
    assert response.name == "name_value"
    assert response.language_code == "language_code_value"


@pytest.mark.asyncio
async def test_update_settings_async_from_dict():
    await test_update_settings_async(request_type=dict)


def test_update_settings_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateSettingsRequest()

    request.settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        call.return_value = resources.Settings()
        client.update_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "settings.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_settings_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateSettingsRequest()

    request.settings.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Settings())
        await client.update_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "settings.name=name_value",
    ) in kw["metadata"]


def test_update_settings_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_settings(
            settings=resources.Settings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].settings
        mock_val = resources.Settings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_settings_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_settings(
            contact_center_insights.UpdateSettingsRequest(),
            settings=resources.Settings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_settings_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_settings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Settings()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Settings())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_settings(
            settings=resources.Settings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].settings
        mock_val = resources.Settings(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_settings_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_settings(
            contact_center_insights.UpdateSettingsRequest(),
            settings=resources.Settings(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.CreateViewRequest,
        dict,
    ],
)
def test_create_view(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View(
            name="name_value",
            display_name="display_name_value",
            value="value_value",
        )
        response = client.create_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


def test_create_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        client.create_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateViewRequest()


@pytest.mark.asyncio
async def test_create_view_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.CreateViewRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.View(
                name="name_value",
                display_name="display_name_value",
                value="value_value",
            )
        )
        response = await client.create_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.CreateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


@pytest.mark.asyncio
async def test_create_view_async_from_dict():
    await test_create_view_async(request_type=dict)


def test_create_view_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateViewRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        call.return_value = resources.View()
        client.create_view(request)

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
async def test_create_view_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.CreateViewRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        await client.create_view(request)

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


def test_create_view_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_view(
            parent="parent_value",
            view=resources.View(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].view
        mock_val = resources.View(name="name_value")
        assert arg == mock_val


def test_create_view_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_view(
            contact_center_insights.CreateViewRequest(),
            parent="parent_value",
            view=resources.View(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_view_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_view(
            parent="parent_value",
            view=resources.View(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].view
        mock_val = resources.View(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_view_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_view(
            contact_center_insights.CreateViewRequest(),
            parent="parent_value",
            view=resources.View(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.GetViewRequest,
        dict,
    ],
)
def test_get_view(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View(
            name="name_value",
            display_name="display_name_value",
            value="value_value",
        )
        response = client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


def test_get_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        client.get_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetViewRequest()


@pytest.mark.asyncio
async def test_get_view_async(
    transport: str = "grpc_asyncio", request_type=contact_center_insights.GetViewRequest
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.View(
                name="name_value",
                display_name="display_name_value",
                value="value_value",
            )
        )
        response = await client.get_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.GetViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


@pytest.mark.asyncio
async def test_get_view_async_from_dict():
    await test_get_view_async(request_type=dict)


def test_get_view_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetViewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        call.return_value = resources.View()
        client.get_view(request)

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
async def test_get_view_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.GetViewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        await client.get_view(request)

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


def test_get_view_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_view(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_view_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_view(
            contact_center_insights.GetViewRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_view_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_view(
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
async def test_get_view_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_view(
            contact_center_insights.GetViewRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.ListViewsRequest,
        dict,
    ],
)
def test_list_views(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListViewsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_views(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListViewsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListViewsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_views_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        client.list_views()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListViewsRequest()


@pytest.mark.asyncio
async def test_list_views_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.ListViewsRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListViewsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_views(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.ListViewsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListViewsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_views_async_from_dict():
    await test_list_views_async(request_type=dict)


def test_list_views_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListViewsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        call.return_value = contact_center_insights.ListViewsResponse()
        client.list_views(request)

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
async def test_list_views_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.ListViewsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListViewsResponse()
        )
        await client.list_views(request)

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


def test_list_views_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListViewsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_views(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_views_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_views(
            contact_center_insights.ListViewsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_views_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = contact_center_insights.ListViewsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            contact_center_insights.ListViewsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_views(
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
async def test_list_views_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_views(
            contact_center_insights.ListViewsRequest(),
            parent="parent_value",
        )


def test_list_views_pager(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                    resources.View(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListViewsResponse(
                views=[],
                next_page_token="def",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_views(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.View) for i in results)


def test_list_views_pages(transport_name: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_views), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                    resources.View(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListViewsResponse(
                views=[],
                next_page_token="def",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_views(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_views_async_pager():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_views), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                    resources.View(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListViewsResponse(
                views=[],
                next_page_token="def",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_views(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.View) for i in responses)


@pytest.mark.asyncio
async def test_list_views_async_pages():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_views), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                    resources.View(),
                ],
                next_page_token="abc",
            ),
            contact_center_insights.ListViewsResponse(
                views=[],
                next_page_token="def",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                ],
                next_page_token="ghi",
            ),
            contact_center_insights.ListViewsResponse(
                views=[
                    resources.View(),
                    resources.View(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_views(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.UpdateViewRequest,
        dict,
    ],
)
def test_update_view(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View(
            name="name_value",
            display_name="display_name_value",
            value="value_value",
        )
        response = client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


def test_update_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        client.update_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateViewRequest()


@pytest.mark.asyncio
async def test_update_view_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.UpdateViewRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.View(
                name="name_value",
                display_name="display_name_value",
                value="value_value",
            )
        )
        response = await client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.UpdateViewRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.View)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.value == "value_value"


@pytest.mark.asyncio
async def test_update_view_async_from_dict():
    await test_update_view_async(request_type=dict)


def test_update_view_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateViewRequest()

    request.view.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        call.return_value = resources.View()
        client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "view.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_view_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.UpdateViewRequest()

    request.view.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        await client.update_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "view.name=name_value",
    ) in kw["metadata"]


def test_update_view_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_view(
            view=resources.View(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].view
        mock_val = resources.View(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_view_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_view(
            contact_center_insights.UpdateViewRequest(),
            view=resources.View(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_view_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.View()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.View())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_view(
            view=resources.View(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].view
        mock_val = resources.View(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_view_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_view(
            contact_center_insights.UpdateViewRequest(),
            view=resources.View(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        contact_center_insights.DeleteViewRequest,
        dict,
    ],
)
def test_delete_view(request_type, transport: str = "grpc"):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteViewRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_view_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        client.delete_view()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteViewRequest()


@pytest.mark.asyncio
async def test_delete_view_async(
    transport: str = "grpc_asyncio",
    request_type=contact_center_insights.DeleteViewRequest,
):
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_view(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == contact_center_insights.DeleteViewRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_view_async_from_dict():
    await test_delete_view_async(request_type=dict)


def test_delete_view_field_headers():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteViewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        call.return_value = None
        client.delete_view(request)

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
async def test_delete_view_field_headers_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = contact_center_insights.DeleteViewRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_view(request)

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


def test_delete_view_flattened():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_view(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_view_flattened_error():
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_view(
            contact_center_insights.DeleteViewRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_view_flattened_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_view), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_view(
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
async def test_delete_view_flattened_error_async():
    client = ContactCenterInsightsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_view(
            contact_center_insights.DeleteViewRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ContactCenterInsightsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ContactCenterInsightsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ContactCenterInsightsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ContactCenterInsightsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ContactCenterInsightsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ContactCenterInsightsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ContactCenterInsightsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ContactCenterInsightsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
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
    transport = ContactCenterInsightsClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ContactCenterInsightsGrpcTransport,
    )


def test_contact_center_insights_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ContactCenterInsightsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_contact_center_insights_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.contact_center_insights_v1.services.contact_center_insights.transports.ContactCenterInsightsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ContactCenterInsightsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_conversation",
        "update_conversation",
        "get_conversation",
        "list_conversations",
        "delete_conversation",
        "create_analysis",
        "get_analysis",
        "list_analyses",
        "delete_analysis",
        "export_insights_data",
        "create_issue_model",
        "update_issue_model",
        "get_issue_model",
        "list_issue_models",
        "delete_issue_model",
        "deploy_issue_model",
        "undeploy_issue_model",
        "get_issue",
        "list_issues",
        "update_issue",
        "calculate_issue_model_stats",
        "create_phrase_matcher",
        "get_phrase_matcher",
        "list_phrase_matchers",
        "delete_phrase_matcher",
        "update_phrase_matcher",
        "calculate_stats",
        "get_settings",
        "update_settings",
        "create_view",
        "get_view",
        "list_views",
        "update_view",
        "delete_view",
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


def test_contact_center_insights_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.contact_center_insights_v1.services.contact_center_insights.transports.ContactCenterInsightsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ContactCenterInsightsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_contact_center_insights_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.contact_center_insights_v1.services.contact_center_insights.transports.ContactCenterInsightsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ContactCenterInsightsTransport()
        adc.assert_called_once()


def test_contact_center_insights_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ContactCenterInsightsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
    ],
)
def test_contact_center_insights_transport_auth_adc(transport_class):
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
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
    ],
)
def test_contact_center_insights_transport_auth_gdch_credentials(transport_class):
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
        (transports.ContactCenterInsightsGrpcTransport, grpc_helpers),
        (transports.ContactCenterInsightsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_contact_center_insights_transport_create_channel(
    transport_class, grpc_helpers
):
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
            "contactcenterinsights.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="contactcenterinsights.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
    ],
)
def test_contact_center_insights_grpc_transport_client_cert_source_for_mtls(
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


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_contact_center_insights_host_no_port(transport_name):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="contactcenterinsights.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("contactcenterinsights.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_contact_center_insights_host_with_port(transport_name):
    client = ContactCenterInsightsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="contactcenterinsights.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("contactcenterinsights.googleapis.com:8000")


def test_contact_center_insights_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ContactCenterInsightsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_contact_center_insights_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ContactCenterInsightsGrpcAsyncIOTransport(
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
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
    ],
)
def test_contact_center_insights_transport_channel_mtls_with_client_cert_source(
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
        transports.ContactCenterInsightsGrpcTransport,
        transports.ContactCenterInsightsGrpcAsyncIOTransport,
    ],
)
def test_contact_center_insights_transport_channel_mtls_with_adc(transport_class):
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


def test_contact_center_insights_grpc_lro_client():
    client = ContactCenterInsightsClient(
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


def test_contact_center_insights_grpc_lro_async_client():
    client = ContactCenterInsightsAsyncClient(
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


def test_analysis_path():
    project = "squid"
    location = "clam"
    conversation = "whelk"
    analysis = "octopus"
    expected = "projects/{project}/locations/{location}/conversations/{conversation}/analyses/{analysis}".format(
        project=project,
        location=location,
        conversation=conversation,
        analysis=analysis,
    )
    actual = ContactCenterInsightsClient.analysis_path(
        project, location, conversation, analysis
    )
    assert expected == actual


def test_parse_analysis_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "conversation": "cuttlefish",
        "analysis": "mussel",
    }
    path = ContactCenterInsightsClient.analysis_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_analysis_path(path)
    assert expected == actual


def test_conversation_path():
    project = "winkle"
    location = "nautilus"
    conversation = "scallop"
    expected = (
        "projects/{project}/locations/{location}/conversations/{conversation}".format(
            project=project,
            location=location,
            conversation=conversation,
        )
    )
    actual = ContactCenterInsightsClient.conversation_path(
        project, location, conversation
    )
    assert expected == actual


def test_parse_conversation_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "conversation": "clam",
    }
    path = ContactCenterInsightsClient.conversation_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_conversation_path(path)
    assert expected == actual


def test_issue_path():
    project = "whelk"
    location = "octopus"
    issue_model = "oyster"
    issue = "nudibranch"
    expected = "projects/{project}/locations/{location}/issueModels/{issue_model}/issues/{issue}".format(
        project=project,
        location=location,
        issue_model=issue_model,
        issue=issue,
    )
    actual = ContactCenterInsightsClient.issue_path(
        project, location, issue_model, issue
    )
    assert expected == actual


def test_parse_issue_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "issue_model": "winkle",
        "issue": "nautilus",
    }
    path = ContactCenterInsightsClient.issue_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_issue_path(path)
    assert expected == actual


def test_issue_model_path():
    project = "scallop"
    location = "abalone"
    issue_model = "squid"
    expected = (
        "projects/{project}/locations/{location}/issueModels/{issue_model}".format(
            project=project,
            location=location,
            issue_model=issue_model,
        )
    )
    actual = ContactCenterInsightsClient.issue_model_path(
        project, location, issue_model
    )
    assert expected == actual


def test_parse_issue_model_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "issue_model": "octopus",
    }
    path = ContactCenterInsightsClient.issue_model_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_issue_model_path(path)
    assert expected == actual


def test_participant_path():
    project = "oyster"
    conversation = "nudibranch"
    participant = "cuttlefish"
    expected = "projects/{project}/conversations/{conversation}/participants/{participant}".format(
        project=project,
        conversation=conversation,
        participant=participant,
    )
    actual = ContactCenterInsightsClient.participant_path(
        project, conversation, participant
    )
    assert expected == actual


def test_parse_participant_path():
    expected = {
        "project": "mussel",
        "conversation": "winkle",
        "participant": "nautilus",
    }
    path = ContactCenterInsightsClient.participant_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_participant_path(path)
    assert expected == actual


def test_phrase_matcher_path():
    project = "scallop"
    location = "abalone"
    phrase_matcher = "squid"
    expected = "projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher}".format(
        project=project,
        location=location,
        phrase_matcher=phrase_matcher,
    )
    actual = ContactCenterInsightsClient.phrase_matcher_path(
        project, location, phrase_matcher
    )
    assert expected == actual


def test_parse_phrase_matcher_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "phrase_matcher": "octopus",
    }
    path = ContactCenterInsightsClient.phrase_matcher_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_phrase_matcher_path(path)
    assert expected == actual


def test_settings_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}/settings".format(
        project=project,
        location=location,
    )
    actual = ContactCenterInsightsClient.settings_path(project, location)
    assert expected == actual


def test_parse_settings_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = ContactCenterInsightsClient.settings_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_settings_path(path)
    assert expected == actual


def test_view_path():
    project = "winkle"
    location = "nautilus"
    view = "scallop"
    expected = "projects/{project}/locations/{location}/views/{view}".format(
        project=project,
        location=location,
        view=view,
    )
    actual = ContactCenterInsightsClient.view_path(project, location, view)
    assert expected == actual


def test_parse_view_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "view": "clam",
    }
    path = ContactCenterInsightsClient.view_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_view_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ContactCenterInsightsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = ContactCenterInsightsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ContactCenterInsightsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = ContactCenterInsightsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ContactCenterInsightsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = ContactCenterInsightsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ContactCenterInsightsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = ContactCenterInsightsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ContactCenterInsightsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = ContactCenterInsightsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ContactCenterInsightsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ContactCenterInsightsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ContactCenterInsightsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ContactCenterInsightsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ContactCenterInsightsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ContactCenterInsightsAsyncClient(
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
        client = ContactCenterInsightsClient(
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
        client = ContactCenterInsightsClient(
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
        (ContactCenterInsightsClient, transports.ContactCenterInsightsGrpcTransport),
        (
            ContactCenterInsightsAsyncClient,
            transports.ContactCenterInsightsGrpcAsyncIOTransport,
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
