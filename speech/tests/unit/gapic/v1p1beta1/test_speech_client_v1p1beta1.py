# Copyright 2018 Google LLC
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

import pytest

from google.rpc import status_pb2

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1.proto import cloud_speech_pb2
from google.longrunning import operations_pb2


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

    def unary_unary(self,
                    method,
                    request_serializer=None,
                    response_deserializer=None):
        return MultiCallableStub(method, self)

    def stream_stream(self,
                      method,
                      request_serializer=None,
                      response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestSpeechClient(object):
    def test_recognize(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cloud_speech_pb2.RecognizeResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup Request
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        sample_rate_hertz = 44100
        language_code = 'en-US'
        config = {
            'encoding': encoding,
            'sample_rate_hertz': sample_rate_hertz,
            'language_code': language_code
        }
        uri = 'gs://bucket_name/file_name.flac'
        audio = {'uri': uri}

        response = client.recognize(config, audio)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_speech_pb2.RecognizeRequest(
            config=config, audio=audio)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_recognize_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup request
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        sample_rate_hertz = 44100
        language_code = 'en-US'
        config = {
            'encoding': encoding,
            'sample_rate_hertz': sample_rate_hertz,
            'language_code': language_code
        }
        uri = 'gs://bucket_name/file_name.flac'
        audio = {'uri': uri}

        with pytest.raises(CustomException):
            client.recognize(config, audio)

    def test_long_running_recognize(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cloud_speech_pb2.LongRunningRecognizeResponse(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_long_running_recognize', done=True)
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup Request
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        sample_rate_hertz = 44100
        language_code = 'en-US'
        config = {
            'encoding': encoding,
            'sample_rate_hertz': sample_rate_hertz,
            'language_code': language_code
        }
        uri = 'gs://bucket_name/file_name.flac'
        audio = {'uri': uri}

        response = client.long_running_recognize(config, audio)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloud_speech_pb2.LongRunningRecognizeRequest(
            config=config, audio=audio)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_long_running_recognize_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_long_running_recognize_exception', done=True)
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup Request
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        sample_rate_hertz = 44100
        language_code = 'en-US'
        config = {
            'encoding': encoding,
            'sample_rate_hertz': sample_rate_hertz,
            'language_code': language_code
        }
        uri = 'gs://bucket_name/file_name.flac'
        audio = {'uri': uri}

        response = client.long_running_recognize(config, audio)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_streaming_recognize(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = cloud_speech_pb2.StreamingRecognizeResponse(
            **expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[iter([expected_response])])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup Request
        request = {}
        request = cloud_speech_pb2.StreamingRecognizeRequest(**request)
        requests = [request]

        response = client._streaming_recognize(requests)
        resources = list(response)
        assert len(resources) == 1
        assert expected_response == resources[0]

        assert len(channel.requests) == 1
        actual_requests = channel.requests[0][1]
        assert len(actual_requests) == 1
        actual_request = list(actual_requests)[0]
        assert request == actual_request

    def test_streaming_recognize_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        client = speech_v1p1beta1.SpeechClient(channel=channel)

        # Setup request
        request = {}

        request = cloud_speech_pb2.StreamingRecognizeRequest(**request)
        requests = [request]

        with pytest.raises(CustomException):
            client._streaming_recognize(requests)
