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


class TestFace(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.face import Face
        return Face

    def _make_face_pb(self, *args, **kwargs):
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        return image_annotator_pb2.FaceAnnotation(*args, **kwargs)

    def setUp(self):
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE
        self.FACE_ANNOTATIONS = FACE_DETECTION_RESPONSE['responses'][0]
        self.face_class = self._get_target_class()
        self.face = self.face_class.from_api_repr(
            self.FACE_ANNOTATIONS['faceAnnotations'][0])

    def test_face_from_pb(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.cloud.proto.vision.v1 import geometry_pb2

        position_pb = geometry_pb2.Position(x=1.0, y=2.0, z=3.0)
        landmark_pb = image_annotator_pb2.FaceAnnotation.Landmark(
            position=position_pb, type=5)
        face_pb = self._make_face_pb(landmarks=[landmark_pb])

        face = self._get_target_class().from_pb(face_pb)
        self.assertIsInstance(face, self._get_target_class())

    def test_face_landmarks(self):
        from google.cloud.vision.face import LandmarkTypes

        self.assertEqual(0.54453093, self.face.landmarking_confidence)
        self.assertEqual(0.9863683, self.face.detection_confidence)
        self.assertTrue(hasattr(self.face.landmarks, 'left_eye'))
        self.assertEqual(1004.8003,
                         self.face.landmarks.left_eye.position.x_coordinate)
        self.assertEqual(482.69385,
                         self.face.landmarks.left_eye.position.y_coordinate)
        self.assertEqual(0.0016593217,
                         self.face.landmarks.left_eye.position.z_coordinate)
        self.assertEqual(self.face.landmarks.left_eye.landmark_type,
                         LandmarkTypes.LEFT_EYE)

    def test_facial_emotions(self):
        from google.cloud.vision.face import Likelihood
        self.assertEqual(Likelihood.VERY_LIKELY,
                         self.face.joy)
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.sorrow)
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.surprise)
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.anger)

    def test_faciale_angles(self):
        self.assertEqual(-0.43419784, self.face.angles.roll)
        self.assertEqual(6.027647, self.face.angles.pan)
        self.assertEqual(-18.412321, self.face.angles.tilt)

    def test_face_headware_and_blur_and_underexposed(self):
        from google.cloud.vision.face import Likelihood
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.image_properties.blurred)
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.headwear)
        self.assertEqual(Likelihood.VERY_UNLIKELY,
                         self.face.image_properties.underexposed)

    def test_face_bounds(self):
        self.assertEqual(4, len(self.face.bounds.vertices))
        self.assertEqual(748, self.face.bounds.vertices[0].x_coordinate)
        self.assertEqual(58, self.face.bounds.vertices[0].y_coordinate)

    def test_facial_skin_bounds(self):
        self.assertEqual(4, len(self.face.fd_bounds.vertices))
        self.assertEqual(845, self.face.fd_bounds.vertices[0].x_coordinate)
        self.assertEqual(310, self.face.fd_bounds.vertices[0].y_coordinate)
