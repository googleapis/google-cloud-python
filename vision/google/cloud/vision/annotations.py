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


from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.face import Face
from google.cloud.vision.feature import FeatureTypes
from google.cloud.vision.color import ImagePropertiesAnnotation
from google.cloud.vision.safe import SafeSearchAnnotation


_REVERSE_TYPES = {
    FeatureTypes.FACE_DETECTION: 'faceAnnotations',
    FeatureTypes.IMAGE_PROPERTIES: 'imagePropertiesAnnotation',
    FeatureTypes.LABEL_DETECTION: 'labelAnnotations',
    FeatureTypes.LANDMARK_DETECTION: 'landmarkAnnotations',
    FeatureTypes.LOGO_DETECTION: 'logoAnnotations',
    FeatureTypes.SAFE_SEARCH_DETECTION: 'safeSearchAnnotation',
    FeatureTypes.TEXT_DETECTION: 'textAnnotations',
}


class Annotations(object):
    """Annotation class for managing responses.

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
    def __init__(self, faces=None, properties=None, labels=None,
                 landmarks=None, logos=None, safe_searches=None, texts=None):
        self.faces = faces or []
        self.properties = properties or []
        self.labels = labels or []
        self.landmarks = landmarks or []
        self.logos = logos or []
        self.safe_searches = safe_searches or []
        self.texts = texts or []

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct an instance of ``Annotations`` from a response.

        :type response: dict
        :param response: Vision API response object.

        :rtype: :class:`~google.cloud.vision.annotations.Annotations`
        :returns: An instance of ``Annotations`` with detection types loaded.
        """
        annotations = {}

        for feature_type in response.keys():
            annotations[feature_type] = []

        for feature_type, annotation in response.items():
            annotations[feature_type].extend(
                _entity_from_response_type(feature_type, annotation))

        faces = annotations.get(
            _REVERSE_TYPES[FeatureTypes.FACE_DETECTION], [])
        properties = annotations.get(
            _REVERSE_TYPES[FeatureTypes.IMAGE_PROPERTIES], [])
        labels = annotations.get(
            _REVERSE_TYPES[FeatureTypes.LABEL_DETECTION], [])
        landmarks = annotations.get(
            _REVERSE_TYPES[FeatureTypes.LANDMARK_DETECTION], [])
        logos = annotations.get(
            _REVERSE_TYPES[FeatureTypes.LOGO_DETECTION], [])
        safe_searches = annotations.get(
            _REVERSE_TYPES[FeatureTypes.SAFE_SEARCH_DETECTION], [])
        texts = annotations.get(
            _REVERSE_TYPES[FeatureTypes.TEXT_DETECTION], [])

        return cls(faces=faces, properties=properties, labels=labels,
                   landmarks=landmarks, logos=logos,
                   safe_searches=safe_searches, texts=texts)


def _entity_from_response_type(feature_type, results):
    """Convert a JSON result to an entity type based on the feature."""

    detected_objects = []
    if feature_type == _REVERSE_TYPES[FeatureTypes.FACE_DETECTION]:
        detected_objects.extend(
            Face.from_api_repr(face) for face in results)
    elif feature_type == _REVERSE_TYPES[FeatureTypes.IMAGE_PROPERTIES]:
        detected_objects.append(
            ImagePropertiesAnnotation.from_api_repr(results))
    elif feature_type == _REVERSE_TYPES[FeatureTypes.SAFE_SEARCH_DETECTION]:
        detected_objects.append(SafeSearchAnnotation.from_api_repr(results))
    else:
        for result in results:
            detected_objects.append(EntityAnnotation.from_api_repr(result))
    return detected_objects
