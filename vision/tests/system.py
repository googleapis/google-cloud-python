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

import six

from google.cloud import exceptions
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id


_SYS_TESTS_DIR = os.path.realpath(os.path.dirname(__file__))
LOGO_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'logo.png')
FACE_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'faces.jpg')
LABEL_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'car.jpg')
LANDMARK_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'landmark.jpg')
TEXT_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'text.jpg')
FULL_TEXT_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'full-text.jpg')


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


class BaseVisionTestCase(unittest.TestCase):
    def _assert_coordinate(self, coordinate):
        if coordinate is None:
            return
        self.assertIsNotNone(coordinate)
        self.assertIsInstance(coordinate, (int, float))

    def _assert_likelihood(self, likelihood):
        from google.cloud.vision.likelihood import Likelihood

        levels = [Likelihood.UNKNOWN, Likelihood.VERY_LIKELY,
                  Likelihood.UNLIKELY, Likelihood.POSSIBLE, Likelihood.LIKELY,
                  Likelihood.VERY_UNLIKELY]
        self.assertIn(likelihood, levels)

    def _pb_not_implemented_skip(self, message):
        if Config.CLIENT._use_gax:
            self.skipTest(message)


class TestVisionFullText(unittest.TestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_full_text(self, full_text):
        from google.cloud.vision.text import TextAnnotation

        self.assertIsInstance(full_text, TextAnnotation)
        self.assertIsInstance(full_text.text, six.text_type)
        self.assertEqual(len(full_text.pages), 1)
        self.assertIsInstance(full_text.pages[0].width, int)
        self.assertIsInstance(full_text.pages[0].height, int)

    def test_detect_full_text_content(self):
        client = Config.CLIENT
        with open(FULL_TEXT_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        full_text = image.detect_full_text(language_hints=['en'])
        self._assert_full_text(full_text)

    def test_detect_full_text_filename(self):
        client = Config.CLIENT
        image = client.image(filename=FULL_TEXT_FILE)
        full_text = image.detect_full_text(language_hints=['en'])
        self._assert_full_text(full_text)

    def test_detect_full_text_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'full-text.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FULL_TEXT_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        full_text = image.detect_full_text(language_hints=['en'])
        self._assert_full_text(full_text)


class TestVisionClientCropHint(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_crop_hint(self, hint):
        from google.cloud.vision.crop_hint import CropHint
        from google.cloud.vision.geometry import Bounds

        self.assertIsInstance(hint, CropHint)
        self.assertIsInstance(hint.bounds, Bounds)
        self.assertGreater(len(hint.bounds.vertices), 1)
        self.assertIsInstance(hint.confidence, (int, float))
        self.assertIsInstance(hint.importance_fraction, float)

    def test_detect_crop_hints_content(self):
        client = Config.CLIENT
        with open(FACE_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        crop_hints = image.detect_crop_hints(
            aspect_ratios=[1.3333, 1.7777], limit=2)
        self.assertEqual(len(crop_hints), 2)
        for hint in crop_hints:
            self._assert_crop_hint(hint)

    def test_detect_crop_hints_filename(self):
        client = Config.CLIENT
        image = client.image(filename=FACE_FILE)
        crop_hints = image.detect_crop_hints(
            aspect_ratios=[1.3333, 1.7777], limit=2)
        self.assertEqual(len(crop_hints), 2)
        for hint in crop_hints:
            self._assert_crop_hint(hint)

    def test_detect_crop_hints_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'faces.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FACE_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        crop_hints = image.detect_crop_hints(
            aspect_ratios=[1.3333, 1.7777], limit=2)
        self.assertEqual(len(crop_hints), 2)
        for hint in crop_hints:
            self._assert_crop_hint(hint)


class TestVisionClientLogo(unittest.TestCase):
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


class TestVisionClientFace(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_landmarks(self, landmarks):
        from google.cloud.vision.face import Landmark
        from google.cloud.vision.face import LandmarkTypes
        from google.cloud.vision.face import Position

        for landmark in LandmarkTypes:
            if landmark is not LandmarkTypes.UNKNOWN_LANDMARK:
                feature = getattr(landmarks, landmark.name.lower())
                self.assertIsInstance(feature, Landmark)
                self.assertIsInstance(feature.position, Position)
                self._assert_coordinate(feature.position.x_coordinate)
                self._assert_coordinate(feature.position.y_coordinate)
                self._assert_coordinate(feature.position.z_coordinate)

    def _assert_face(self, face):
        from google.cloud.vision.face import Bounds
        from google.cloud.vision.face import FDBounds
        from google.cloud.vision.face import Face
        from google.cloud.vision.face import Landmarks
        from google.cloud.vision.geometry import Vertex

        self.assertIsInstance(face, Face)
        self.assertGreater(face.detection_confidence, 0.0)
        self._assert_likelihood(face.anger)
        self._assert_likelihood(face.joy)
        self._assert_likelihood(face.sorrow)
        self._assert_likelihood(face.surprise)
        self._assert_likelihood(face.image_properties.blurred)
        self._assert_likelihood(face.image_properties.underexposed)
        self._assert_likelihood(face.headwear)
        self.assertNotEqual(face.angles.roll, 0.0)
        self.assertNotEqual(face.angles.pan, 0.0)
        self.assertNotEqual(face.angles.tilt, 0.0)

        self.assertIsInstance(face.bounds, Bounds)
        for vertex in face.bounds.vertices:
            self.assertIsInstance(vertex, Vertex)
            self._assert_coordinate(vertex.x_coordinate)
            self._assert_coordinate(vertex.y_coordinate)

        self.assertIsInstance(face.fd_bounds, FDBounds)
        for vertex in face.fd_bounds.vertices:
            self.assertIsInstance(vertex, Vertex)
            self._assert_coordinate(vertex.x_coordinate)
            self._assert_coordinate(vertex.y_coordinate)

        self.assertIsInstance(face.landmarks, Landmarks)
        self._assert_landmarks(face.landmarks)

    def test_detect_faces_content(self):
        client = Config.CLIENT
        with open(FACE_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        faces = image.detect_faces()
        self.assertEqual(len(faces), 5)
        for face in faces:
            self._assert_face(face)

    def test_detect_faces_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'faces.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FACE_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        faces = image.detect_faces()
        self.assertEqual(len(faces), 5)
        for face in faces:
            self._assert_face(face)

    def test_detect_faces_filename(self):
        client = Config.CLIENT
        image = client.image(filename=FACE_FILE)
        faces = image.detect_faces()
        self.assertEqual(len(faces), 5)
        for face in faces:
            self._assert_face(face)


class TestVisionClientLabel(BaseVisionTestCase):
    DESCRIPTIONS = (
        'car',
        'vehicle',
        'land vehicle',
        'automotive design',
        'wheel',
        'automobile make',
        'luxury vehicle',
        'sports car',
        'performance car',
        'automotive exterior',
    )

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_label(self, label):
        self.assertIsInstance(label, EntityAnnotation)
        self.assertIn(label.description, self.DESCRIPTIONS)
        self.assertIsInstance(label.mid, six.text_type)
        self.assertGreater(label.score, 0.0)

    def test_detect_labels_content(self):
        client = Config.CLIENT
        with open(LABEL_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        labels = image.detect_labels()
        self.assertEqual(len(labels), 10)
        for label in labels:
            self._assert_label(label)

    def test_detect_labels_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'car.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(LABEL_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        labels = image.detect_labels()
        self.assertEqual(len(labels), 10)
        for label in labels:
            self._assert_label(label)

    def test_detect_labels_filename(self):
        client = Config.CLIENT
        image = client.image(filename=LABEL_FILE)
        labels = image.detect_labels()
        self.assertEqual(len(labels), 10)
        for label in labels:
            self._assert_label(label)


class TestVisionClientLandmark(BaseVisionTestCase):
    DESCRIPTIONS = ('Mount Rushmore',)

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_landmark(self, landmark):
        self.assertIsInstance(landmark, EntityAnnotation)
        self.assertIn(landmark.description, self.DESCRIPTIONS)
        self.assertEqual(len(landmark.locations), 1)
        location = landmark.locations[0]
        self._assert_coordinate(location.latitude)
        self._assert_coordinate(location.longitude)
        for vertex in landmark.bounds.vertices:
            self._assert_coordinate(vertex.x_coordinate)
            self._assert_coordinate(vertex.y_coordinate)
        self.assertGreater(landmark.score, 0.2)
        self.assertIsInstance(landmark.mid, six.text_type)

    def test_detect_landmark_content(self):
        client = Config.CLIENT
        with open(LANDMARK_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        landmarks = image.detect_landmarks()
        self.assertEqual(len(landmarks), 1)
        landmark = landmarks[0]
        self._assert_landmark(landmark)

    def test_detect_landmark_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'landmark.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(LANDMARK_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        landmarks = image.detect_landmarks()
        self.assertEqual(len(landmarks), 1)
        landmark = landmarks[0]
        self._assert_landmark(landmark)

    def test_detect_landmark_filename(self):
        client = Config.CLIENT
        image = client.image(filename=LANDMARK_FILE)
        landmarks = image.detect_landmarks()
        self.assertEqual(len(landmarks), 1)
        landmark = landmarks[0]
        self._assert_landmark(landmark)


class TestVisionClientSafeSearch(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_safe_search(self, safe_search):
        from google.cloud.vision.safe_search import SafeSearchAnnotation

        self.assertIsInstance(safe_search, SafeSearchAnnotation)
        self._assert_likelihood(safe_search.adult)
        self._assert_likelihood(safe_search.spoof)
        self._assert_likelihood(safe_search.medical)
        self._assert_likelihood(safe_search.violence)

    def test_detect_safe_search_content(self):
        client = Config.CLIENT
        with open(FACE_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        safe_search = image.detect_safe_search()
        self._assert_safe_search(safe_search)

    def test_detect_safe_search_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'faces.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FACE_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        safe_search = image.detect_safe_search()
        self._assert_safe_search(safe_search)

    def test_detect_safe_search_filename(self):
        client = Config.CLIENT
        image = client.image(filename=FACE_FILE)
        safe_search = image.detect_safe_search()
        self._assert_safe_search(safe_search)


class TestVisionClientText(unittest.TestCase):
    DESCRIPTIONS = (
        'Do',
        'what',
        'is',
        'right,',
        'not',
        'what',
        'is',
        'easy',
        'Do what is\nright, not\nwhat is easy\n',
    )

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_text(self, text):
        self.assertIsInstance(text, EntityAnnotation)
        self.assertIn(text.description, self.DESCRIPTIONS)
        self.assertIn(text.locale, (None, '', 'en'))
        self.assertIsInstance(text.score, (type(None), float))

    def test_detect_text_content(self):
        client = Config.CLIENT
        with open(TEXT_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        texts = image.detect_text()
        self.assertEqual(len(texts), 9)
        for text in texts:
            self._assert_text(text)

    def test_detect_text_gcs(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'text.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(TEXT_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        client = Config.CLIENT
        image = client.image(source_uri=source_uri)
        texts = image.detect_text()
        self.assertEqual(len(texts), 9)
        for text in texts:
            self._assert_text(text)

    def test_detect_text_filename(self):
        client = Config.CLIENT
        image = client.image(filename=TEXT_FILE)
        texts = image.detect_text()
        self.assertEqual(len(texts), 9)
        for text in texts:
            self._assert_text(text)


class TestVisionClientImageProperties(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_color(self, color):
        self.assertIsInstance(color.red, float)
        self.assertIsInstance(color.green, float)
        self.assertIsInstance(color.blue, float)
        self.assertIsInstance(color.alpha, float)
        self.assertNotEqual(color.red, 0.0)
        self.assertNotEqual(color.green, 0.0)
        self.assertNotEqual(color.blue, 0.0)

    def _assert_properties(self, image_property):
        from google.cloud.vision.color import ImagePropertiesAnnotation

        self.assertIsInstance(image_property, ImagePropertiesAnnotation)
        results = image_property.colors
        for color_info in results:
            self._assert_color(color_info.color)
            self.assertNotEqual(color_info.pixel_fraction, 0.0)
            self.assertNotEqual(color_info.score, 0.0)

    def test_detect_properties_content(self):
        client = Config.CLIENT
        with open(FACE_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        properties = image.detect_properties()
        self._assert_properties(properties)

    def test_detect_properties_gcs(self):
        client = Config.CLIENT
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'faces.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FACE_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        image = client.image(source_uri=source_uri)
        properties = image.detect_properties()
        self._assert_properties(properties)

    def test_detect_properties_filename(self):
        client = Config.CLIENT
        image = client.image(filename=FACE_FILE)
        properties = image.detect_properties()
        self._assert_properties(properties)


class TestVisionBatchProcessing(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def test_batch_detect_gcs(self):
        client = Config.CLIENT
        bucket_name = Config.TEST_BUCKET.name

        # Logo GCS image.
        blob_name = 'logos.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(LOGO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        logo_source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        image_one = client.image(source_uri=logo_source_uri)
        logo_feature = Feature(FeatureTypes.LOGO_DETECTION, 2)

        # Faces GCS image.
        blob_name = 'faces.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(FACE_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        face_source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        image_two = client.image(source_uri=face_source_uri)
        face_feature = Feature(FeatureTypes.FACE_DETECTION, 2)

        batch = client.batch()
        batch.add_image(image_one, [logo_feature])
        batch.add_image(image_two, [face_feature, logo_feature])
        results = batch.detect()
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], vision.annotations.Annotations)
        self.assertIsInstance(results[1], vision.annotations.Annotations)
        self.assertEqual(len(results[0].logos), 1)
        self.assertEqual(len(results[0].faces), 0)

        self.assertEqual(len(results[1].logos), 0)
        self.assertEqual(len(results[1].faces), 2)


class TestVisionWebAnnotation(BaseVisionTestCase):
    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _assert_web_entity(self, web_entity):
        from google.cloud.vision.web import WebEntity

        self.assertIsInstance(web_entity, WebEntity)
        self.assertIsInstance(web_entity.entity_id, six.text_type)
        self.assertIsInstance(web_entity.score, float)
        self.assertIsInstance(web_entity.description, six.text_type)

    def _assert_web_image(self, web_image):
        from google.cloud.vision.web import WebImage

        self.assertIsInstance(web_image, WebImage)
        self.assertIsInstance(web_image.url, six.text_type)
        self.assertIsInstance(web_image.score, float)

    def _assert_web_page(self, web_page):
        from google.cloud.vision.web import WebPage

        self.assertIsInstance(web_page, WebPage)
        self.assertIsInstance(web_page.url, six.text_type)
        self.assertIsInstance(web_page.score, float)

    def _assert_web_images(self, web_images, limit):
        self.assertEqual(len(web_images.web_entities), limit)
        for web_entity in web_images.web_entities:
            self._assert_web_entity(web_entity)

        self.assertEqual(len(web_images.full_matching_images), limit)
        for web_image in web_images.full_matching_images:
            self._assert_web_image(web_image)

        self.assertEqual(len(web_images.partial_matching_images), limit)
        for web_image in web_images.partial_matching_images:
            self._assert_web_image(web_image)

        self.assertEqual(len(web_images.pages_with_matching_images), limit)
        for web_page in web_images.pages_with_matching_images:
            self._assert_web_page(web_page)

    def test_detect_web_images_from_content(self):
        client = Config.CLIENT
        with open(LANDMARK_FILE, 'rb') as image_file:
            image = client.image(content=image_file.read())
        limit = 5
        web_images = image.detect_web(limit=limit)
        self._assert_web_images(web_images, limit)

    def test_detect_web_images_from_gcs(self):
        client = Config.CLIENT
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'landmark.jpg'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(LANDMARK_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)

        image = client.image(source_uri=source_uri)
        limit = 5
        web_images = image.detect_web(limit=limit)
        self._assert_web_images(web_images, limit)

    def test_detect_web_images_from_filename(self):
        client = Config.CLIENT
        image = client.image(filename=LANDMARK_FILE)
        limit = 5
        web_images = image.detect_web(limit=limit)
        self._assert_web_images(web_images, limit)
