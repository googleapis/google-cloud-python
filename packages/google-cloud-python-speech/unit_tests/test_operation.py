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

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        client = object()
        operation = self._makeOne(
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
        from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

        return cloud_speech_pb2.SpeechRecognitionResult(
            alternatives=[
                cloud_speech_pb2.SpeechRecognitionAlternative(
                    transcript=transcript,
                    confidence=confidence,
                ),
            ],
        )

    def _make_operation_pb(self, *results):
        from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2
        from google.longrunning import operations_pb2
        from google.protobuf.any_pb2 import Any

        any_pb = None
        if results:
            result_pb = cloud_speech_pb2.AsyncRecognizeResponse(
                results=results,
            )
            type_url = 'type.googleapis.com/%s' % (
                result_pb.DESCRIPTOR.full_name,)
            any_pb = Any(type_url=type_url,
                         value=result_pb.SerializeToString())

        return operations_pb2.Operation(
            name=self.OPERATION_NAME,
            response=any_pb)

    def test__update_state_no_response(self):
        client = object()
        operation = self._makeOne(
            self.OPERATION_NAME, client)

        operation_pb = self._make_operation_pb()
        operation._update_state(operation_pb)
        self.assertIsNone(operation.response)
        self.assertIsNone(operation.results)

    def test__update_state_with_response(self):
        from google.cloud.speech.alternative import Alternative

        client = object()
        operation = self._makeOne(
            self.OPERATION_NAME, client)

        text = 'hi mom'
        confidence = 0.75
        result = self._make_result(text, confidence)
        operation_pb = self._make_operation_pb(result)
        operation._update_state(operation_pb)
        self.assertIsNotNone(operation.response)

        self.assertEqual(len(operation.results), 1)
        alternative = operation.results[0]
        self.assertIsInstance(alternative, Alternative)
        self.assertEqual(alternative.transcript, text)
        self.assertEqual(alternative.confidence, confidence)

    def test__update_state_bad_response(self):
        client = object()
        operation = self._makeOne(
            self.OPERATION_NAME, client)

        result1 = self._make_result('is this ok?', 0.625)
        result2 = self._make_result('ease is ok', None)
        operation_pb = self._make_operation_pb(result1, result2)
        with self.assertRaises(ValueError):
            operation._update_state(operation_pb)
