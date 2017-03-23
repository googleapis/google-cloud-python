# Copyright 2017 Google Inc.
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


class TestTextAnnotatin(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.text import TextAnnotation
        return TextAnnotation

    def test_text_annotation_from_api_repr(self):
        annotation = {
            'pages': [],
            'text': 'some detected text',
        }
        text_annotation = self._get_target_class().from_api_repr(annotation)
        self.assertIsInstance(text_annotation, self._get_target_class())
        self.assertEqual(len(text_annotation.pages), 0)
        self.assertEqual(text_annotation.text, annotation['text'])

    def test_text_annotation_from_pb(self):
        from google.cloud.proto.vision.v1 import text_annotation_pb2

        page = text_annotation_pb2.Page(width=8, height=11)
        text = 'some detected text'
        text_annotation_pb = text_annotation_pb2.TextAnnotation(
            pages=[page], text=text)

        text_annotation = self._get_target_class().from_pb(text_annotation_pb)
        self.assertIsInstance(text_annotation, self._get_target_class())
        self.assertEqual(len(text_annotation.pages), 1)
        self.assertEqual(text_annotation.pages[0].width, 8)
        self.assertEqual(text_annotation.pages[0].height, 11)
        self.assertEqual(text_annotation.text, text)
