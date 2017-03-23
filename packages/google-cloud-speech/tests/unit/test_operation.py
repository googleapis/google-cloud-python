# Copyright 2016 Google Inc.
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

import unittest


class TestOperation(unittest.TestCase):

    OPERATION_NAME = '123456789'

    @staticmethod
    def _get_target_class():
        from google.cloud.speech.operation import Operation

        return Operation

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        client = object()
        operation = self._make_one(
            self.OPERATION_NAME, client)
        self.assertEqual(operation.name, self.OPERATION_NAME)
        self.assertIs(operation.client, client)
        self.assertIsNone(operation.target)
        self.assertIsNone(operation.response)
        self.assertIsNone(operation.results)
        self.assertIsNone(operation.error)
        self.assertIsNone(operation.metadata)
        self.assertEqual(operation.caller_metadata, {})
        self.assertTrue(operation._from_grpc)

    @staticmethod
    def _make_result(transcript, confidence):
        from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2

        return cloud_speech_pb2.SpeechRecognitionResult(
            alternatives=[
                cloud_speech_pb2.SpeechRecognitionAlternative(
                    transcript=transcript,
                    confidence=confidence,
                ),
            ],
        )

    def _make_operation_pb(self, *results):
        from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any

        any_pb = None
        if results:
            result_pb = cloud_speech_pb2.AsyncRecognizeResponse(
                results=results,
            )
            type_url = 'type.googleapis.com/%s' % (
                result_pb.DESCRIPTOR.full_name,)
            any_pb = Any(
                type_url=type_url, value=result_pb.SerializeToString())

        return operations_pb2.Operation(
            name=self.OPERATION_NAME, response=any_pb)

    def test__update_state_no_response(self):
        client = object()
        operation = self._make_one(
            self.OPERATION_NAME, client)

        operation_pb = self._make_operation_pb()
        operation._update_state(operation_pb)
        self.assertIsNone(operation.response)
        self.assertIsNone(operation.results)

    def test__update_state_with_response(self):
        from google.cloud.speech.alternative import Alternative
        from google.cloud.speech.result import Result

        client = object()
        operation = self._make_one(
            self.OPERATION_NAME, client)

        results = [
            self._make_result('hi mom', 0.75),
            self._make_result('hi dad', 0.75),
        ]
        operation_pb = self._make_operation_pb(*results)
        operation._update_state(operation_pb)
        self.assertIsNotNone(operation.response)

        self.assertEqual(len(operation.results), 2)
        for result, text in zip(operation.results, ['hi mom', 'hi dad']):
            self.assertIsInstance(result, Result)
            self.assertEqual(result.transcript, text)
            self.assertEqual(result.confidence, 0.75)
            self.assertIsInstance(result.alternatives, list)
            self.assertIsInstance(result.alternatives[0], Alternative)

    def test__update_state_with_empty_response(self):
        from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any

        # Simulate an empty response (rather than no response yet, which
        # is distinct).
        response = cloud_speech_pb2.AsyncRecognizeResponse(results=[])
        type_url = 'type.googleapis.com/%s' % response.DESCRIPTOR.full_name
        any_pb = Any(
            type_url=type_url,
            value=response.SerializeToString(),
        )
        operation_pb = operations_pb2.Operation(
            name=self.OPERATION_NAME,
            response=any_pb,
        )

        # Establish that we raise ValueError at state update time.
        client = object()
        operation = self._make_one(self.OPERATION_NAME, client)
        with self.assertRaises(ValueError):
            operation._update_state(operation_pb)
