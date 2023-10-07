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
from google.cloud.eventarc_v1.services.eventarc import EventarcAsyncClient
from google.cloud.eventarc_v1.services.eventarc import EventarcClient
from google.cloud.eventarc_v1.services.eventarc import pagers
from google.cloud.eventarc_v1.services.eventarc import transports
from google.cloud.eventarc_v1.types import channel
from google.cloud.eventarc_v1.types import channel as gce_channel
from google.cloud.eventarc_v1.types import channel_connection
from google.cloud.eventarc_v1.types import channel_connection as gce_channel_connection
from google.cloud.eventarc_v1.types import discovery
from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import google_channel_config
from google.cloud.eventarc_v1.types import google_channel_config as gce_google_channel_config
from google.cloud.eventarc_v1.types import trigger
from google.cloud.eventarc_v1.types import trigger as gce_trigger
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert EventarcClient._get_default_mtls_endpoint(None) is None
    assert EventarcClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert EventarcClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert EventarcClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert EventarcClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert EventarcClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (EventarcClient, "grpc"),
    (EventarcAsyncClient, "grpc_asyncio"),
    (EventarcClient, "rest"),
])
def test_eventarc_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'eventarc.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://eventarc.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.EventarcGrpcTransport, "grpc"),
    (transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.EventarcRestTransport, "rest"),
])
def test_eventarc_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (EventarcClient, "grpc"),
    (EventarcAsyncClient, "grpc_asyncio"),
    (EventarcClient, "rest"),
])
def test_eventarc_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'eventarc.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://eventarc.googleapis.com'
        )


def test_eventarc_client_get_transport_class():
    transport = EventarcClient.get_transport_class()
    available_transports = [
        transports.EventarcGrpcTransport,
        transports.EventarcRestTransport,
    ]
    assert transport in available_transports

    transport = EventarcClient.get_transport_class("grpc")
    assert transport == transports.EventarcGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (EventarcClient, transports.EventarcGrpcTransport, "grpc"),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio"),
    (EventarcClient, transports.EventarcRestTransport, "rest"),
])
@mock.patch.object(EventarcClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcClient))
@mock.patch.object(EventarcAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcAsyncClient))
def test_eventarc_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(EventarcClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(EventarcClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
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
        with mock.patch.object(transport_class, '__init__') as patched:
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
        with mock.patch.object(transport_class, '__init__') as patched:
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
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
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
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
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
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (EventarcClient, transports.EventarcGrpcTransport, "grpc", "true"),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (EventarcClient, transports.EventarcGrpcTransport, "grpc", "false"),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (EventarcClient, transports.EventarcRestTransport, "rest", "true"),
    (EventarcClient, transports.EventarcRestTransport, "rest", "false"),
])
@mock.patch.object(EventarcClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcClient))
@mock.patch.object(EventarcAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_eventarc_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
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
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
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
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
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


@pytest.mark.parametrize("client_class", [
    EventarcClient, EventarcAsyncClient
])
@mock.patch.object(EventarcClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcClient))
@mock.patch.object(EventarcAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(EventarcAsyncClient))
def test_eventarc_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
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
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (EventarcClient, transports.EventarcGrpcTransport, "grpc"),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio"),
    (EventarcClient, transports.EventarcRestTransport, "rest"),
])
def test_eventarc_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
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

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (EventarcClient, transports.EventarcGrpcTransport, "grpc", grpc_helpers),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (EventarcClient, transports.EventarcRestTransport, "rest", None),
])
def test_eventarc_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
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

def test_eventarc_client_client_options_from_dict():
    with mock.patch('google.cloud.eventarc_v1.services.eventarc.transports.EventarcGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = EventarcClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
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


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (EventarcClient, transports.EventarcGrpcTransport, "grpc", grpc_helpers),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_eventarc_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
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
            "eventarc.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="eventarc.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  eventarc.GetTriggerRequest,
  dict,
])
def test_get_trigger(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = trigger.Trigger(
            name='name_value',
            uid='uid_value',
            service_account='service_account_value',
            channel='channel_value',
            etag='etag_value',
        )
        response = client.get_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, trigger.Trigger)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.service_account == 'service_account_value'
    assert response.channel == 'channel_value'
    assert response.etag == 'etag_value'


def test_get_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        client.get_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetTriggerRequest()

@pytest.mark.asyncio
async def test_get_trigger_async(transport: str = 'grpc_asyncio', request_type=eventarc.GetTriggerRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(trigger.Trigger(
            name='name_value',
            uid='uid_value',
            service_account='service_account_value',
            channel='channel_value',
            etag='etag_value',
        ))
        response = await client.get_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, trigger.Trigger)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.service_account == 'service_account_value'
    assert response.channel == 'channel_value'
    assert response.etag == 'etag_value'


@pytest.mark.asyncio
async def test_get_trigger_async_from_dict():
    await test_get_trigger_async(request_type=dict)


