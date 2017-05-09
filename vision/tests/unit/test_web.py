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


class TestWebDetection(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.web import WebDetection
        return WebDetection

    def _make_one(self, web_entities, full_matching_images,
                  partial_matching_images, pages_with_matching_images):
        return self._get_target_class()(web_entities, full_matching_images,
                                        partial_matching_images,
                                        pages_with_matching_images)

    def test_web_detection_ctor(self):
        web_detection = self._make_one(1, 2, 3, 4)
        self.assertEqual(web_detection.web_entities, 1)
        self.assertEqual(web_detection.full_matching_images, 2)
        self.assertEqual(web_detection.partial_matching_images, 3)
        self.assertEqual(web_detection.pages_with_matching_images, 4)

    def test_web_detection_from_api_repr(self):
        from google.cloud.vision.web import WebEntity
        from google.cloud.vision.web import WebImage
        from google.cloud.vision.web import WebPage

        web_detection_dict = {
            'partialMatchingImages': [{
                'url': 'https://cloud.google.com/vision',
                'score': 0.92234,
            }],
            'fullMatchingImages': [{
                'url': 'https://cloud.google.com/vision',
                'score': 0.92234,
            }],
            'webEntities': [{
                'entityId': '/m/05_5t0l',
                'score': 0.9468027,
                'description': 'Landmark'
            }],
            'pagesWithMatchingImages': [{
                'url': 'https://cloud.google.com/vision',
                'score': 0.92234,
            }],
        }
        web_detection = self._get_target_class().from_api_repr(
            web_detection_dict)
        self.assertEqual(len(web_detection.partial_matching_images), 1)
        self.assertEqual(len(web_detection.full_matching_images), 1)
        self.assertEqual(len(web_detection.web_entities), 1)
        self.assertEqual(len(web_detection.pages_with_matching_images), 1)

        self.assertIsInstance(web_detection.partial_matching_images[0],
                              WebImage)
        self.assertIsInstance(web_detection.full_matching_images[0], WebImage)
        self.assertIsInstance(web_detection.web_entities[0], WebEntity)
        self.assertIsInstance(web_detection.pages_with_matching_images[0],
                              WebPage)

    def test_web_detection_from_pb(self):
        from google.cloud.proto.vision.v1 import web_detection_pb2
        from google.cloud.vision.web import WebEntity
        from google.cloud.vision.web import WebImage
        from google.cloud.vision.web import WebPage

        description = 'Some images like the image you have.'
        entity_id = '/m/019dvv'
        score = 1470.4435
        url = 'http://cloud.google.com/vision'

        web_entity_pb = web_detection_pb2.WebDetection.WebEntity(
            entity_id=entity_id, score=score, description=description)

        web_image_pb = web_detection_pb2.WebDetection.WebImage(
            url=url, score=score)

        web_page_pb = web_detection_pb2.WebDetection.WebPage(
            url=url, score=score)

        web_detection_pb = web_detection_pb2.WebDetection(
            web_entities=[web_entity_pb], full_matching_images=[web_image_pb],
            partial_matching_images=[web_image_pb],
            pages_with_matching_images=[web_page_pb])
        web_detection = self._get_target_class().from_pb(web_detection_pb)
        self.assertEqual(len(web_detection.web_entities), 1)
        self.assertEqual(len(web_detection.full_matching_images), 1)
        self.assertEqual(len(web_detection.partial_matching_images), 1)
        self.assertEqual(len(web_detection.pages_with_matching_images), 1)
        self.assertIsInstance(web_detection.web_entities[0], WebEntity)
        self.assertIsInstance(web_detection.full_matching_images[0], WebImage)
        self.assertIsInstance(web_detection.partial_matching_images[0],
                              WebImage)
        self.assertIsInstance(web_detection.pages_with_matching_images[0],
                              WebPage)


class TestWebEntity(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.web import WebEntity
        return WebEntity

    def _make_one(self, entity_id, score, description):
        return self._get_target_class()(entity_id, score, description)

    def test_web_entity_ctor(self):
        entity_id = 'm/abc123'
        score = 0.13245
        description = 'This is an image from the web that matches your image.'
        web_entity = self._make_one(entity_id, score, description)
        self.assertEqual(web_entity.entity_id, entity_id)
        self.assertAlmostEqual(web_entity.score, score, 4)
        self.assertEqual(web_entity.description, description)

    def test_web_entity_from_api_repr(self):
        entity_dict = {
            'entityId': '/m/019dvv',
            'score': 1470.4435,
            'description': 'Mount Rushmore National Memorial',
        }
        web_entity = self._get_target_class().from_api_repr(entity_dict)

        self.assertEqual(web_entity.entity_id, entity_dict['entityId'])
        self.assertAlmostEqual(web_entity.score, entity_dict['score'], 4)
        self.assertEqual(web_entity.description, entity_dict['description'])

    def test_web_entity_from_pb(self):
        from google.cloud.proto.vision.v1 import web_detection_pb2

        entity_id = '/m/019dvv'
        score = 1470.4435
        description = 'Some images like the image you have.'
        web_entity_pb = web_detection_pb2.WebDetection.WebEntity(
            entity_id=entity_id, score=score, description=description)
        web_entity = self._get_target_class().from_pb(web_entity_pb)
        self.assertEqual(web_entity.entity_id, entity_id)
        self.assertAlmostEqual(web_entity.score, score, 4)
        self.assertEqual(web_entity.description, description)


class TestWebImage(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.web import WebImage
        return WebImage

    def _make_one(self, url, score):
        return self._get_target_class()(url, score)

    def test_web_image_ctor(self):
        url = 'http://cloud.google.com/vision'
        score = 1234.23
        web_image = self._make_one(url, score)
        self.assertEqual(web_image.url, url)
        self.assertAlmostEqual(web_image.score, score, 4)

    def test_web_image_from_api_repr(self):
        web_image_dict = {
            'url': 'http://cloud.google.com/vision',
            'score': 1234.23,
        }
        web_image = self._get_target_class().from_api_repr(web_image_dict)
        self.assertEqual(web_image.url, web_image_dict['url'])
        self.assertAlmostEqual(web_image.score, web_image_dict['score'])

    def test_web_image_from_pb(self):
        from google.cloud.proto.vision.v1 import web_detection_pb2

        url = 'http://cloud.google.com/vision'
        score = 1234.23
        web_image_pb = web_detection_pb2.WebDetection.WebImage(
            url=url, score=score)
        web_image = self._get_target_class().from_pb(web_image_pb)
        self.assertEqual(web_image.url, url)
        self.assertAlmostEqual(web_image.score, score, 4)


class TestWebPage(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.web import WebPage
        return WebPage

    def _make_one(self, url, score):
        return self._get_target_class()(url, score)

    def test_web_page_ctor(self):
        url = 'http://cloud.google.com/vision'
        score = 1234.23
        web_page = self._make_one(url, score)
        self.assertEqual(web_page.url, url)
        self.assertAlmostEqual(web_page.score, score, 4)

    def test_web_page_from_api_repr(self):
        web_page_dict = {
            'url': 'http://cloud.google.com/vision',
            'score': 1234.23,
        }
        web_page = self._get_target_class().from_api_repr(web_page_dict)
        self.assertEqual(web_page.url, web_page_dict['url'])
        self.assertAlmostEqual(web_page.score, web_page_dict['score'], 4)

    def test_web_page_from_pb(self):
        from google.cloud.proto.vision.v1 import web_detection_pb2

        url = 'http://cloud.google.com/vision'
        score = 1234.23
        web_page_pb = web_detection_pb2.WebDetection.WebPage(
            url=url, score=score)
        web_page = self._get_target_class().from_pb(web_page_pb)
        self.assertEqual(web_page.url, url)
        self.assertAlmostEqual(web_page.score, score, 4)
