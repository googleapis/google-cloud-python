# Copyright 2016 Google Inc. All rights reserved.
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
import base64

from gcloud._helpers import _to_bytes


class TestVisionImage(unittest.TestCase):
    _IMAGE_SOURCE = 'gs://some/image.jpg'
    _IMAGE_CONTENT = _to_bytes('/9j/4QNURXhpZgAASUkq')
    _B64_IMAGE_CONTENT = base64.b64encode(_IMAGE_CONTENT)
    _CLIENT_MOCK = {'source': ''}

    def _getTargetClass(self):
        from gcloud.vision.image import Image
        return Image

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_image_source_type_content(self):
        image = self._makeOne(self._IMAGE_CONTENT, self._CLIENT_MOCK)

        _AS_DICT = {
            'content': self._B64_IMAGE_CONTENT
        }

        self.assertEqual(self._B64_IMAGE_CONTENT, image.content)
        self.assertEqual(None, image.source)
        self.assertEqual(_AS_DICT, image.as_dict())

    def test_image_source_type_gcloud_storage(self):
        image = self._makeOne(self._IMAGE_SOURCE, self._CLIENT_MOCK)

        _AS_DICT = {
            'source': {
                'gcs_image_uri': self._IMAGE_SOURCE
            }
        }

        self.assertEqual(self._IMAGE_SOURCE, image.source)
        self.assertEqual(None, image.content)
        self.assertEqual(_AS_DICT, image.as_dict())

    def test_cannot_set_both_source_and_content(self):
        image = self._makeOne(self._IMAGE_CONTENT, self._CLIENT_MOCK)

        self.assertEqual(self._B64_IMAGE_CONTENT, image.content)
        with self.assertRaises(AttributeError):
            image.source = self._IMAGE_SOURCE

        image = self._makeOne(self._IMAGE_SOURCE, self._CLIENT_MOCK)
        self.assertEqual(self._IMAGE_SOURCE, image.source)
        with self.assertRaises(AttributeError):
            image.content = self._IMAGE_CONTENT
