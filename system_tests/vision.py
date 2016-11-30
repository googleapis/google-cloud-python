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

"""System tests for Vision API."""

import os
import unittest

from google.cloud import exceptions
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision.entity import EntityAnnotation

from system_test_utils import unique_resource_id
from retry import RetryErrors


_SYS_TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
LOGO_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'logo.png')


class Config(object):
    CLIENT = None
    TEST_BUCKET = None


def setUpModule():
    Config.CLIENT = vision.Client()
    storage_client = storage.Client()
    bucket_name = 'new' + unique_resource_id()
    Config.TEST_BUCKET = storage_client.bucket(bucket_name)
    # 429 Too Many Requests in case API requests rate-limited.
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    # 409 Conflict if the bucket is full.
    # 429 Too Many Requests in case API requests rate-limited.
    bucket_retry = RetryErrors(
        (exceptions.TooManyRequests, exceptions.Conflict))
    bucket_retry(Config.TEST_BUCKET.delete)(force=True)


class TestVisionClient(unittest.TestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_logo(self, logo):
        self.assertIsInstance(logo, EntityAnnotation)
        self.assertEqual(logo.description, 'Google')
        self.assertEqual(len(logo.bounds.vertices), 4)
        self.assertEqual(logo.bounds.vertices[0].x_coordinate, 40)
        self.assertEqual(logo.bounds.vertices[0].y_coordinate, 40)
        self.assertEqual(logo.bounds.vertices[1].x_coordinate, 959)
        self.assertEqual(logo.bounds.vertices[1].y_coordinate, 40)
        self.assertEqual(logo.bounds.vertices[2].x_coordinate, 959)
        self.assertEqual(logo.bounds.vertices[2].y_coordinate, 302)
        self.assertEqual(logo.bounds.vertices[3].x_coordinate, 40)
        self.assertEqual(logo.bounds.vertices[3].y_coordinate, 302)
        self.assertTrue(logo.score > 0.25)

    def test_detect_logos_content(self):
        client = Config.CLIENT
        with open(LOGO_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        logos = image.detect_logos()
        self.assertEqual(len(logos), 1)
        logo = logos[0]
        self._assert_logo(logo)

    def test_detect_logos_filename(self):
        client = Config.CLIENT
        image = client.image(filename=LOGO_FILE)
        logos = image.detect_logos()
        self.assertEqual(len(logos), 1)
        logo = logos[0]
        self._assert_logo(logo)

    def test_detect_logos_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'logo.png'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(LOGO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        logos = image.detect_logos()
        self.assertEqual(len(logos), 1)
        logo = logos[0]
        self._assert_logo(logo)