def test_get_trigger_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetTriggerRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        call.return_value = trigger.Trigger()
        client.get_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_trigger_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetTriggerRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(trigger.Trigger())
        await client.get_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_trigger_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = trigger.Trigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_trigger(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_trigger_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_trigger(
            eventarc.GetTriggerRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_trigger_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = trigger.Trigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(trigger.Trigger())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_trigger(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_trigger_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_trigger(
            eventarc.GetTriggerRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.ListTriggersRequest,
  dict,
])
def test_list_triggers(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListTriggersResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTriggersPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_triggers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        client.list_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListTriggersRequest()

@pytest.mark.asyncio
async def test_list_triggers_async(transport: str = 'grpc_asyncio', request_type=eventarc.ListTriggersRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListTriggersResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTriggersAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_triggers_async_from_dict():
    await test_list_triggers_async(request_type=dict)


def test_list_triggers_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListTriggersRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        call.return_value = eventarc.ListTriggersResponse()
        client.list_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_triggers_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListTriggersRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListTriggersResponse())
        await client.list_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_triggers_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListTriggersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_triggers(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_triggers_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_triggers(
            eventarc.ListTriggersRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_triggers_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListTriggersResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_triggers(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_triggers_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_triggers(
            eventarc.ListTriggersRequest(),
            parent='parent_value',
        )


def test_list_triggers_pager(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListTriggersResponse(
                triggers=[],
                next_page_token='def',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_triggers(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, trigger.Trigger)
                   for i in results)
def test_list_triggers_pages(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListTriggersResponse(
                triggers=[],
                next_page_token='def',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_triggers(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_triggers_async_pager():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListTriggersResponse(
                triggers=[],
                next_page_token='def',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_triggers(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, trigger.Trigger)
                for i in responses)


@pytest.mark.asyncio
async def test_list_triggers_async_pages():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_triggers),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListTriggersResponse(
                triggers=[],
                next_page_token='def',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_triggers(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  eventarc.CreateTriggerRequest,
  dict,
])
def test_create_trigger(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        client.create_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateTriggerRequest()

@pytest.mark.asyncio
async def test_create_trigger_async(transport: str = 'grpc_asyncio', request_type=eventarc.CreateTriggerRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_trigger_async_from_dict():
    await test_create_trigger_async(request_type=dict)


def test_create_trigger_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateTriggerRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_trigger_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateTriggerRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_trigger_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_trigger(
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = gce_trigger.Trigger(name='name_value')
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = 'trigger_id_value'
        assert arg == mock_val


def test_create_trigger_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_trigger(
            eventarc.CreateTriggerRequest(),
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )

@pytest.mark.asyncio
async def test_create_trigger_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_trigger(
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = gce_trigger.Trigger(name='name_value')
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = 'trigger_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_trigger_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_trigger(
            eventarc.CreateTriggerRequest(),
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.UpdateTriggerRequest,
  dict,
])
def test_update_trigger(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        client.update_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateTriggerRequest()

@pytest.mark.asyncio
async def test_update_trigger_async(transport: str = 'grpc_asyncio', request_type=eventarc.UpdateTriggerRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_trigger_async_from_dict():
    await test_update_trigger_async(request_type=dict)


def test_update_trigger_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateTriggerRequest()

    request.trigger.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'trigger.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_trigger_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateTriggerRequest()

    request.trigger.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'trigger.name=name_value',
    ) in kw['metadata']


def test_update_trigger_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_trigger(
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].trigger
        mock_val = gce_trigger.Trigger(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val
        arg = args[0].allow_missing
        mock_val = True
        assert arg == mock_val


def test_update_trigger_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_trigger(
            eventarc.UpdateTriggerRequest(),
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )

@pytest.mark.asyncio
async def test_update_trigger_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_trigger(
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].trigger
        mock_val = gce_trigger.Trigger(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val
        arg = args[0].allow_missing
        mock_val = True
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_trigger_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_trigger(
            eventarc.UpdateTriggerRequest(),
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )


@pytest.mark.parametrize("request_type", [
  eventarc.DeleteTriggerRequest,
  dict,
])
def test_delete_trigger(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        client.delete_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteTriggerRequest()

@pytest.mark.asyncio
async def test_delete_trigger_async(transport: str = 'grpc_asyncio', request_type=eventarc.DeleteTriggerRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_trigger_async_from_dict():
    await test_delete_trigger_async(request_type=dict)


def test_delete_trigger_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteTriggerRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_trigger_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteTriggerRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_trigger_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_trigger(
            name='name_value',
            allow_missing=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].allow_missing
        mock_val = True
        assert arg == mock_val


def test_delete_trigger_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_trigger(
            eventarc.DeleteTriggerRequest(),
            name='name_value',
            allow_missing=True,
        )

@pytest.mark.asyncio
async def test_delete_trigger_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_trigger),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_trigger(
            name='name_value',
            allow_missing=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].allow_missing
        mock_val = True
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_trigger_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_trigger(
            eventarc.DeleteTriggerRequest(),
            name='name_value',
            allow_missing=True,
        )


@pytest.mark.parametrize("request_type", [
  eventarc.GetChannelRequest,
  dict,
])
def test_get_channel(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel.Channel(
            name='name_value',
            uid='uid_value',
            provider='provider_value',
            state=channel.Channel.State.PENDING,
            activation_token='activation_token_value',
            crypto_key_name='crypto_key_name_value',
            pubsub_topic='pubsub_topic_value',
        )
        response = client.get_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel.Channel)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.provider == 'provider_value'
    assert response.state == channel.Channel.State.PENDING
    assert response.activation_token == 'activation_token_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_get_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        client.get_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelRequest()

@pytest.mark.asyncio
async def test_get_channel_async(transport: str = 'grpc_asyncio', request_type=eventarc.GetChannelRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(channel.Channel(
            name='name_value',
            uid='uid_value',
            provider='provider_value',
            state=channel.Channel.State.PENDING,
            activation_token='activation_token_value',
            crypto_key_name='crypto_key_name_value',
        ))
        response = await client.get_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel.Channel)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.provider == 'provider_value'
    assert response.state == channel.Channel.State.PENDING
    assert response.activation_token == 'activation_token_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


@pytest.mark.asyncio
async def test_get_channel_async_from_dict():
    await test_get_channel_async(request_type=dict)


def test_get_channel_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetChannelRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        call.return_value = channel.Channel()
        client.get_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_channel_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetChannelRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(channel.Channel())
        await client.get_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_channel_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel.Channel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_channel(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_channel_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_channel(
            eventarc.GetChannelRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_channel_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel.Channel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(channel.Channel())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_channel(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_channel_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_channel(
            eventarc.GetChannelRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.ListChannelsRequest,
  dict,
])
def test_list_channels(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_channels_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        client.list_channels()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelsRequest()

@pytest.mark.asyncio
async def test_list_channels_async(transport: str = 'grpc_asyncio', request_type=eventarc.ListChannelsRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_channels_async_from_dict():
    await test_list_channels_async(request_type=dict)


def test_list_channels_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListChannelsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        call.return_value = eventarc.ListChannelsResponse()
        client.list_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_channels_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListChannelsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelsResponse())
        await client.list_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_channels_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_channels(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_channels_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_channels(
            eventarc.ListChannelsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_channels_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_channels(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_channels_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_channels(
            eventarc.ListChannelsRequest(),
            parent='parent_value',
        )


def test_list_channels_pager(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                    channel.Channel(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelsResponse(
                channels=[],
                next_page_token='def',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_channels(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, channel.Channel)
                   for i in results)
def test_list_channels_pages(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                    channel.Channel(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelsResponse(
                channels=[],
                next_page_token='def',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_channels(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_channels_async_pager():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                    channel.Channel(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelsResponse(
                channels=[],
                next_page_token='def',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_channels(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, channel.Channel)
                for i in responses)


@pytest.mark.asyncio
async def test_list_channels_async_pages():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channels),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                    channel.Channel(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelsResponse(
                channels=[],
                next_page_token='def',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_channels(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  eventarc.CreateChannelRequest,
  dict,
])
def test_create_channel(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        client.create_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelRequest()

@pytest.mark.asyncio
async def test_create_channel_async(transport: str = 'grpc_asyncio', request_type=eventarc.CreateChannelRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_channel_async_from_dict():
    await test_create_channel_async(request_type=dict)


def test_create_channel_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateChannelRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_channel_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateChannelRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_channel_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_channel(
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].channel
        mock_val = gce_channel.Channel(name='name_value')
        assert arg == mock_val
        arg = args[0].channel_id
        mock_val = 'channel_id_value'
        assert arg == mock_val


def test_create_channel_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_channel(
            eventarc.CreateChannelRequest(),
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )

@pytest.mark.asyncio
async def test_create_channel_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_channel(
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].channel
        mock_val = gce_channel.Channel(name='name_value')
        assert arg == mock_val
        arg = args[0].channel_id
        mock_val = 'channel_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_channel_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_channel(
            eventarc.CreateChannelRequest(),
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.UpdateChannelRequest,
  dict,
])
def test_update_channel(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        client.update_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateChannelRequest()

@pytest.mark.asyncio
async def test_update_channel_async(transport: str = 'grpc_asyncio', request_type=eventarc.UpdateChannelRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_channel_async_from_dict():
    await test_update_channel_async(request_type=dict)


def test_update_channel_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateChannelRequest()

    request.channel.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'channel.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_channel_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateChannelRequest()

    request.channel.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'channel.name=name_value',
    ) in kw['metadata']


def test_update_channel_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_channel(
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].channel
        mock_val = gce_channel.Channel(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_channel_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_channel(
            eventarc.UpdateChannelRequest(),
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_channel_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_channel(
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].channel
        mock_val = gce_channel.Channel(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_channel_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_channel(
            eventarc.UpdateChannelRequest(),
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  eventarc.DeleteChannelRequest,
  dict,
])
def test_delete_channel(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        client.delete_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelRequest()

@pytest.mark.asyncio
async def test_delete_channel_async(transport: str = 'grpc_asyncio', request_type=eventarc.DeleteChannelRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_channel_async_from_dict():
    await test_delete_channel_async(request_type=dict)


def test_delete_channel_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteChannelRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_channel_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteChannelRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_channel_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_channel(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_channel_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_channel(
            eventarc.DeleteChannelRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_channel_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_channel(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_channel_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_channel(
            eventarc.DeleteChannelRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.GetProviderRequest,
  dict,
])
def test_get_provider(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = discovery.Provider(
            name='name_value',
            display_name='display_name_value',
        )
        response = client.get_provider(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetProviderRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, discovery.Provider)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'


def test_get_provider_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        client.get_provider()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetProviderRequest()

@pytest.mark.asyncio
async def test_get_provider_async(transport: str = 'grpc_asyncio', request_type=eventarc.GetProviderRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(discovery.Provider(
            name='name_value',
            display_name='display_name_value',
        ))
        response = await client.get_provider(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetProviderRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, discovery.Provider)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'


@pytest.mark.asyncio
async def test_get_provider_async_from_dict():
    await test_get_provider_async(request_type=dict)


def test_get_provider_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetProviderRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        call.return_value = discovery.Provider()
        client.get_provider(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_provider_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetProviderRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(discovery.Provider())
        await client.get_provider(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_provider_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = discovery.Provider()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_provider(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_provider_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_provider(
            eventarc.GetProviderRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_provider_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_provider),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = discovery.Provider()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(discovery.Provider())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_provider(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_provider_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_provider(
            eventarc.GetProviderRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.ListProvidersRequest,
  dict,
])
def test_list_providers(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListProvidersResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_providers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListProvidersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProvidersPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_providers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        client.list_providers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListProvidersRequest()

@pytest.mark.asyncio
async def test_list_providers_async(transport: str = 'grpc_asyncio', request_type=eventarc.ListProvidersRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListProvidersResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_providers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListProvidersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProvidersAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_providers_async_from_dict():
    await test_list_providers_async(request_type=dict)


def test_list_providers_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListProvidersRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        call.return_value = eventarc.ListProvidersResponse()
        client.list_providers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_providers_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListProvidersRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListProvidersResponse())
        await client.list_providers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_providers_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListProvidersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_providers(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_providers_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_providers(
            eventarc.ListProvidersRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_providers_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListProvidersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListProvidersResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_providers(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_providers_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_providers(
            eventarc.ListProvidersRequest(),
            parent='parent_value',
        )


def test_list_providers_pager(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                    discovery.Provider(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListProvidersResponse(
                providers=[],
                next_page_token='def',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_providers(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, discovery.Provider)
                   for i in results)
def test_list_providers_pages(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                    discovery.Provider(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListProvidersResponse(
                providers=[],
                next_page_token='def',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_providers(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_providers_async_pager():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                    discovery.Provider(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListProvidersResponse(
                providers=[],
                next_page_token='def',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_providers(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, discovery.Provider)
                for i in responses)


@pytest.mark.asyncio
async def test_list_providers_async_pages():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_providers),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                    discovery.Provider(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListProvidersResponse(
                providers=[],
                next_page_token='def',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_providers(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  eventarc.GetChannelConnectionRequest,
  dict,
])
def test_get_channel_connection(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_connection.ChannelConnection(
            name='name_value',
            uid='uid_value',
            channel='channel_value',
            activation_token='activation_token_value',
        )
        response = client.get_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_connection.ChannelConnection)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.channel == 'channel_value'
    assert response.activation_token == 'activation_token_value'


def test_get_channel_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        client.get_channel_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelConnectionRequest()

@pytest.mark.asyncio
async def test_get_channel_connection_async(transport: str = 'grpc_asyncio', request_type=eventarc.GetChannelConnectionRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(channel_connection.ChannelConnection(
            name='name_value',
            uid='uid_value',
            channel='channel_value',
            activation_token='activation_token_value',
        ))
        response = await client.get_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_connection.ChannelConnection)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.channel == 'channel_value'
    assert response.activation_token == 'activation_token_value'


@pytest.mark.asyncio
async def test_get_channel_connection_async_from_dict():
    await test_get_channel_connection_async(request_type=dict)


def test_get_channel_connection_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetChannelConnectionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        call.return_value = channel_connection.ChannelConnection()
        client.get_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_channel_connection_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetChannelConnectionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(channel_connection.ChannelConnection())
        await client.get_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_channel_connection_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_connection.ChannelConnection()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_channel_connection(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_channel_connection_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_channel_connection(
            eventarc.GetChannelConnectionRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_channel_connection_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = channel_connection.ChannelConnection()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(channel_connection.ChannelConnection())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_channel_connection(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_channel_connection_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_channel_connection(
            eventarc.GetChannelConnectionRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.ListChannelConnectionsRequest,
  dict,
])
def test_list_channel_connections(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelConnectionsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_channel_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelConnectionsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_channel_connections_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        client.list_channel_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelConnectionsRequest()

@pytest.mark.asyncio
async def test_list_channel_connections_async(transport: str = 'grpc_asyncio', request_type=eventarc.ListChannelConnectionsRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelConnectionsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_channel_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.ListChannelConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelConnectionsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_channel_connections_async_from_dict():
    await test_list_channel_connections_async(request_type=dict)


def test_list_channel_connections_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListChannelConnectionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        call.return_value = eventarc.ListChannelConnectionsResponse()
        client.list_channel_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_channel_connections_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.ListChannelConnectionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelConnectionsResponse())
        await client.list_channel_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_channel_connections_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelConnectionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_channel_connections(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_channel_connections_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_channel_connections(
            eventarc.ListChannelConnectionsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_channel_connections_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = eventarc.ListChannelConnectionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(eventarc.ListChannelConnectionsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_channel_connections(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_channel_connections_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_channel_connections(
            eventarc.ListChannelConnectionsRequest(),
            parent='parent_value',
        )


def test_list_channel_connections_pager(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[],
                next_page_token='def',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_channel_connections(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, channel_connection.ChannelConnection)
                   for i in results)
def test_list_channel_connections_pages(transport_name: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[],
                next_page_token='def',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_channel_connections(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_channel_connections_async_pager():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[],
                next_page_token='def',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_channel_connections(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, channel_connection.ChannelConnection)
                for i in responses)


@pytest.mark.asyncio
async def test_list_channel_connections_async_pages():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_channel_connections),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[],
                next_page_token='def',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_channel_connections(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  eventarc.CreateChannelConnectionRequest,
  dict,
])
def test_create_channel_connection(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_channel_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        client.create_channel_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelConnectionRequest()

@pytest.mark.asyncio
async def test_create_channel_connection_async(transport: str = 'grpc_asyncio', request_type=eventarc.CreateChannelConnectionRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.CreateChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_channel_connection_async_from_dict():
    await test_create_channel_connection_async(request_type=dict)


def test_create_channel_connection_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateChannelConnectionRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_channel_connection_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.CreateChannelConnectionRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_channel_connection_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_channel_connection(
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].channel_connection
        mock_val = gce_channel_connection.ChannelConnection(name='name_value')
        assert arg == mock_val
        arg = args[0].channel_connection_id
        mock_val = 'channel_connection_id_value'
        assert arg == mock_val


def test_create_channel_connection_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_channel_connection(
            eventarc.CreateChannelConnectionRequest(),
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )

@pytest.mark.asyncio
async def test_create_channel_connection_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_channel_connection(
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].channel_connection
        mock_val = gce_channel_connection.ChannelConnection(name='name_value')
        assert arg == mock_val
        arg = args[0].channel_connection_id
        mock_val = 'channel_connection_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_channel_connection_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_channel_connection(
            eventarc.CreateChannelConnectionRequest(),
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.DeleteChannelConnectionRequest,
  dict,
])
def test_delete_channel_connection(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_channel_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        client.delete_channel_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelConnectionRequest()

@pytest.mark.asyncio
async def test_delete_channel_connection_async(transport: str = 'grpc_asyncio', request_type=eventarc.DeleteChannelConnectionRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.DeleteChannelConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_channel_connection_async_from_dict():
    await test_delete_channel_connection_async(request_type=dict)


def test_delete_channel_connection_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteChannelConnectionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_channel_connection_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.DeleteChannelConnectionRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_channel_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_channel_connection_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_channel_connection(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_channel_connection_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_channel_connection(
            eventarc.DeleteChannelConnectionRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_channel_connection_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_channel_connection),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_channel_connection(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_channel_connection_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_channel_connection(
            eventarc.DeleteChannelConnectionRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.GetGoogleChannelConfigRequest,
  dict,
])
def test_get_google_channel_config(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = google_channel_config.GoogleChannelConfig(
            name='name_value',
            crypto_key_name='crypto_key_name_value',
        )
        response = client.get_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetGoogleChannelConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_get_google_channel_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        client.get_google_channel_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetGoogleChannelConfigRequest()

@pytest.mark.asyncio
async def test_get_google_channel_config_async(transport: str = 'grpc_asyncio', request_type=eventarc.GetGoogleChannelConfigRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(google_channel_config.GoogleChannelConfig(
            name='name_value',
            crypto_key_name='crypto_key_name_value',
        ))
        response = await client.get_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.GetGoogleChannelConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


@pytest.mark.asyncio
async def test_get_google_channel_config_async_from_dict():
    await test_get_google_channel_config_async(request_type=dict)


def test_get_google_channel_config_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetGoogleChannelConfigRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        call.return_value = google_channel_config.GoogleChannelConfig()
        client.get_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_google_channel_config_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.GetGoogleChannelConfigRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(google_channel_config.GoogleChannelConfig())
        await client.get_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_google_channel_config_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = google_channel_config.GoogleChannelConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_google_channel_config(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_google_channel_config_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_google_channel_config(
            eventarc.GetGoogleChannelConfigRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_google_channel_config_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = google_channel_config.GoogleChannelConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(google_channel_config.GoogleChannelConfig())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_google_channel_config(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_google_channel_config_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_google_channel_config(
            eventarc.GetGoogleChannelConfigRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  eventarc.UpdateGoogleChannelConfigRequest,
  dict,
])
def test_update_google_channel_config(request_type, transport: str = 'grpc'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gce_google_channel_config.GoogleChannelConfig(
            name='name_value',
            crypto_key_name='crypto_key_name_value',
        )
        response = client.update_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateGoogleChannelConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gce_google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_update_google_channel_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        client.update_google_channel_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateGoogleChannelConfigRequest()

@pytest.mark.asyncio
async def test_update_google_channel_config_async(transport: str = 'grpc_asyncio', request_type=eventarc.UpdateGoogleChannelConfigRequest):
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gce_google_channel_config.GoogleChannelConfig(
            name='name_value',
            crypto_key_name='crypto_key_name_value',
        ))
        response = await client.update_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == eventarc.UpdateGoogleChannelConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gce_google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


@pytest.mark.asyncio
async def test_update_google_channel_config_async_from_dict():
    await test_update_google_channel_config_async(request_type=dict)


def test_update_google_channel_config_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateGoogleChannelConfigRequest()

    request.google_channel_config.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        call.return_value = gce_google_channel_config.GoogleChannelConfig()
        client.update_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'google_channel_config.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_google_channel_config_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = eventarc.UpdateGoogleChannelConfigRequest()

    request.google_channel_config.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gce_google_channel_config.GoogleChannelConfig())
        await client.update_google_channel_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'google_channel_config.name=name_value',
    ) in kw['metadata']


def test_update_google_channel_config_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gce_google_channel_config.GoogleChannelConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_google_channel_config(
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].google_channel_config
        mock_val = gce_google_channel_config.GoogleChannelConfig(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_google_channel_config_flattened_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_channel_config(
            eventarc.UpdateGoogleChannelConfigRequest(),
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_google_channel_config_flattened_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_google_channel_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gce_google_channel_config.GoogleChannelConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gce_google_channel_config.GoogleChannelConfig())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_google_channel_config(
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].google_channel_config
        mock_val = gce_google_channel_config.GoogleChannelConfig(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_google_channel_config_flattened_error_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_google_channel_config(
            eventarc.UpdateGoogleChannelConfigRequest(),
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
    eventarc.GetTriggerRequest,
    dict,
])
def test_get_trigger_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = trigger.Trigger(
              name='name_value',
              uid='uid_value',
              service_account='service_account_value',
              channel='channel_value',
              etag='etag_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = trigger.Trigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_trigger(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, trigger.Trigger)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.service_account == 'service_account_value'
    assert response.channel == 'channel_value'
    assert response.etag == 'etag_value'


def test_get_trigger_rest_required_fields(request_type=eventarc.GetTriggerRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = trigger.Trigger()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = trigger.Trigger.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_trigger(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_trigger_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_trigger_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_get_trigger") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_get_trigger") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.GetTriggerRequest.pb(eventarc.GetTriggerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = trigger.Trigger.to_json(trigger.Trigger())

        request = eventarc.GetTriggerRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = trigger.Trigger()

        client.get_trigger(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_trigger_rest_bad_request(transport: str = 'rest', request_type=eventarc.GetTriggerRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_trigger(request)


def test_get_trigger_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = trigger.Trigger()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = trigger.Trigger.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/triggers/*}" % client.transport._host, args[1])


def test_get_trigger_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_trigger(
            eventarc.GetTriggerRequest(),
            name='name_value',
        )


def test_get_trigger_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.ListTriggersRequest,
    dict,
])
def test_list_triggers_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListTriggersResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListTriggersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_triggers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTriggersPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_triggers_rest_required_fields(request_type=eventarc.ListTriggersRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_triggers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_triggers._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = eventarc.ListTriggersResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = eventarc.ListTriggersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_triggers(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_triggers_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_triggers._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_triggers_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_list_triggers") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_list_triggers") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.ListTriggersRequest.pb(eventarc.ListTriggersRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = eventarc.ListTriggersResponse.to_json(eventarc.ListTriggersResponse())

        request = eventarc.ListTriggersRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = eventarc.ListTriggersResponse()

        client.list_triggers(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_triggers_rest_bad_request(transport: str = 'rest', request_type=eventarc.ListTriggersRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_triggers(request)


def test_list_triggers_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListTriggersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListTriggersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_triggers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/triggers" % client.transport._host, args[1])


def test_list_triggers_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_triggers(
            eventarc.ListTriggersRequest(),
            parent='parent_value',
        )


def test_list_triggers_rest_pager(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListTriggersResponse(
                triggers=[],
                next_page_token='def',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListTriggersResponse(
                triggers=[
                    trigger.Trigger(),
                    trigger.Trigger(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(eventarc.ListTriggersResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_triggers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, trigger.Trigger)
                for i in results)

        pages = list(client.list_triggers(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    eventarc.CreateTriggerRequest,
    dict,
])
def test_create_trigger_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["trigger"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'event_filters': [{'attribute': 'attribute_value', 'value': 'value_value', 'operator': 'operator_value'}], 'service_account': 'service_account_value', 'destination': {'cloud_run': {'service': 'service_value', 'path': 'path_value', 'region': 'region_value'}, 'cloud_function': 'cloud_function_value', 'gke': {'cluster': 'cluster_value', 'location': 'location_value', 'namespace': 'namespace_value', 'service': 'service_value', 'path': 'path_value'}, 'workflow': 'workflow_value'}, 'transport': {'pubsub': {'topic': 'topic_value', 'subscription': 'subscription_value'}}, 'labels': {}, 'channel': 'channel_value', 'conditions': {}, 'etag': 'etag_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.CreateTriggerRequest.meta.fields["trigger"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.CreateTriggerRequest.meta.fields["trigger"].message.meta.fields
    else:
        message_fields = eventarc.CreateTriggerRequest.meta.fields["trigger"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["trigger"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["trigger"][field])):
                    del request_init["trigger"][field][i][subfield]
            else:
                del request_init["trigger"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_trigger(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_trigger_rest_required_fields(request_type=eventarc.CreateTriggerRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["trigger_id"] = ""
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "triggerId" not in jsonified_request
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == request_init["trigger_id"]
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["triggerId"] = 'trigger_id_value'
    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("trigger_id", "validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "triggerId" in jsonified_request
    assert jsonified_request["triggerId"] == 'trigger_id_value'
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_trigger(request)

            expected_params = [
                (
                    "triggerId",
                    "",
                ),
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_trigger_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (set(("triggerId", "validateOnly", )) & set(("parent", "trigger", "triggerId", "validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_trigger_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_create_trigger") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_create_trigger") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.CreateTriggerRequest.pb(eventarc.CreateTriggerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.CreateTriggerRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_trigger(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_trigger_rest_bad_request(transport: str = 'rest', request_type=eventarc.CreateTriggerRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_trigger(request)


def test_create_trigger_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/triggers" % client.transport._host, args[1])


def test_create_trigger_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_trigger(
            eventarc.CreateTriggerRequest(),
            parent='parent_value',
            trigger=gce_trigger.Trigger(name='name_value'),
            trigger_id='trigger_id_value',
        )


def test_create_trigger_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.UpdateTriggerRequest,
    dict,
])
def test_update_trigger_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'trigger': {'name': 'projects/sample1/locations/sample2/triggers/sample3'}}
    request_init["trigger"] = {'name': 'projects/sample1/locations/sample2/triggers/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'event_filters': [{'attribute': 'attribute_value', 'value': 'value_value', 'operator': 'operator_value'}], 'service_account': 'service_account_value', 'destination': {'cloud_run': {'service': 'service_value', 'path': 'path_value', 'region': 'region_value'}, 'cloud_function': 'cloud_function_value', 'gke': {'cluster': 'cluster_value', 'location': 'location_value', 'namespace': 'namespace_value', 'service': 'service_value', 'path': 'path_value'}, 'workflow': 'workflow_value'}, 'transport': {'pubsub': {'topic': 'topic_value', 'subscription': 'subscription_value'}}, 'labels': {}, 'channel': 'channel_value', 'conditions': {}, 'etag': 'etag_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.UpdateTriggerRequest.meta.fields["trigger"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.UpdateTriggerRequest.meta.fields["trigger"].message.meta.fields
    else:
        message_fields = eventarc.UpdateTriggerRequest.meta.fields["trigger"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["trigger"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["trigger"][field])):
                    del request_init["trigger"][field][i][subfield]
            else:
                del request_init["trigger"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_trigger(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_trigger_rest_required_fields(request_type=eventarc.UpdateTriggerRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("allow_missing", "update_mask", "validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_trigger(request)

            expected_params = [
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_trigger_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (set(("allowMissing", "updateMask", "validateOnly", )) & set(("validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_trigger_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_update_trigger") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_update_trigger") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.UpdateTriggerRequest.pb(eventarc.UpdateTriggerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.UpdateTriggerRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_trigger(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_trigger_rest_bad_request(transport: str = 'rest', request_type=eventarc.UpdateTriggerRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'trigger': {'name': 'projects/sample1/locations/sample2/triggers/sample3'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_trigger(request)


def test_update_trigger_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'trigger': {'name': 'projects/sample1/locations/sample2/triggers/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{trigger.name=projects/*/locations/*/triggers/*}" % client.transport._host, args[1])


def test_update_trigger_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_trigger(
            eventarc.UpdateTriggerRequest(),
            trigger=gce_trigger.Trigger(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
            allow_missing=True,
        )


def test_update_trigger_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.DeleteTriggerRequest,
    dict,
])
def test_delete_trigger_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_trigger(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_trigger_rest_required_fields(request_type=eventarc.DeleteTriggerRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_trigger._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["name"] = 'name_value'
    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_trigger._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("allow_missing", "etag", "validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_trigger(request)

            expected_params = [
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_trigger_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_trigger._get_unset_required_fields({})
    assert set(unset_fields) == (set(("allowMissing", "etag", "validateOnly", )) & set(("name", "validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_trigger_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_delete_trigger") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_delete_trigger") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.DeleteTriggerRequest.pb(eventarc.DeleteTriggerRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.DeleteTriggerRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_trigger(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_trigger_rest_bad_request(transport: str = 'rest', request_type=eventarc.DeleteTriggerRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_trigger(request)


def test_delete_trigger_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/triggers/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            allow_missing=True,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_trigger(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/triggers/*}" % client.transport._host, args[1])


def test_delete_trigger_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_trigger(
            eventarc.DeleteTriggerRequest(),
            name='name_value',
            allow_missing=True,
        )


def test_delete_trigger_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.GetChannelRequest,
    dict,
])
def test_get_channel_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channels/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = channel.Channel(
              name='name_value',
              uid='uid_value',
              provider='provider_value',
              state=channel.Channel.State.PENDING,
              activation_token='activation_token_value',
              crypto_key_name='crypto_key_name_value',
            pubsub_topic='pubsub_topic_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = channel.Channel.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_channel(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel.Channel)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.provider == 'provider_value'
    assert response.state == channel.Channel.State.PENDING
    assert response.activation_token == 'activation_token_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_get_channel_rest_required_fields(request_type=eventarc.GetChannelRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_channel._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_channel._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = channel.Channel()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = channel.Channel.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_channel(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_channel_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_channel._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_channel_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_get_channel") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_get_channel") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.GetChannelRequest.pb(eventarc.GetChannelRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = channel.Channel.to_json(channel.Channel())

        request = eventarc.GetChannelRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = channel.Channel()

        client.get_channel(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_channel_rest_bad_request(transport: str = 'rest', request_type=eventarc.GetChannelRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channels/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_channel(request)


def test_get_channel_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = channel.Channel()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/channels/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = channel.Channel.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_channel(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/channels/*}" % client.transport._host, args[1])


def test_get_channel_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_channel(
            eventarc.GetChannelRequest(),
            name='name_value',
        )


def test_get_channel_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.ListChannelsRequest,
    dict,
])
def test_list_channels_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListChannelsResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListChannelsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_channels(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_channels_rest_required_fields(request_type=eventarc.ListChannelsRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_channels._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_channels._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = eventarc.ListChannelsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = eventarc.ListChannelsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_channels(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_channels_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_channels._get_unset_required_fields({})
    assert set(unset_fields) == (set(("orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_channels_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_list_channels") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_list_channels") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.ListChannelsRequest.pb(eventarc.ListChannelsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = eventarc.ListChannelsResponse.to_json(eventarc.ListChannelsResponse())

        request = eventarc.ListChannelsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = eventarc.ListChannelsResponse()

        client.list_channels(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_channels_rest_bad_request(transport: str = 'rest', request_type=eventarc.ListChannelsRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_channels(request)


def test_list_channels_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListChannelsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListChannelsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_channels(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/channels" % client.transport._host, args[1])


def test_list_channels_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_channels(
            eventarc.ListChannelsRequest(),
            parent='parent_value',
        )


def test_list_channels_rest_pager(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                    channel.Channel(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelsResponse(
                channels=[],
                next_page_token='def',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelsResponse(
                channels=[
                    channel.Channel(),
                    channel.Channel(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(eventarc.ListChannelsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_channels(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, channel.Channel)
                for i in results)

        pages = list(client.list_channels(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    eventarc.CreateChannelRequest,
    dict,
])
def test_create_channel_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["channel"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'provider': 'provider_value', 'pubsub_topic': 'pubsub_topic_value', 'state': 1, 'activation_token': 'activation_token_value', 'crypto_key_name': 'crypto_key_name_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.CreateChannelRequest.meta.fields["channel"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.CreateChannelRequest.meta.fields["channel"].message.meta.fields
    else:
        message_fields = eventarc.CreateChannelRequest.meta.fields["channel"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["channel"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["channel"][field])):
                    del request_init["channel"][field][i][subfield]
            else:
                del request_init["channel"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_channel(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_channel_rest_required_fields(request_type=eventarc.CreateChannelRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["channel_id"] = ""
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "channelId" not in jsonified_request
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_channel_._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "channelId" in jsonified_request
    assert jsonified_request["channelId"] == request_init["channel_id"]
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["channelId"] = 'channel_id_value'
    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_channel_._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("channel_id", "validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "channelId" in jsonified_request
    assert jsonified_request["channelId"] == 'channel_id_value'
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_channel(request)

            expected_params = [
                (
                    "channelId",
                    "",
                ),
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_channel_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_channel_._get_unset_required_fields({})
    assert set(unset_fields) == (set(("channelId", "validateOnly", )) & set(("parent", "channel", "channelId", "validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_channel_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_create_channel") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_create_channel") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.CreateChannelRequest.pb(eventarc.CreateChannelRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.CreateChannelRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_channel(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_channel_rest_bad_request(transport: str = 'rest', request_type=eventarc.CreateChannelRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_channel(request)


def test_create_channel_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_channel(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/channels" % client.transport._host, args[1])


def test_create_channel_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_channel(
            eventarc.CreateChannelRequest(),
            parent='parent_value',
            channel=gce_channel.Channel(name='name_value'),
            channel_id='channel_id_value',
        )


def test_create_channel_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.UpdateChannelRequest,
    dict,
])
def test_update_channel_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'channel': {'name': 'projects/sample1/locations/sample2/channels/sample3'}}
    request_init["channel"] = {'name': 'projects/sample1/locations/sample2/channels/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'provider': 'provider_value', 'pubsub_topic': 'pubsub_topic_value', 'state': 1, 'activation_token': 'activation_token_value', 'crypto_key_name': 'crypto_key_name_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.UpdateChannelRequest.meta.fields["channel"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.UpdateChannelRequest.meta.fields["channel"].message.meta.fields
    else:
        message_fields = eventarc.UpdateChannelRequest.meta.fields["channel"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["channel"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["channel"][field])):
                    del request_init["channel"][field][i][subfield]
            else:
                del request_init["channel"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_channel(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_channel_rest_required_fields(request_type=eventarc.UpdateChannelRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_channel._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_channel._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", "validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_channel(request)

            expected_params = [
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_channel_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_channel._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", "validateOnly", )) & set(("validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_channel_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_update_channel") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_update_channel") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.UpdateChannelRequest.pb(eventarc.UpdateChannelRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.UpdateChannelRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_channel(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_channel_rest_bad_request(transport: str = 'rest', request_type=eventarc.UpdateChannelRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'channel': {'name': 'projects/sample1/locations/sample2/channels/sample3'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_channel(request)


def test_update_channel_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'channel': {'name': 'projects/sample1/locations/sample2/channels/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_channel(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{channel.name=projects/*/locations/*/channels/*}" % client.transport._host, args[1])


def test_update_channel_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_channel(
            eventarc.UpdateChannelRequest(),
            channel=gce_channel.Channel(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_channel_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.DeleteChannelRequest,
    dict,
])
def test_delete_channel_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channels/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_channel(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_channel_rest_required_fields(request_type=eventarc.DeleteChannelRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["validate_only"] = False
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "validateOnly" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_channel._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == request_init["validate_only"]

    jsonified_request["name"] = 'name_value'
    jsonified_request["validateOnly"] = True

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_channel._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("validate_only", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "validateOnly" in jsonified_request
    assert jsonified_request["validateOnly"] == True

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_channel(request)

            expected_params = [
                (
                    "validateOnly",
                    str(False).lower(),
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_channel_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_channel._get_unset_required_fields({})
    assert set(unset_fields) == (set(("validateOnly", )) & set(("name", "validateOnly", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_channel_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_delete_channel") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_delete_channel") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.DeleteChannelRequest.pb(eventarc.DeleteChannelRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.DeleteChannelRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_channel(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_channel_rest_bad_request(transport: str = 'rest', request_type=eventarc.DeleteChannelRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channels/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_channel(request)


def test_delete_channel_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/channels/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_channel(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/channels/*}" % client.transport._host, args[1])


def test_delete_channel_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_channel(
            eventarc.DeleteChannelRequest(),
            name='name_value',
        )


def test_delete_channel_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.GetProviderRequest,
    dict,
])
def test_get_provider_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/providers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = discovery.Provider(
              name='name_value',
              display_name='display_name_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = discovery.Provider.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_provider(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, discovery.Provider)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'


def test_get_provider_rest_required_fields(request_type=eventarc.GetProviderRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_provider._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_provider._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = discovery.Provider()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = discovery.Provider.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_provider(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_provider_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_provider._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_provider_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_get_provider") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_get_provider") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.GetProviderRequest.pb(eventarc.GetProviderRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = discovery.Provider.to_json(discovery.Provider())

        request = eventarc.GetProviderRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = discovery.Provider()

        client.get_provider(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_provider_rest_bad_request(transport: str = 'rest', request_type=eventarc.GetProviderRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/providers/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_provider(request)


def test_get_provider_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = discovery.Provider()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/providers/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = discovery.Provider.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_provider(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/providers/*}" % client.transport._host, args[1])


def test_get_provider_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_provider(
            eventarc.GetProviderRequest(),
            name='name_value',
        )


def test_get_provider_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.ListProvidersRequest,
    dict,
])
def test_list_providers_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListProvidersResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListProvidersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_providers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProvidersPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_providers_rest_required_fields(request_type=eventarc.ListProvidersRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_providers._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_providers._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = eventarc.ListProvidersResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = eventarc.ListProvidersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_providers(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_providers_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_providers._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_providers_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_list_providers") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_list_providers") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.ListProvidersRequest.pb(eventarc.ListProvidersRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = eventarc.ListProvidersResponse.to_json(eventarc.ListProvidersResponse())

        request = eventarc.ListProvidersRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = eventarc.ListProvidersResponse()

        client.list_providers(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_providers_rest_bad_request(transport: str = 'rest', request_type=eventarc.ListProvidersRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_providers(request)


def test_list_providers_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListProvidersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListProvidersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_providers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/providers" % client.transport._host, args[1])


def test_list_providers_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_providers(
            eventarc.ListProvidersRequest(),
            parent='parent_value',
        )


def test_list_providers_rest_pager(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                    discovery.Provider(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListProvidersResponse(
                providers=[],
                next_page_token='def',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListProvidersResponse(
                providers=[
                    discovery.Provider(),
                    discovery.Provider(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(eventarc.ListProvidersResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_providers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, discovery.Provider)
                for i in results)

        pages = list(client.list_providers(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    eventarc.GetChannelConnectionRequest,
    dict,
])
def test_get_channel_connection_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = channel_connection.ChannelConnection(
              name='name_value',
              uid='uid_value',
              channel='channel_value',
              activation_token='activation_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = channel_connection.ChannelConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_channel_connection(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, channel_connection.ChannelConnection)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.channel == 'channel_value'
    assert response.activation_token == 'activation_token_value'


def test_get_channel_connection_rest_required_fields(request_type=eventarc.GetChannelConnectionRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_channel_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_channel_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = channel_connection.ChannelConnection()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = channel_connection.ChannelConnection.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_channel_connection(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_channel_connection_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_channel_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_channel_connection_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_get_channel_connection") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_get_channel_connection") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.GetChannelConnectionRequest.pb(eventarc.GetChannelConnectionRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = channel_connection.ChannelConnection.to_json(channel_connection.ChannelConnection())

        request = eventarc.GetChannelConnectionRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = channel_connection.ChannelConnection()

        client.get_channel_connection(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_channel_connection_rest_bad_request(transport: str = 'rest', request_type=eventarc.GetChannelConnectionRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_channel_connection(request)


def test_get_channel_connection_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = channel_connection.ChannelConnection()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = channel_connection.ChannelConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_channel_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/channelConnections/*}" % client.transport._host, args[1])


def test_get_channel_connection_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_channel_connection(
            eventarc.GetChannelConnectionRequest(),
            name='name_value',
        )


def test_get_channel_connection_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.ListChannelConnectionsRequest,
    dict,
])
def test_list_channel_connections_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListChannelConnectionsResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListChannelConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_channel_connections(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListChannelConnectionsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_channel_connections_rest_required_fields(request_type=eventarc.ListChannelConnectionsRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_channel_connections._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_channel_connections._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = eventarc.ListChannelConnectionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = eventarc.ListChannelConnectionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_channel_connections(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_channel_connections_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_channel_connections._get_unset_required_fields({})
    assert set(unset_fields) == (set(("pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_channel_connections_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_list_channel_connections") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_list_channel_connections") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.ListChannelConnectionsRequest.pb(eventarc.ListChannelConnectionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = eventarc.ListChannelConnectionsResponse.to_json(eventarc.ListChannelConnectionsResponse())

        request = eventarc.ListChannelConnectionsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = eventarc.ListChannelConnectionsResponse()

        client.list_channel_connections(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_channel_connections_rest_bad_request(transport: str = 'rest', request_type=eventarc.ListChannelConnectionsRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_channel_connections(request)


def test_list_channel_connections_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = eventarc.ListChannelConnectionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = eventarc.ListChannelConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_channel_connections(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/channelConnections" % client.transport._host, args[1])


def test_list_channel_connections_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_channel_connections(
            eventarc.ListChannelConnectionsRequest(),
            parent='parent_value',
        )


def test_list_channel_connections_rest_pager(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='abc',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[],
                next_page_token='def',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                ],
                next_page_token='ghi',
            ),
            eventarc.ListChannelConnectionsResponse(
                channel_connections=[
                    channel_connection.ChannelConnection(),
                    channel_connection.ChannelConnection(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(eventarc.ListChannelConnectionsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_channel_connections(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, channel_connection.ChannelConnection)
                for i in results)

        pages = list(client.list_channel_connections(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    eventarc.CreateChannelConnectionRequest,
    dict,
])
def test_create_channel_connection_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["channel_connection"] = {'name': 'name_value', 'uid': 'uid_value', 'channel': 'channel_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'activation_token': 'activation_token_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.CreateChannelConnectionRequest.meta.fields["channel_connection"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.CreateChannelConnectionRequest.meta.fields["channel_connection"].message.meta.fields
    else:
        message_fields = eventarc.CreateChannelConnectionRequest.meta.fields["channel_connection"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["channel_connection"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["channel_connection"][field])):
                    del request_init["channel_connection"][field][i][subfield]
            else:
                del request_init["channel_connection"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_channel_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_channel_connection_rest_required_fields(request_type=eventarc.CreateChannelConnectionRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["channel_connection_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "channelConnectionId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_channel_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "channelConnectionId" in jsonified_request
    assert jsonified_request["channelConnectionId"] == request_init["channel_connection_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["channelConnectionId"] = 'channel_connection_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_channel_connection._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("channel_connection_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "channelConnectionId" in jsonified_request
    assert jsonified_request["channelConnectionId"] == 'channel_connection_id_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_channel_connection(request)

            expected_params = [
                (
                    "channelConnectionId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_channel_connection_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_channel_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(("channelConnectionId", )) & set(("parent", "channelConnection", "channelConnectionId", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_channel_connection_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_create_channel_connection") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_create_channel_connection") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.CreateChannelConnectionRequest.pb(eventarc.CreateChannelConnectionRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.CreateChannelConnectionRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_channel_connection(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_channel_connection_rest_bad_request(transport: str = 'rest', request_type=eventarc.CreateChannelConnectionRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_channel_connection(request)


def test_create_channel_connection_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_channel_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/channelConnections" % client.transport._host, args[1])


def test_create_channel_connection_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_channel_connection(
            eventarc.CreateChannelConnectionRequest(),
            parent='parent_value',
            channel_connection=gce_channel_connection.ChannelConnection(name='name_value'),
            channel_connection_id='channel_connection_id_value',
        )


def test_create_channel_connection_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.DeleteChannelConnectionRequest,
    dict,
])
def test_delete_channel_connection_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_channel_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_channel_connection_rest_required_fields(request_type=eventarc.DeleteChannelConnectionRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_channel_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_channel_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_channel_connection(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_channel_connection_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_channel_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_channel_connection_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.EventarcRestInterceptor, "post_delete_channel_connection") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_delete_channel_connection") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.DeleteChannelConnectionRequest.pb(eventarc.DeleteChannelConnectionRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = eventarc.DeleteChannelConnectionRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_channel_connection(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_channel_connection_rest_bad_request(transport: str = 'rest', request_type=eventarc.DeleteChannelConnectionRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_channel_connection(request)


def test_delete_channel_connection_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/channelConnections/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_channel_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/channelConnections/*}" % client.transport._host, args[1])


def test_delete_channel_connection_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_channel_connection(
            eventarc.DeleteChannelConnectionRequest(),
            name='name_value',
        )


def test_delete_channel_connection_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.GetGoogleChannelConfigRequest,
    dict,
])
def test_get_google_channel_config_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = google_channel_config.GoogleChannelConfig(
              name='name_value',
              crypto_key_name='crypto_key_name_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = google_channel_config.GoogleChannelConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_google_channel_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_get_google_channel_config_rest_required_fields(request_type=eventarc.GetGoogleChannelConfigRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_google_channel_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_google_channel_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = google_channel_config.GoogleChannelConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = google_channel_config.GoogleChannelConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_google_channel_config(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_google_channel_config_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_google_channel_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_google_channel_config_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_get_google_channel_config") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_get_google_channel_config") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.GetGoogleChannelConfigRequest.pb(eventarc.GetGoogleChannelConfigRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = google_channel_config.GoogleChannelConfig.to_json(google_channel_config.GoogleChannelConfig())

        request = eventarc.GetGoogleChannelConfigRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = google_channel_config.GoogleChannelConfig()

        client.get_google_channel_config(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_google_channel_config_rest_bad_request(transport: str = 'rest', request_type=eventarc.GetGoogleChannelConfigRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_google_channel_config(request)


def test_get_google_channel_config_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = google_channel_config.GoogleChannelConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = google_channel_config.GoogleChannelConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_google_channel_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/googleChannelConfig}" % client.transport._host, args[1])


def test_get_google_channel_config_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_google_channel_config(
            eventarc.GetGoogleChannelConfigRequest(),
            name='name_value',
        )


def test_get_google_channel_config_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    eventarc.UpdateGoogleChannelConfigRequest,
    dict,
])
def test_update_google_channel_config_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'google_channel_config': {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}}
    request_init["google_channel_config"] = {'name': 'projects/sample1/locations/sample2/googleChannelConfig', 'update_time': {'seconds': 751, 'nanos': 543}, 'crypto_key_name': 'crypto_key_name_value'}
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    is_message_proto_plus_type = not hasattr(eventarc.UpdateGoogleChannelConfigRequest.meta.fields["google_channel_config"].message, "DESCRIPTOR")

    if is_message_proto_plus_type:
        message_fields = eventarc.UpdateGoogleChannelConfigRequest.meta.fields["google_channel_config"].message.meta.fields
    else:
        message_fields = eventarc.UpdateGoogleChannelConfigRequest.meta.fields["google_channel_config"].message.DESCRIPTOR.fields

    subfields_not_in_runtime = []

    # Get all subfields for the message
    runtime_nested_fields = [
        (field.name, subfield.name)
        for field in message_fields
        if hasattr(field, "message_type") and field.message_type
        for subfield in field.message_type.fields
    ]

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    for field, value in request_init["google_channel_config"].items():
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {"field": field, "subfield": subfield, "is_repeated": is_repeated}
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    for subfield_to_delete in subfields_not_in_runtime:
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["google_channel_config"][field])):
                    del request_init["google_channel_config"][field][i][subfield]
            else:
                del request_init["google_channel_config"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gce_google_channel_config.GoogleChannelConfig(
              name='name_value',
              crypto_key_name='crypto_key_name_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gce_google_channel_config.GoogleChannelConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_google_channel_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gce_google_channel_config.GoogleChannelConfig)
    assert response.name == 'name_value'
    assert response.crypto_key_name == 'crypto_key_name_value'


def test_update_google_channel_config_rest_required_fields(request_type=eventarc.UpdateGoogleChannelConfigRequest):
    transport_class = transports.EventarcRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_google_channel_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_google_channel_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gce_google_channel_config.GoogleChannelConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = gce_google_channel_config.GoogleChannelConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_google_channel_config(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_google_channel_config_rest_unset_required_fields():
    transport = transports.EventarcRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_google_channel_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("googleChannelConfig", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_google_channel_config_rest_interceptors(null_interceptor):
    transport = transports.EventarcRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.EventarcRestInterceptor(),
        )
    client = EventarcClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.EventarcRestInterceptor, "post_update_google_channel_config") as post, \
         mock.patch.object(transports.EventarcRestInterceptor, "pre_update_google_channel_config") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = eventarc.UpdateGoogleChannelConfigRequest.pb(eventarc.UpdateGoogleChannelConfigRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gce_google_channel_config.GoogleChannelConfig.to_json(gce_google_channel_config.GoogleChannelConfig())

        request = eventarc.UpdateGoogleChannelConfigRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gce_google_channel_config.GoogleChannelConfig()

        client.update_google_channel_config(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_google_channel_config_rest_bad_request(transport: str = 'rest', request_type=eventarc.UpdateGoogleChannelConfigRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'google_channel_config': {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_google_channel_config(request)


def test_update_google_channel_config_rest_flattened():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gce_google_channel_config.GoogleChannelConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {'google_channel_config': {'name': 'projects/sample1/locations/sample2/googleChannelConfig'}}

        # get truthy value for each flattened field
        mock_args = dict(
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = gce_google_channel_config.GoogleChannelConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_google_channel_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{google_channel_config.name=projects/*/locations/*/googleChannelConfig}" % client.transport._host, args[1])


def test_update_google_channel_config_rest_flattened_error(transport: str = 'rest'):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_google_channel_config(
            eventarc.UpdateGoogleChannelConfigRequest(),
            google_channel_config=gce_google_channel_config.GoogleChannelConfig(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_google_channel_config_rest_error():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EventarcClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EventarcClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EventarcClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EventarcClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EventarcClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = EventarcClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EventarcGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.EventarcGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.EventarcGrpcTransport,
    transports.EventarcGrpcAsyncIOTransport,
    transports.EventarcRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = EventarcClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.EventarcGrpcTransport,
    )

def test_eventarc_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.EventarcTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_eventarc_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.eventarc_v1.services.eventarc.transports.EventarcTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.EventarcTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'get_trigger',
        'list_triggers',
        'create_trigger',
        'update_trigger',
        'delete_trigger',
        'get_channel',
        'list_channels',
        'create_channel_',
        'update_channel',
        'delete_channel',
        'get_provider',
        'list_providers',
        'get_channel_connection',
        'list_channel_connections',
        'create_channel_connection',
        'delete_channel_connection',
        'get_google_channel_config',
        'update_google_channel_config',
        'set_iam_policy',
        'get_iam_policy',
        'test_iam_permissions',
        'get_location',
        'list_locations',
        'get_operation',
        'cancel_operation',
        'delete_operation',
        'list_operations',
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
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_eventarc_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.eventarc_v1.services.eventarc.transports.EventarcTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EventarcTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_eventarc_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.eventarc_v1.services.eventarc.transports.EventarcTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EventarcTransport()
        adc.assert_called_once()


def test_eventarc_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        EventarcClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EventarcGrpcTransport,
        transports.EventarcGrpcAsyncIOTransport,
    ],
)
def test_eventarc_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EventarcGrpcTransport,
        transports.EventarcGrpcAsyncIOTransport,
        transports.EventarcRestTransport,
    ],
)
def test_eventarc_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.EventarcGrpcTransport, grpc_helpers),
        (transports.EventarcGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_eventarc_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "eventarc.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="eventarc.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.EventarcGrpcTransport, transports.EventarcGrpcAsyncIOTransport])
def test_eventarc_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
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
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_eventarc_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.EventarcRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_eventarc_rest_lro_client():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_eventarc_host_no_port(transport_name):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='eventarc.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'eventarc.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://eventarc.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_eventarc_host_with_port(transport_name):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='eventarc.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'eventarc.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://eventarc.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_eventarc_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = EventarcClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = EventarcClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_trigger._session
    session2 = client2.transport.get_trigger._session
    assert session1 != session2
    session1 = client1.transport.list_triggers._session
    session2 = client2.transport.list_triggers._session
    assert session1 != session2
    session1 = client1.transport.create_trigger._session
    session2 = client2.transport.create_trigger._session
    assert session1 != session2
    session1 = client1.transport.update_trigger._session
    session2 = client2.transport.update_trigger._session
    assert session1 != session2
    session1 = client1.transport.delete_trigger._session
    session2 = client2.transport.delete_trigger._session
    assert session1 != session2
    session1 = client1.transport.get_channel._session
    session2 = client2.transport.get_channel._session
    assert session1 != session2
    session1 = client1.transport.list_channels._session
    session2 = client2.transport.list_channels._session
    assert session1 != session2
    session1 = client1.transport.create_channel_._session
    session2 = client2.transport.create_channel_._session
    assert session1 != session2
    session1 = client1.transport.update_channel._session
    session2 = client2.transport.update_channel._session
    assert session1 != session2
    session1 = client1.transport.delete_channel._session
    session2 = client2.transport.delete_channel._session
    assert session1 != session2
    session1 = client1.transport.get_provider._session
    session2 = client2.transport.get_provider._session
    assert session1 != session2
    session1 = client1.transport.list_providers._session
    session2 = client2.transport.list_providers._session
    assert session1 != session2
    session1 = client1.transport.get_channel_connection._session
    session2 = client2.transport.get_channel_connection._session
    assert session1 != session2
    session1 = client1.transport.list_channel_connections._session
    session2 = client2.transport.list_channel_connections._session
    assert session1 != session2
    session1 = client1.transport.create_channel_connection._session
    session2 = client2.transport.create_channel_connection._session
    assert session1 != session2
    session1 = client1.transport.delete_channel_connection._session
    session2 = client2.transport.delete_channel_connection._session
    assert session1 != session2
    session1 = client1.transport.get_google_channel_config._session
    session2 = client2.transport.get_google_channel_config._session
    assert session1 != session2
    session1 = client1.transport.update_google_channel_config._session
    session2 = client2.transport.update_google_channel_config._session
    assert session1 != session2
def test_eventarc_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EventarcGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_eventarc_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EventarcGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.EventarcGrpcTransport, transports.EventarcGrpcAsyncIOTransport])
def test_eventarc_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
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
@pytest.mark.parametrize("transport_class", [transports.EventarcGrpcTransport, transports.EventarcGrpcAsyncIOTransport])
def test_eventarc_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
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


def test_eventarc_grpc_lro_client():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_eventarc_grpc_lro_async_client():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_channel_path():
    project = "squid"
    location = "clam"
    channel = "whelk"
    expected = "projects/{project}/locations/{location}/channels/{channel}".format(project=project, location=location, channel=channel, )
    actual = EventarcClient.channel_path(project, location, channel)
    assert expected == actual


def test_parse_channel_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "channel": "nudibranch",
    }
    path = EventarcClient.channel_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_channel_path(path)
    assert expected == actual

def test_channel_connection_path():
    project = "cuttlefish"
    location = "mussel"
    channel_connection = "winkle"
    expected = "projects/{project}/locations/{location}/channelConnections/{channel_connection}".format(project=project, location=location, channel_connection=channel_connection, )
    actual = EventarcClient.channel_connection_path(project, location, channel_connection)
    assert expected == actual


def test_parse_channel_connection_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "channel_connection": "abalone",
    }
    path = EventarcClient.channel_connection_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_channel_connection_path(path)
    assert expected == actual

def test_cloud_function_path():
    project = "squid"
    location = "clam"
    function = "whelk"
    expected = "projects/{project}/locations/{location}/functions/{function}".format(project=project, location=location, function=function, )
    actual = EventarcClient.cloud_function_path(project, location, function)
    assert expected == actual


def test_parse_cloud_function_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "function": "nudibranch",
    }
    path = EventarcClient.cloud_function_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_cloud_function_path(path)
    assert expected == actual

def test_crypto_key_path():
    project = "cuttlefish"
    location = "mussel"
    key_ring = "winkle"
    crypto_key = "nautilus"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(project=project, location=location, key_ring=key_ring, crypto_key=crypto_key, )
    actual = EventarcClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "key_ring": "squid",
        "crypto_key": "clam",
    }
    path = EventarcClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_crypto_key_path(path)
    assert expected == actual

def test_google_channel_config_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}/googleChannelConfig".format(project=project, location=location, )
    actual = EventarcClient.google_channel_config_path(project, location)
    assert expected == actual


def test_parse_google_channel_config_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = EventarcClient.google_channel_config_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_google_channel_config_path(path)
    assert expected == actual

def test_provider_path():
    project = "cuttlefish"
    location = "mussel"
    provider = "winkle"
    expected = "projects/{project}/locations/{location}/providers/{provider}".format(project=project, location=location, provider=provider, )
    actual = EventarcClient.provider_path(project, location, provider)
    assert expected == actual


def test_parse_provider_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "provider": "abalone",
    }
    path = EventarcClient.provider_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_provider_path(path)
    assert expected == actual

def test_service_path():
    expected = "*".format()
    actual = EventarcClient.service_path()
    assert expected == actual


def test_parse_service_path():
    expected = {
    }
    path = EventarcClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_service_path(path)
    assert expected == actual

def test_service_account_path():
    project = "squid"
    service_account = "clam"
    expected = "projects/{project}/serviceAccounts/{service_account}".format(project=project, service_account=service_account, )
    actual = EventarcClient.service_account_path(project, service_account)
    assert expected == actual


def test_parse_service_account_path():
    expected = {
        "project": "whelk",
        "service_account": "octopus",
    }
    path = EventarcClient.service_account_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_service_account_path(path)
    assert expected == actual

def test_trigger_path():
    project = "oyster"
    location = "nudibranch"
    trigger = "cuttlefish"
    expected = "projects/{project}/locations/{location}/triggers/{trigger}".format(project=project, location=location, trigger=trigger, )
    actual = EventarcClient.trigger_path(project, location, trigger)
    assert expected == actual


def test_parse_trigger_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "trigger": "nautilus",
    }
    path = EventarcClient.trigger_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_trigger_path(path)
    assert expected == actual

def test_workflow_path():
    project = "scallop"
    location = "abalone"
    workflow = "squid"
    expected = "projects/{project}/locations/{location}/workflows/{workflow}".format(project=project, location=location, workflow=workflow, )
    actual = EventarcClient.workflow_path(project, location, workflow)
    assert expected == actual


def test_parse_workflow_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "workflow": "octopus",
    }
    path = EventarcClient.workflow_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_workflow_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = EventarcClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = EventarcClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder, )
    actual = EventarcClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = EventarcClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = EventarcClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = EventarcClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project, )
    actual = EventarcClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = EventarcClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = EventarcClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = EventarcClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = EventarcClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.EventarcTransport, '_prep_wrapped_messages') as prep:
        client = EventarcClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.EventarcTransport, '_prep_wrapped_messages') as prep:
        transport_class = EventarcClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(transport: str = 'rest', request_type=locations_pb2.GetLocationRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)

@pytest.mark.parametrize("request_type", [
    locations_pb2.GetLocationRequest,
    dict,
])
def test_get_location_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)

def test_list_locations_rest_bad_request(transport: str = 'rest', request_type=locations_pb2.ListLocationsRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)

@pytest.mark.parametrize("request_type", [
    locations_pb2.ListLocationsRequest,
    dict,
])
def test_list_locations_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)

def test_get_iam_policy_rest_bad_request(transport: str = 'rest', request_type=iam_policy_pb2.GetIamPolicyRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'resource': 'projects/sample1/locations/sample2/triggers/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)

@pytest.mark.parametrize("request_type", [
    iam_policy_pb2.GetIamPolicyRequest,
    dict,
])
def test_get_iam_policy_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'resource': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

def test_set_iam_policy_rest_bad_request(transport: str = 'rest', request_type=iam_policy_pb2.SetIamPolicyRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'resource': 'projects/sample1/locations/sample2/triggers/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)

@pytest.mark.parametrize("request_type", [
    iam_policy_pb2.SetIamPolicyRequest,
    dict,
])
def test_set_iam_policy_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'resource': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

def test_test_iam_permissions_rest_bad_request(transport: str = 'rest', request_type=iam_policy_pb2.TestIamPermissionsRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'resource': 'projects/sample1/locations/sample2/triggers/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)

@pytest.mark.parametrize("request_type", [
    iam_policy_pb2.TestIamPermissionsRequest,
    dict,
])
def test_test_iam_permissions_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'resource': 'projects/sample1/locations/sample2/triggers/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

def test_cancel_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.CancelOperationRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.CancelOperationRequest,
    dict,
])
def test_cancel_operation_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = '{}'

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None

def test_delete_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.DeleteOperationRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.DeleteOperationRequest,
    dict,
])
def test_delete_operation_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = '{}'

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None

def test_get_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.GetOperationRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.GetOperationRequest,
    dict,
])
def test_get_operation_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)

def test_list_operations_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.ListOperationsRequest):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.ListOperationsRequest,
    dict,
])
def test_list_operations_rest(request_type):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None

def test_delete_operation_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value =  None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_delete_operation_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None

def test_cancel_operation_field_headers():
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value =  None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_cancel_operation_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_get_operation_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
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
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_list_operations_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
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
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_list_locations_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
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
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials())

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
    assert ("x-goog-request-params", "name=locations/abc",) in kw["metadata"]
@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "name=locations/abc",) in kw["metadata"]

def test_get_location_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
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
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(version=774, etag=b"etag_blob",)
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(version=774, etag=b"etag_blob",)
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]
@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]

def test_set_iam_policy_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy()
        )

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()

def test_get_iam_policy(transport: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(version=774, etag=b"etag_blob",)

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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_iam_policy), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(version=774, etag=b"etag_blob",)
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_iam_policy), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy()
        )

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()

def test_test_iam_permissions(transport: str = "grpc"):
    client = EventarcClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
    client = EventarcAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            iam_policy_pb2.TestIamPermissionsResponse(permissions=["permissions_value"],)
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
    client = EventarcClient(
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
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = EventarcAsyncClient(
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
    assert ("x-goog-request-params", "resource=resource/value",) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = EventarcClient(
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
    client = EventarcAsyncClient(
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
        client = EventarcClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = EventarcClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (EventarcClient, transports.EventarcGrpcTransport),
    (EventarcAsyncClient, transports.EventarcGrpcAsyncIOTransport),
])
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
