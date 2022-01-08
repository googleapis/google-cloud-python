# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.speech_v1p1beta1.services.adaptation import AdaptationAsyncClient
from google.cloud.speech_v1p1beta1.services.adaptation import AdaptationClient
from google.cloud.speech_v1p1beta1.services.adaptation import pagers
from google.cloud.speech_v1p1beta1.services.adaptation import transports
from google.cloud.speech_v1p1beta1.types import cloud_speech_adaptation
from google.cloud.speech_v1p1beta1.types import resource
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
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

    assert AdaptationClient._get_default_mtls_endpoint(None) is None
    assert (
        AdaptationClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        AdaptationClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AdaptationClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AdaptationClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert AdaptationClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [AdaptationClient, AdaptationAsyncClient,])
def test_adaptation_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "speech.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AdaptationGrpcTransport, "grpc"),
        (transports.AdaptationGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_adaptation_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize("client_class", [AdaptationClient, AdaptationAsyncClient,])
def test_adaptation_client_from_service_account_file(client_class):
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

        assert client.transport._host == "speech.googleapis.com:443"


def test_adaptation_client_get_transport_class():
    transport = AdaptationClient.get_transport_class()
    available_transports = [
        transports.AdaptationGrpcTransport,
    ]
    assert transport in available_transports

    transport = AdaptationClient.get_transport_class("grpc")
    assert transport == transports.AdaptationGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AdaptationClient, transports.AdaptationGrpcTransport, "grpc"),
        (
            AdaptationAsyncClient,
            transports.AdaptationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AdaptationClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AdaptationClient)
)
@mock.patch.object(
    AdaptationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AdaptationAsyncClient),
)
def test_adaptation_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AdaptationClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AdaptationClient, "get_transport_class") as gtc:
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
        (AdaptationClient, transports.AdaptationGrpcTransport, "grpc", "true"),
        (
            AdaptationAsyncClient,
            transports.AdaptationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (AdaptationClient, transports.AdaptationGrpcTransport, "grpc", "false"),
        (
            AdaptationAsyncClient,
            transports.AdaptationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AdaptationClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AdaptationClient)
)
@mock.patch.object(
    AdaptationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AdaptationAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_adaptation_client_mtls_env_auto(
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
    "client_class,transport_class,transport_name",
    [
        (AdaptationClient, transports.AdaptationGrpcTransport, "grpc"),
        (
            AdaptationAsyncClient,
            transports.AdaptationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_adaptation_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
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
    "client_class,transport_class,transport_name",
    [
        (AdaptationClient, transports.AdaptationGrpcTransport, "grpc"),
        (
            AdaptationAsyncClient,
            transports.AdaptationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_adaptation_client_client_options_credentials_file(
    client_class, transport_class, transport_name
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


def test_adaptation_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.speech_v1p1beta1.services.adaptation.transports.AdaptationGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AdaptationClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
    "request_type", [cloud_speech_adaptation.CreatePhraseSetRequest, dict,]
)
def test_create_phrase_set(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet(name="name_value", boost=0.551,)
        response = client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


def test_create_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        client.create_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreatePhraseSetRequest()


@pytest.mark.asyncio
async def test_create_phrase_set_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.CreatePhraseSetRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.PhraseSet(name="name_value", boost=0.551,)
        )
        response = await client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


@pytest.mark.asyncio
async def test_create_phrase_set_async_from_dict():
    await test_create_phrase_set_async(request_type=dict)


def test_create_phrase_set_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.CreatePhraseSetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        call.return_value = resource.PhraseSet()
        client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_phrase_set_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.CreatePhraseSetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        await client.create_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_phrase_set_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_phrase_set(
            parent="parent_value",
            phrase_set=resource.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_set
        mock_val = resource.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].phrase_set_id
        mock_val = "phrase_set_id_value"
        assert arg == mock_val


def test_create_phrase_set_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_phrase_set(
            cloud_speech_adaptation.CreatePhraseSetRequest(),
            parent="parent_value",
            phrase_set=resource.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )


@pytest.mark.asyncio
async def test_create_phrase_set_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_phrase_set(
            parent="parent_value",
            phrase_set=resource.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].phrase_set
        mock_val = resource.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].phrase_set_id
        mock_val = "phrase_set_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_phrase_set_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_phrase_set(
            cloud_speech_adaptation.CreatePhraseSetRequest(),
            parent="parent_value",
            phrase_set=resource.PhraseSet(name="name_value"),
            phrase_set_id="phrase_set_id_value",
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.GetPhraseSetRequest, dict,]
)
def test_get_phrase_set(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet(name="name_value", boost=0.551,)
        response = client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


def test_get_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        client.get_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetPhraseSetRequest()


@pytest.mark.asyncio
async def test_get_phrase_set_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.GetPhraseSetRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.PhraseSet(name="name_value", boost=0.551,)
        )
        response = await client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


@pytest.mark.asyncio
async def test_get_phrase_set_async_from_dict():
    await test_get_phrase_set_async(request_type=dict)


def test_get_phrase_set_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.GetPhraseSetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        call.return_value = resource.PhraseSet()
        client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_phrase_set_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.GetPhraseSetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        await client.get_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_phrase_set_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_phrase_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_phrase_set_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_phrase_set(
            cloud_speech_adaptation.GetPhraseSetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_phrase_set_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_phrase_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_phrase_set_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_phrase_set(
            cloud_speech_adaptation.GetPhraseSetRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.ListPhraseSetRequest, dict,]
)
def test_list_phrase_set(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListPhraseSetResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseSetPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        client.list_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListPhraseSetRequest()


@pytest.mark.asyncio
async def test_list_phrase_set_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.ListPhraseSetRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListPhraseSetResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListPhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPhraseSetAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_phrase_set_async_from_dict():
    await test_list_phrase_set_async(request_type=dict)


def test_list_phrase_set_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.ListPhraseSetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        call.return_value = cloud_speech_adaptation.ListPhraseSetResponse()
        client.list_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_phrase_set_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.ListPhraseSetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListPhraseSetResponse()
        )
        await client.list_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_phrase_set_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListPhraseSetResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_phrase_set(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_phrase_set_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_phrase_set(
            cloud_speech_adaptation.ListPhraseSetRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_phrase_set_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListPhraseSetResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListPhraseSetResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_phrase_set(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_phrase_set_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_phrase_set(
            cloud_speech_adaptation.ListPhraseSetRequest(), parent="parent_value",
        )


def test_list_phrase_set_pager(transport_name: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(), resource.PhraseSet(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_phrase_set(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resource.PhraseSet) for i in results)


def test_list_phrase_set_pages(transport_name: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_phrase_set), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(), resource.PhraseSet(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_phrase_set(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_phrase_set_async_pager():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_set), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(), resource.PhraseSet(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_phrase_set(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resource.PhraseSet) for i in responses)


@pytest.mark.asyncio
async def test_list_phrase_set_async_pages():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_phrase_set), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                    resource.PhraseSet(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListPhraseSetResponse(
                phrase_sets=[resource.PhraseSet(), resource.PhraseSet(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_phrase_set(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.UpdatePhraseSetRequest, dict,]
)
def test_update_phrase_set(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet(name="name_value", boost=0.551,)
        response = client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


def test_update_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        client.update_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdatePhraseSetRequest()


@pytest.mark.asyncio
async def test_update_phrase_set_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.UpdatePhraseSetRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.PhraseSet(name="name_value", boost=0.551,)
        )
        response = await client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdatePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.PhraseSet)
    assert response.name == "name_value"
    assert math.isclose(response.boost, 0.551, rel_tol=1e-6)


@pytest.mark.asyncio
async def test_update_phrase_set_async_from_dict():
    await test_update_phrase_set_async(request_type=dict)


def test_update_phrase_set_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.UpdatePhraseSetRequest()

    request.phrase_set.name = "phrase_set.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        call.return_value = resource.PhraseSet()
        client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "phrase_set.name=phrase_set.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_phrase_set_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.UpdatePhraseSetRequest()

    request.phrase_set.name = "phrase_set.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        await client.update_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "phrase_set.name=phrase_set.name/value",) in kw[
        "metadata"
    ]


def test_update_phrase_set_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_phrase_set(
            phrase_set=resource.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_set
        mock_val = resource.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_phrase_set_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_phrase_set(
            cloud_speech_adaptation.UpdatePhraseSetRequest(),
            phrase_set=resource.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_phrase_set_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.PhraseSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resource.PhraseSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_phrase_set(
            phrase_set=resource.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].phrase_set
        mock_val = resource.PhraseSet(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_phrase_set_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_phrase_set(
            cloud_speech_adaptation.UpdatePhraseSetRequest(),
            phrase_set=resource.PhraseSet(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.DeletePhraseSetRequest, dict,]
)
def test_delete_phrase_set(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_phrase_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        client.delete_phrase_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeletePhraseSetRequest()


@pytest.mark.asyncio
async def test_delete_phrase_set_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.DeletePhraseSetRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeletePhraseSetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_phrase_set_async_from_dict():
    await test_delete_phrase_set_async(request_type=dict)


def test_delete_phrase_set_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.DeletePhraseSetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        call.return_value = None
        client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_phrase_set_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.DeletePhraseSetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_phrase_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_phrase_set_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_phrase_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_phrase_set_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_phrase_set(
            cloud_speech_adaptation.DeletePhraseSetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_phrase_set_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_phrase_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_phrase_set(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_phrase_set_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_phrase_set(
            cloud_speech_adaptation.DeletePhraseSetRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.CreateCustomClassRequest, dict,]
)
def test_create_custom_class(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass(
            name="name_value", custom_class_id="custom_class_id_value",
        )
        response = client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


def test_create_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        client.create_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreateCustomClassRequest()


@pytest.mark.asyncio
async def test_create_custom_class_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.CreateCustomClassRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass(
                name="name_value", custom_class_id="custom_class_id_value",
            )
        )
        response = await client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.CreateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


@pytest.mark.asyncio
async def test_create_custom_class_async_from_dict():
    await test_create_custom_class_async(request_type=dict)


def test_create_custom_class_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.CreateCustomClassRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        call.return_value = resource.CustomClass()
        client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_custom_class_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.CreateCustomClassRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        await client.create_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_custom_class_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_custom_class(
            parent="parent_value",
            custom_class=resource.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_class
        mock_val = resource.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].custom_class_id
        mock_val = "custom_class_id_value"
        assert arg == mock_val


def test_create_custom_class_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_custom_class(
            cloud_speech_adaptation.CreateCustomClassRequest(),
            parent="parent_value",
            custom_class=resource.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )


@pytest.mark.asyncio
async def test_create_custom_class_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_custom_class(
            parent="parent_value",
            custom_class=resource.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].custom_class
        mock_val = resource.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].custom_class_id
        mock_val = "custom_class_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_custom_class_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_custom_class(
            cloud_speech_adaptation.CreateCustomClassRequest(),
            parent="parent_value",
            custom_class=resource.CustomClass(name="name_value"),
            custom_class_id="custom_class_id_value",
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.GetCustomClassRequest, dict,]
)
def test_get_custom_class(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass(
            name="name_value", custom_class_id="custom_class_id_value",
        )
        response = client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


def test_get_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        client.get_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetCustomClassRequest()


@pytest.mark.asyncio
async def test_get_custom_class_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.GetCustomClassRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass(
                name="name_value", custom_class_id="custom_class_id_value",
            )
        )
        response = await client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.GetCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


@pytest.mark.asyncio
async def test_get_custom_class_async_from_dict():
    await test_get_custom_class_async(request_type=dict)


def test_get_custom_class_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.GetCustomClassRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        call.return_value = resource.CustomClass()
        client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_custom_class_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.GetCustomClassRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        await client.get_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_custom_class_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_custom_class(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_custom_class_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_custom_class(
            cloud_speech_adaptation.GetCustomClassRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_custom_class_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_custom_class), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_custom_class(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_custom_class_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_custom_class(
            cloud_speech_adaptation.GetCustomClassRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.ListCustomClassesRequest, dict,]
)
def test_list_custom_classes(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListCustomClassesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListCustomClassesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomClassesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_custom_classes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        client.list_custom_classes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListCustomClassesRequest()


@pytest.mark.asyncio
async def test_list_custom_classes_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.ListCustomClassesRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListCustomClassesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.ListCustomClassesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCustomClassesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_custom_classes_async_from_dict():
    await test_list_custom_classes_async(request_type=dict)


def test_list_custom_classes_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.ListCustomClassesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        call.return_value = cloud_speech_adaptation.ListCustomClassesResponse()
        client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_custom_classes_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.ListCustomClassesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListCustomClassesResponse()
        )
        await client.list_custom_classes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_custom_classes_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListCustomClassesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_custom_classes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_custom_classes_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_custom_classes(
            cloud_speech_adaptation.ListCustomClassesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_custom_classes_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_speech_adaptation.ListCustomClassesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_speech_adaptation.ListCustomClassesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_custom_classes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_custom_classes_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_custom_classes(
            cloud_speech_adaptation.ListCustomClassesRequest(), parent="parent_value",
        )


def test_list_custom_classes_pager(transport_name: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[
                    resource.CustomClass(),
                    resource.CustomClass(),
                    resource.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(), resource.CustomClass(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_custom_classes(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resource.CustomClass) for i in results)


def test_list_custom_classes_pages(transport_name: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[
                    resource.CustomClass(),
                    resource.CustomClass(),
                    resource.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(), resource.CustomClass(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_custom_classes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_custom_classes_async_pager():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[
                    resource.CustomClass(),
                    resource.CustomClass(),
                    resource.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(), resource.CustomClass(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_custom_classes(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resource.CustomClass) for i in responses)


@pytest.mark.asyncio
async def test_list_custom_classes_async_pages():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_custom_classes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[
                    resource.CustomClass(),
                    resource.CustomClass(),
                    resource.CustomClass(),
                ],
                next_page_token="abc",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[], next_page_token="def",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(),], next_page_token="ghi",
            ),
            cloud_speech_adaptation.ListCustomClassesResponse(
                custom_classes=[resource.CustomClass(), resource.CustomClass(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_custom_classes(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.UpdateCustomClassRequest, dict,]
)
def test_update_custom_class(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass(
            name="name_value", custom_class_id="custom_class_id_value",
        )
        response = client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


def test_update_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        client.update_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdateCustomClassRequest()


@pytest.mark.asyncio
async def test_update_custom_class_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.UpdateCustomClassRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass(
                name="name_value", custom_class_id="custom_class_id_value",
            )
        )
        response = await client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.UpdateCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resource.CustomClass)
    assert response.name == "name_value"
    assert response.custom_class_id == "custom_class_id_value"


@pytest.mark.asyncio
async def test_update_custom_class_async_from_dict():
    await test_update_custom_class_async(request_type=dict)


def test_update_custom_class_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.UpdateCustomClassRequest()

    request.custom_class.name = "custom_class.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        call.return_value = resource.CustomClass()
        client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_class.name=custom_class.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_custom_class_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.UpdateCustomClassRequest()

    request.custom_class.name = "custom_class.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        await client.update_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "custom_class.name=custom_class.name/value",
    ) in kw["metadata"]


def test_update_custom_class_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_custom_class(
            custom_class=resource.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_class
        mock_val = resource.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_custom_class_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_custom_class(
            cloud_speech_adaptation.UpdateCustomClassRequest(),
            custom_class=resource.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_custom_class_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resource.CustomClass()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resource.CustomClass()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_custom_class(
            custom_class=resource.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].custom_class
        mock_val = resource.CustomClass(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_custom_class_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_custom_class(
            cloud_speech_adaptation.UpdateCustomClassRequest(),
            custom_class=resource.CustomClass(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type", [cloud_speech_adaptation.DeleteCustomClassRequest, dict,]
)
def test_delete_custom_class(request_type, transport: str = "grpc"):
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_custom_class_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        client.delete_custom_class()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeleteCustomClassRequest()


@pytest.mark.asyncio
async def test_delete_custom_class_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_speech_adaptation.DeleteCustomClassRequest,
):
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_speech_adaptation.DeleteCustomClassRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_custom_class_async_from_dict():
    await test_delete_custom_class_async(request_type=dict)


def test_delete_custom_class_field_headers():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.DeleteCustomClassRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        call.return_value = None
        client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_custom_class_field_headers_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_speech_adaptation.DeleteCustomClassRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_custom_class(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_custom_class_flattened():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_custom_class(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_custom_class_flattened_error():
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_custom_class(
            cloud_speech_adaptation.DeleteCustomClassRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_custom_class_flattened_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_custom_class), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_custom_class(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_custom_class_flattened_error_async():
    client = AdaptationAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_custom_class(
            cloud_speech_adaptation.DeleteCustomClassRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AdaptationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AdaptationClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AdaptationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AdaptationClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AdaptationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AdaptationClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AdaptationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AdaptationClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AdaptationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AdaptationGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.AdaptationGrpcTransport, transports.AdaptationGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AdaptationClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.AdaptationGrpcTransport,)


def test_adaptation_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AdaptationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_adaptation_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.speech_v1p1beta1.services.adaptation.transports.AdaptationTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AdaptationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_phrase_set",
        "get_phrase_set",
        "list_phrase_set",
        "update_phrase_set",
        "delete_phrase_set",
        "create_custom_class",
        "get_custom_class",
        "list_custom_classes",
        "update_custom_class",
        "delete_custom_class",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_adaptation_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.speech_v1p1beta1.services.adaptation.transports.AdaptationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AdaptationTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_adaptation_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.speech_v1p1beta1.services.adaptation.transports.AdaptationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AdaptationTransport()
        adc.assert_called_once()


def test_adaptation_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AdaptationClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AdaptationGrpcTransport, transports.AdaptationGrpcAsyncIOTransport,],
)
def test_adaptation_transport_auth_adc(transport_class):
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
    "transport_class,grpc_helpers",
    [
        (transports.AdaptationGrpcTransport, grpc_helpers),
        (transports.AdaptationGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_adaptation_transport_create_channel(transport_class, grpc_helpers):
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
            "speech.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="speech.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AdaptationGrpcTransport, transports.AdaptationGrpcAsyncIOTransport],
)
def test_adaptation_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_adaptation_host_no_port():
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="speech.googleapis.com"
        ),
    )
    assert client.transport._host == "speech.googleapis.com:443"


def test_adaptation_host_with_port():
    client = AdaptationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="speech.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "speech.googleapis.com:8000"


def test_adaptation_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AdaptationGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_adaptation_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AdaptationGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.AdaptationGrpcTransport, transports.AdaptationGrpcAsyncIOTransport],
)
def test_adaptation_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.AdaptationGrpcTransport, transports.AdaptationGrpcAsyncIOTransport],
)
def test_adaptation_transport_channel_mtls_with_adc(transport_class):
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


def test_custom_class_path():
    project = "squid"
    location = "clam"
    custom_class = "whelk"
    expected = "projects/{project}/locations/{location}/customClasses/{custom_class}".format(
        project=project, location=location, custom_class=custom_class,
    )
    actual = AdaptationClient.custom_class_path(project, location, custom_class)
    assert expected == actual


def test_parse_custom_class_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "custom_class": "nudibranch",
    }
    path = AdaptationClient.custom_class_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_custom_class_path(path)
    assert expected == actual


def test_phrase_set_path():
    project = "cuttlefish"
    location = "mussel"
    phrase_set = "winkle"
    expected = "projects/{project}/locations/{location}/phraseSets/{phrase_set}".format(
        project=project, location=location, phrase_set=phrase_set,
    )
    actual = AdaptationClient.phrase_set_path(project, location, phrase_set)
    assert expected == actual


def test_parse_phrase_set_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "phrase_set": "abalone",
    }
    path = AdaptationClient.phrase_set_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_phrase_set_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AdaptationClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = AdaptationClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = AdaptationClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = AdaptationClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = AdaptationClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = AdaptationClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = AdaptationClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = AdaptationClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AdaptationClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = AdaptationClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AdaptationClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AdaptationTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AdaptationClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AdaptationTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AdaptationClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = AdaptationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
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
        client = AdaptationClient(
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
        client = AdaptationClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
