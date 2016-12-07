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
import six


_SYS_TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
LOGO_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'logo.png')
FACE_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'faces.jpg')
LABEL_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'car.jpg')
LANDMARK_FILE = os.path.join(_SYS_TESTS_DIR, 'data', 'landmark.jpg')


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
        self.assertIsInstance(coordinate, (int, float))
        self.assertNotEqual(coordinate, 0.0)


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

    def _assert_likelihood(self, likelihood):
        from google.cloud.vision.likelihood import Likelihood

        levels = [Likelihood.UNKNOWN, Likelihood.VERY_LIKELY,
                  Likelihood.UNLIKELY, Likelihood.POSSIBLE, Likelihood.LIKELY,
                  Likelihood.VERY_UNLIKELY]
        self.assertIn(likelihood, levels)

    def _assert_landmarks(self, landmarks):
        from google.cloud.vision.face import Landmark
        from google.cloud.vision.face import LandmarkTypes
        from google.cloud.vision.face import Position

        for landmark in LandmarkTypes:
            if landmark is not LandmarkTypes.UNKNOWN_LANDMARK:
                feature = getattr(landmarks, landmark.value.lower())
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
    DESCRIPTIONS = ('Mount Rushmore')

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
