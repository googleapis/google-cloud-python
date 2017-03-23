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
        from tests.unit._fixtures import FACE_DETECTION_RESPONSE

        self.face_annotations = FACE_DETECTION_RESPONSE['responses'][0]
        self.face_class = self._get_target_class()
        self.face = self.face_class.from_api_repr(
            self.face_annotations['faceAnnotations'][0])

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

        self.assertEqual(self.face.landmarking_confidence, 0.54453093)
        self.assertEqual(self.face.detection_confidence, 0.9863683)
        self.assertTrue(hasattr(self.face.landmarks, 'left_eye'))
        left_eye = self.face.landmarks.left_eye
        self.assertEqual(left_eye.position.x_coordinate, 1004.8003)
        self.assertEqual(left_eye.position.y_coordinate, 482.69385)
        self.assertEqual(left_eye.position.z_coordinate, 0.0016593217)
        self.assertEqual(left_eye.landmark_type, LandmarkTypes.LEFT_EYE)

    def test_facial_emotions(self):
        from google.cloud.vision.face import Likelihood

        self.assertEqual(self.face.joy, Likelihood.VERY_LIKELY)
        self.assertEqual(self.face.sorrow, Likelihood.VERY_UNLIKELY)
        self.assertEqual(self.face.surprise, Likelihood.VERY_UNLIKELY)
        self.assertEqual(self.face.anger, Likelihood.VERY_UNLIKELY)

    def test_facial_angles(self):
        self.assertEqual(self.face.angles.roll, -0.43419784)
        self.assertEqual(self.face.angles.pan, 6.027647)
        self.assertEqual(self.face.angles.tilt, -18.412321)

    def test_face_headware_and_blur_and_underexposed(self):
        from google.cloud.vision.face import Likelihood

        very_unlikely = Likelihood.VERY_UNLIKELY
        image_properties = self.face.image_properties
        self.assertEqual(image_properties.blurred, very_unlikely)
        self.assertEqual(image_properties.underexposed, very_unlikely)
        self.assertEqual(self.face.headwear, Likelihood.VERY_UNLIKELY)

    def test_face_bounds(self):
        self.assertEqual(len(self.face.bounds.vertices), 4)
        vertex = self.face.bounds.vertices[0]
        self.assertEqual(vertex.x_coordinate, 748)
        self.assertEqual(vertex.y_coordinate, 58)

    def test_facial_skin_bounds(self):
        self.assertEqual(len(self.face.fd_bounds.vertices), 4)
        vertex = self.face.bounds.vertices[1]
        self.assertEqual(vertex.x_coordinate, 1430)
        self.assertEqual(vertex.y_coordinate, 58)
