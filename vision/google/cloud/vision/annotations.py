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

"""Annotations management for Vision API responses."""

import six

from google.cloud.vision.color import ImagePropertiesAnnotation
from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.face import Face
from google.cloud.vision.safe_search import SafeSearchAnnotation


_FACE_ANNOTATIONS = 'faceAnnotations'
_IMAGE_PROPERTIES_ANNOTATION = 'imagePropertiesAnnotation'
_SAFE_SEARCH_ANNOTATION = 'safeSearchAnnotation'

_KEY_MAP = {
    _FACE_ANNOTATIONS: 'faces',
    _IMAGE_PROPERTIES_ANNOTATION: 'properties',
    'labelAnnotations': 'labels',
    'landmarkAnnotations': 'landmarks',
    'logoAnnotations': 'logos',
    _SAFE_SEARCH_ANNOTATION: 'safe_searches',
    'textAnnotations': 'texts'
}


class Annotations(object):
    """Helper class to bundle annotation responses.

    :type faces: list
    :param faces: List of :class:`~google.cloud.vision.face.Face`.

    :type properties: list
    :param properties:
        List of :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.

    :type labels: list
    :param labels: List of
                   :class:`~google.cloud.vision.entity.EntityAnnotation`.

    :type landmarks: list
    :param landmarks: List of
                      :class:`~google.cloud.vision.entity.EntityAnnotation.`

    :type logos: list
    :param logos: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.

    :type safe_searches: list
    :param safe_searches:
        List of :class:`~google.cloud.vision.safe_search.SafeSearchAnnotation`

    :type texts: list
    :param texts: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
    """
    def __init__(self, faces=(), properties=(), labels=(), landmarks=(),
                 logos=(), safe_searches=(), texts=()):
        self.faces = faces
        self.properties = properties
        self.labels = labels
        self.landmarks = landmarks
        self.logos = logos
        self.safe_searches = safe_searches
        self.texts = texts

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct an instance of ``Annotations`` from a response.

        :type response: dict
        :param response: Vision API response object.

        :rtype: :class:`~google.cloud.vision.annotations.Annotations`
        :returns: An instance of ``Annotations`` with detection types loaded.
        """
        annotations = {
            _KEY_MAP[feature_type]: _entity_from_response_type(
                feature_type, annotation)
            for feature_type, annotation in six.iteritems(response)
            if feature_type in _KEY_MAP
        }
        return cls(**annotations)

    @classmethod
    def from_pb(cls, response):
        """Factory: construct an instance of ``Annotations`` from protobuf.

        :type response: :class:`~google.cloud.proto.vision.v1.\
                        image_annotator_pb2.AnnotateImageResponse`
        :param response: ``AnnotateImageResponse`` from protobuf call.

        :rtype: :class:`~google.cloud.vision.annotations.Annotations`
        :returns: ``Annotations`` instance populated from gRPC response.
        """
        annotations = _process_image_annotations(response)
        return cls(**annotations)


def _process_image_annotations(image):
    """Helper for processing annotation types from protobuf.

    :type image: :class:`~google.cloud.proto.vision.v1.image_annotator_pb2.\
                 AnnotateImageResponse`
    :param image: ``AnnotateImageResponse`` from protobuf.

    :rtype: dict
    :returns: Dictionary populated with entities from response.
    """
    return {
        'faces': _make_faces_from_pb(image.face_annotations),
        'labels': _make_entity_from_pb(image.label_annotations),
        'landmarks': _make_entity_from_pb(image.landmark_annotations),
        'logos': _make_entity_from_pb(image.logo_annotations),
        'properties': _make_image_properties_from_pb(
            image.image_properties_annotation),
        'safe_searches': _make_safe_search_from_pb(
            image.safe_search_annotation),
        'texts': _make_entity_from_pb(image.text_annotations),
    }


def _make_entity_from_pb(annotations):
    """Create an entity from a protobuf response.

    :type annotations:
    :class:`~google.cloud.proto.vision.v1.image_annotator_pb2.EntityAnnotation`
    :param annotations: protobuf instance of ``EntityAnnotation``.

    :rtype: list
    :returns: List of ``EntityAnnotation``.
    """
    return [EntityAnnotation.from_pb(annotation) for annotation in annotations]


def _make_faces_from_pb(faces):
    """Create face objects from a protobuf response.

    :type faces:
    :class:`~google.cloud.proto.vision.v1.image_annotator_pb2.FaceAnnotation`
    :param faces: Protobuf instance of ``FaceAnnotation``.

    :rtype: list
    :returns: List of ``Face``.
    """
    return [Face.from_pb(face) for face in faces]


def _make_image_properties_from_pb(image_properties):
    """Create ``ImageProperties`` object from a protobuf response.

    :type image_properties: :class:`~google.cloud.proto.vision.v1.\
                            image_annotator_pb2.ImagePropertiesAnnotation`
    :param image_properties: Protobuf instance of
                             ``ImagePropertiesAnnotation``.

    :rtype: list or ``None``
    :returns: List of ``ImageProperties`` or ``None``.
    """
    return ImagePropertiesAnnotation.from_pb(image_properties)


def _make_safe_search_from_pb(safe_search):
    """Create ``SafeSearchAnnotation`` object from a protobuf response.

    :type safe_search: :class:`~google.cloud.proto.vision.v1.\
                            image_annotator_pb2.SafeSearchAnnotation`
    :param safe_search: Protobuf instance of ``SafeSearchAnnotation``.

    :rtype: :class: `~google.cloud.vision.safe_search.SafeSearchAnnotation`
    :returns: Instance of ``SafeSearchAnnotation``.
    """
    return SafeSearchAnnotation.from_pb(safe_search)


def _entity_from_response_type(feature_type, results):
    """Convert a JSON result to an entity type based on the feature.

    :rtype: list
    :returns: List containing any of
              :class:`~google.cloud.vision.entity.EntityAnnotation`,
              :class:`~google.cloud.vision.face.Face`

              or one of

              :class:`~google.cloud.vision.safe_search.SafeSearchAnnotation`,
              :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
    """
    detected_objects = []
    if feature_type == _FACE_ANNOTATIONS:
        detected_objects.extend(
            Face.from_api_repr(face) for face in results)
    elif feature_type == _IMAGE_PROPERTIES_ANNOTATION:
        return ImagePropertiesAnnotation.from_api_repr(results)
    elif feature_type == _SAFE_SEARCH_ANNOTATION:
        return SafeSearchAnnotation.from_api_repr(results)
    else:
        for result in results:
            detected_objects.append(EntityAnnotation.from_api_repr(result))
    return detected_objects
