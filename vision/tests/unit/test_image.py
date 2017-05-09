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

import base64
import unittest

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode

IMAGE_SOURCE = 'gs://some/image.jpg'
IMAGE_CONTENT = _to_bytes('/9j/4QNURXhpZgAASUkq')
B64_IMAGE_CONTENT = _bytes_to_unicode(base64.b64encode(IMAGE_CONTENT))
CLIENT_MOCK = {'source': ''}


class TestVisionImage(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.image import Image

        return Image

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_must_set_one_source(self):
        with self.assertRaises(ValueError):
            self._make_one(CLIENT_MOCK)

        with self.assertRaises(ValueError):
            self._make_one(CLIENT_MOCK, content=IMAGE_CONTENT,
                           source_uri=IMAGE_SOURCE)

        with self.assertRaises(ValueError):
            self._make_one(CLIENT_MOCK, content=IMAGE_CONTENT,
                           source_uri=IMAGE_SOURCE, filename='myimage.jpg')

        image = self._make_one(CLIENT_MOCK, content=IMAGE_CONTENT)
        self.assertEqual(image.content, IMAGE_CONTENT)

    def test_image_source_type_content(self):
        image = self._make_one(CLIENT_MOCK, content=IMAGE_CONTENT)

        as_dict = {
            'content': B64_IMAGE_CONTENT,
        }

        self.assertEqual(image.content, IMAGE_CONTENT)
        self.assertIsNone(image.source)
        self.assertEqual(image.as_dict(), as_dict)

    def test_image_source_type_google_cloud_storage(self):
        image = self._make_one(CLIENT_MOCK, source_uri=IMAGE_SOURCE)

        as_dict = {
            'source': {
                'gcs_image_uri': IMAGE_SOURCE,
            }
        }

        self.assertEqual(IMAGE_SOURCE, image.source)
        self.assertEqual(None, image.content)
        self.assertEqual(image.as_dict(), as_dict)

    def test_image_source_type_image_url(self):
        url = 'http://www.example.com/image.jpg'
        image = self._make_one(CLIENT_MOCK, source_uri=url)
        as_dict = {
            'source': {
                'image_uri': url,
            },
        }

        self.assertEqual(image.source, url)
        self.assertIsNone(image.content)
        self.assertEqual(image.as_dict(), as_dict)

    def test_image_no_valid_image_data(self):
        image = self._make_one(CLIENT_MOCK, source_uri='ftp://notsupported')
        with self.assertRaises(ValueError):
            image.as_dict()

    def test_cannot_set_both_source_and_content(self):
        image = self._make_one(CLIENT_MOCK, content=IMAGE_CONTENT)

        self.assertEqual(image.content, IMAGE_CONTENT)
        with self.assertRaises(AttributeError):
            image.source = IMAGE_SOURCE

        image = self._make_one(CLIENT_MOCK, source_uri=IMAGE_SOURCE)
        self.assertEqual(IMAGE_SOURCE, image.source)
        with self.assertRaises(AttributeError):
            image.content = IMAGE_CONTENT

    def test_image_from_filename(self):
        from mock import mock_open
        from mock import patch

        as_dict = {
            'content': B64_IMAGE_CONTENT,
        }

        with patch('google.cloud.vision.image.open',
                   mock_open(read_data=IMAGE_CONTENT)) as m:
            image = self._make_one(CLIENT_MOCK, filename='my-image-file.jpg')
        m.assert_called_once_with('my-image-file.jpg', 'rb')
        self.assertEqual(image.content, IMAGE_CONTENT)
        self.assertEqual(image.as_dict(), as_dict)
