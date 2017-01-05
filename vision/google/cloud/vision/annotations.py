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


from google.cloud.vision.color import ImagePropertiesAnnotation
from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.face import Face
from google.cloud.vision.safe import SafeSearchAnnotation


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
        List of :class:`~google.cloud.vision.safe.SafeSearchAnnotation`

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
        annotations = {}
        for feature_type, annotation in response.items():
            curr_feature = annotations.setdefault(_KEY_MAP[feature_type], [])
            curr_feature.extend(
                _entity_from_response_type(feature_type, annotation))
        return cls(**annotations)

    @classmethod
    def from_pb(cls, response):
        """Factory: construct an instance of ``Annotations`` from protobuf.

        :type response: :class:`~google.cloud.grpc.vision.v1.\
                        image_annotator_pb2.AnnotateImageResponse`
        :param response: ``AnnotateImageResponse`` from protobuf call.

        :rtype: :class:`~google.cloud.vision.annotations.Annotations`
        :returns: ``Annotations`` instance populated from gRPC response.
        """
        annotations = _process_image_annotations(response)
        return cls(**annotations)


def _process_image_annotations(image):
    """Helper for processing annotation types from protobuf.

    :type image: :class:`~google.cloud.grpc.vision.v1.image_annotator_pb2.\
                 AnnotateImageResponse`
    :param image: ``AnnotateImageResponse`` from protobuf.

    :rtype: dict
    :returns: Dictionary populated with entities from response.
    """
    return {
        'labels': _make_entity_from_pb(image.label_annotations),
        'landmarks': _make_entity_from_pb(image.landmark_annotations),
        'logos': _make_entity_from_pb(image.logo_annotations),
        'texts': _make_entity_from_pb(image.text_annotations),
    }


def _make_entity_from_pb(annotations):
    """Create an entity from a gRPC response.

    :type annotations:
    :class:`~google.cloud.grpc.vision.v1.image_annotator_pb2.EntityAnnotation`
    :param annotations: protobuf instance of ``EntityAnnotation``.

    :rtype: list
    :returns: List of ``EntityAnnotation``.
    """
    return [EntityAnnotation.from_pb(annotation) for annotation in annotations]


def _entity_from_response_type(feature_type, results):
    """Convert a JSON result to an entity type based on the feature.

    :rtype: list
    :returns: List containing any of
              :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`,
              :class:`~google.cloud.vision.entity.EntityAnnotation`,
              :class:`~google.cloud.vision.face.Face`,
              :class:`~google.cloud.vision.safe.SafeSearchAnnotation`.
    """
    detected_objects = []
    if feature_type == _FACE_ANNOTATIONS:
        detected_objects.extend(
            Face.from_api_repr(face) for face in results)
    elif feature_type == _IMAGE_PROPERTIES_ANNOTATION:
        detected_objects.append(
            ImagePropertiesAnnotation.from_api_repr(results))
    elif feature_type == _SAFE_SEARCH_ANNOTATION:
        detected_objects.append(SafeSearchAnnotation.from_api_repr(results))
    else:
        for result in results:
            detected_objects.append(EntityAnnotation.from_api_repr(result))
    return detected_objects
