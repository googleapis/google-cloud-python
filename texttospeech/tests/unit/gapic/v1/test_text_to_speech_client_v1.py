# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import mock
import pytest

from google.cloud import texttospeech_v1
from google.cloud.texttospeech_v1.proto import cloud_tts_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestTextToSpeechClient(object):
    def test_list_voices(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cloud_tts_pb2.ListVoicesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = texttospeech_v1.TextToSpeechClient()

        response = client.list_voices()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_tts_pb2.ListVoicesRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_voices_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = texttospeech_v1.TextToSpeechClient()

        with pytest.raises(CustomException):
            client.list_voices()

    def test_synthesize_speech(self):
        # Setup Expected Response
        audio_content = b"16"
        expected_response = {"audio_content": audio_content}
        expected_response = cloud_tts_pb2.SynthesizeSpeechResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = texttospeech_v1.TextToSpeechClient()

        # Setup Request
        input_ = {}
        voice = {}
        audio_config = {}

        response = client.synthesize_speech(input_, voice, audio_config)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_tts_pb2.SynthesizeSpeechRequest(
            input=input_, voice=voice, audio_config=audio_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_synthesize_speech_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = texttospeech_v1.TextToSpeechClient()

        # Setup request
        input_ = {}
        voice = {}
        audio_config = {}

        with pytest.raises(CustomException):
            client.synthesize_speech(input_, voice, audio_config)
