# Copyright 2017, Google Inc. All rights reserved.
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

from google.rpc import status_pb2

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2.proto import video_intelligence_pb2
from google.longrunning import operations_pb2


class UnaryUnaryMultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""
    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))
        return self.channel_stub.responses.pop()


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""
    def __init__(self, responses):
        self.responses = responses
        self.requests = []

    def unary_unary(
            self, method, request_serializer=None, response_deserializer=None):
        return UnaryUnaryMultiCallableStub(method, self)


class TestVideoIntelligenceServiceClient(object):
    def test_annotate_video(self):
        # Request
        input_uri = 'inputUri1707300727'
        features = []

        # Response
        expected_response = video_intelligence_pb2.AnnotateVideoResponse()
        operation = operations_pb2.Operation(
            name='operations/test_annotate_video', done=True)
        operation.response.Pack(expected_response)

        # gRPC Channel
        channel = ChannelStub(responses=[operation])

        # Client
        client = videointelligence_v1beta2.VideoIntelligenceServiceClient(
            channel=channel)

        # Make the request and check the result.
        response = client.annotate_video(input_uri, features)
        result = response.result()

        assert expected_response == result

        # Verify the state of the stubs
        assert len(channel.requests) == 1

        expected_request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri, features=features)
        actual_request = channel.requests[0][1]

        assert actual_request == expected_request

    def test_annotate_video_exception(self):
        # Mock request
        input_uri = 'inputUri1707300727'
        features = []

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_annotate_video_exception', done=True)
        operation.error.CopyFrom(error)

        # gRPC Channel
        channel = ChannelStub(responses=[operation])

        # Make the request and check the result.
        client = videointelligence_v1beta2.VideoIntelligenceServiceClient(
            channel=channel)

        response = client.annotate_video(input_uri, features)
        exception = response.exception()

        assert exception.errors[0] == error
