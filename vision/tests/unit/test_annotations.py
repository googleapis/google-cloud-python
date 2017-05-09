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


def _make_pb_entity():
    from google.cloud.proto.vision.v1 import geometry_pb2
    from google.cloud.proto.vision.v1 import image_annotator_pb2
    from google.type import latlng_pb2

    description = 'testing 1 2 3'
    locale = 'US'
    mid = 'm/w/45342234'
    score = 0.390625

    entity_annotation = image_annotator_pb2.EntityAnnotation(
        mid=mid,
        locale=locale,
        description=description,
        score=score,
        bounding_poly=geometry_pb2.BoundingPoly(
            vertices=[
                geometry_pb2.Vertex(x=1, y=2),
            ],
        ),
        locations=[
            image_annotator_pb2.LocationInfo(
                lat_lng=latlng_pb2.LatLng(latitude=1.0, longitude=2.0),
            ),
        ],
    )
    return entity_annotation


class TestAnnotations(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.annotations import Annotations

        return Annotations

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        annotations = self._make_one(
            faces=[True], properties=[True], labels=[True], landmarks=[True],
            logos=[True], safe_searches=[True], texts=[True])
        self.assertEqual(annotations.faces, [True])
        self.assertEqual(annotations.properties, [True])
        self.assertEqual(annotations.labels, [True])
        self.assertEqual(annotations.landmarks, [True])
        self.assertEqual(annotations.logos, [True])
        self.assertEqual(annotations.safe_searches, [True])
        self.assertEqual(annotations.texts, [True])

    def test_unsupported_http_annotation(self):
        returned = {
            'responses': [
                {'someMadeUpAnnotation': None},
            ],
        }
        annotation = self._get_target_class().from_api_repr(returned)
        self.assertIsInstance(annotation, self._get_target_class())

    def test_from_pb(self):
        from google.cloud.vision.likelihood import Likelihood
        from google.cloud.vision.safe_search import SafeSearchAnnotation
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        image_response = image_annotator_pb2.AnnotateImageResponse()
        annotations = self._make_one().from_pb(image_response)
        self.assertEqual(annotations.labels, [])
        self.assertEqual(annotations.logos, [])
        self.assertEqual(annotations.faces, [])
        self.assertEqual(annotations.landmarks, [])
        self.assertEqual(annotations.texts, [])
        self.assertIsNone(annotations.properties)

        self.assertIsInstance(annotations.safe_searches, SafeSearchAnnotation)
        safe_search = annotations.safe_searches
        unknown = Likelihood.UNKNOWN
        self.assertIs(safe_search.adult, unknown)
        self.assertIs(safe_search.spoof, unknown)
        self.assertIs(safe_search.medical, unknown)
        self.assertIs(safe_search.violence, unknown)


class Test__make_entity_from_pb(unittest.TestCase):
    def _call_fut(self, annotations):
        from google.cloud.vision.annotations import _make_entity_from_pb

        return _make_entity_from_pb(annotations)

    def test_it(self):
        description = 'testing 1 2 3'
        locale = 'US'
        mid = 'm/w/45342234'
        score = 0.390625
        entity_annotation = _make_pb_entity()
        entities = self._call_fut([entity_annotation])
        self.assertEqual(len(entities), 1)
        entity = entities[0]
        self.assertEqual(entity.description, description)
        self.assertEqual(entity.mid, mid)
        self.assertEqual(entity.locale, locale)
        self.assertEqual(entity.score, score)
        self.assertEqual(len(entity.bounds.vertices), 1)
        self.assertEqual(entity.bounds.vertices[0].x_coordinate, 1)
        self.assertEqual(entity.bounds.vertices[0].y_coordinate, 2)
        self.assertEqual(len(entity.locations), 1)
        self.assertEqual(entity.locations[0].latitude, 1.0)
        self.assertEqual(entity.locations[0].longitude, 2.0)


class Test__make_faces_from_pb(unittest.TestCase):
    def _call_fut(self, annotations):
        from google.cloud.vision.annotations import _make_faces_from_pb

        return _make_faces_from_pb(annotations)

    def test_it(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.cloud.vision.face import Face

        faces_pb = [image_annotator_pb2.FaceAnnotation()]

        faces = self._call_fut(faces_pb)
        self.assertIsInstance(faces[0], Face)


class Test__make_image_properties_from_pb(unittest.TestCase):
    def _call_fut(self, annotations):
        from google.cloud.vision.annotations import (
            _make_image_properties_from_pb)

        return _make_image_properties_from_pb(annotations)

    def test_it(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.protobuf.wrappers_pb2 import FloatValue
        from google.type.color_pb2 import Color

        alpha = FloatValue(value=1.0)
        color_pb = Color(red=1.0, green=2.0, blue=3.0, alpha=alpha)
        color_info_pb = image_annotator_pb2.ColorInfo(color=color_pb,
                                                      score=1.0,
                                                      pixel_fraction=1.0)
        dominant_colors = image_annotator_pb2.DominantColorsAnnotation(
            colors=[color_info_pb])

        image_properties_pb = image_annotator_pb2.ImageProperties(
            dominant_colors=dominant_colors)

        image_properties = self._call_fut(image_properties_pb)
        self.assertEqual(image_properties.colors[0].pixel_fraction, 1.0)
        self.assertEqual(image_properties.colors[0].score, 1.0)
        self.assertEqual(image_properties.colors[0].color.red, 1.0)
        self.assertEqual(image_properties.colors[0].color.green, 2.0)
        self.assertEqual(image_properties.colors[0].color.blue, 3.0)
        self.assertEqual(image_properties.colors[0].color.alpha, 1.0)


class Test__process_image_annotations(unittest.TestCase):
    def _call_fut(self, image):
        from google.cloud.vision.annotations import _process_image_annotations

        return _process_image_annotations(image)

    def test_it(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        description = 'testing 1 2 3'
        locale = 'US'
        mid = 'm/w/45342234'
        score = 0.390625
        entity_annotation = _make_pb_entity()

        image_response = image_annotator_pb2.AnnotateImageResponse(
            label_annotations=[entity_annotation])

        annotations = self._call_fut(image_response)
        self.assertEqual(len(annotations['labels']), 1)
        entity = annotations['labels'][0]

        self.assertEqual(entity.description, description)
        self.assertEqual(entity.mid, mid)
        self.assertEqual(entity.locale, locale)
        self.assertEqual(entity.score, score)
        self.assertEqual(len(entity.bounds.vertices), 1)
        self.assertEqual(entity.bounds.vertices[0].x_coordinate, 1)
        self.assertEqual(entity.bounds.vertices[0].y_coordinate, 2)
        self.assertEqual(len(entity.locations), 1)
        self.assertEqual(entity.locations[0].latitude, 1.0)
        self.assertEqual(entity.locations[0].longitude, 2.0)
