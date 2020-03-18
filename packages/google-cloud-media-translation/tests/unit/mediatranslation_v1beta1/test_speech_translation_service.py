# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.auth import credentials
from google.cloud.mediatranslation_v1beta1.services.speech_translation_service import (
    SpeechTranslationServiceClient,
)
from google.cloud.mediatranslation_v1beta1.services.speech_translation_service import (
    transports,
)
from google.cloud.mediatranslation_v1beta1.types import media_translation
from google.oauth2 import service_account
from google.rpc import status_pb2 as status  # type: ignore


def test_speech_translation_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = SpeechTranslationServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = SpeechTranslationServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "mediatranslation.googleapis.com:443"


def test_speech_translation_service_client_client_options():
    # Check the default options have their expected values.
    assert (
        SpeechTranslationServiceClient.DEFAULT_OPTIONS.api_endpoint
        == "mediatranslation.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.mediatranslation_v1beta1.services.speech_translation_service.SpeechTranslationServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = SpeechTranslationServiceClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_speech_translation_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.mediatranslation_v1beta1.services.speech_translation_service.SpeechTranslationServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = SpeechTranslationServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_streaming_translate_speech(transport: str = "grpc"):
    client = SpeechTranslationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = media_translation.StreamingTranslateSpeechRequest()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.streaming_translate_speech), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([media_translation.StreamingTranslateSpeechResponse()])

        response = client.streaming_translate_speech(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, media_translation.StreamingTranslateSpeechResponse)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SpeechTranslationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = SpeechTranslationServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SpeechTranslationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = SpeechTranslationServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = SpeechTranslationServiceClient(
        credentials=credentials.AnonymousCredentials()
    )
    assert isinstance(
        client._transport, transports.SpeechTranslationServiceGrpcTransport
    )


def test_speech_translation_service_base_transport():
    # Instantiate the base transport.
    transport = transports.SpeechTranslationServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = ("streaming_translate_speech",)
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_speech_translation_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        SpeechTranslationServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_speech_translation_service_host_no_port():
    client = SpeechTranslationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="mediatranslation.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "mediatranslation.googleapis.com:443"


def test_speech_translation_service_host_with_port():
    client = SpeechTranslationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="mediatranslation.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "mediatranslation.googleapis.com:8000"


def test_speech_translation_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.SpeechTranslationServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
