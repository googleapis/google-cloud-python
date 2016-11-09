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

"""Image represented by either a URI or byte stream."""


from base64 import b64encode

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode
from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.face import Face
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes
from google.cloud.vision.color import ImagePropertiesAnnotation
from google.cloud.vision.safe import SafeSearchAnnotation


_FACE_DETECTION = 'FACE_DETECTION'
_IMAGE_PROPERTIES = 'IMAGE_PROPERTIES'
_LABEL_DETECTION = 'LABEL_DETECTION'
_LANDMARK_DETECTION = 'LANDMARK_DETECTION'
_LOGO_DETECTION = 'LOGO_DETECTION'
_SAFE_SEARCH_DETECTION = 'SAFE_SEARCH_DETECTION'
_TEXT_DETECTION = 'TEXT_DETECTION'

_REVERSE_TYPES = {
    _FACE_DETECTION: 'faceAnnotations',
    _IMAGE_PROPERTIES: 'imagePropertiesAnnotation',
    _LABEL_DETECTION: 'labelAnnotations',
    _LANDMARK_DETECTION: 'landmarkAnnotations',
    _LOGO_DETECTION: 'logoAnnotations',
    _SAFE_SEARCH_DETECTION: 'safeSearchAnnotation',
    _TEXT_DETECTION: 'textAnnotations',
}


class Image(object):
    """Image representation containing information to be annotate.

    :type content: bytes
    :param content: Byte stream of an image.

    :type source_uri: str
    :param source_uri: Google Cloud Storage URI of image.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Instance of Vision client.
    """

    def __init__(self, client, content=None, source_uri=None):
        self.client = client
        self._content = None
        self._source = None

        if source_uri:
            self._source = source_uri
        else:
            self._content = _bytes_to_unicode(b64encode(_to_bytes(content)))

    def as_dict(self):
        """Generate dictionary structure for request.

        :rtype: dict
        :returns: Dictionary with source information for image.
        """
        if self.content:
            return {
                'content': self.content
            }
        else:
            return {
                'source': {
                    'gcs_image_uri': self.source
                }
            }

    @property
    def content(self):
        """Base64 encoded image content.

        :rtype: str
        :returns: Base64 encoded image bytes.
        """
        return self._content

    @property
    def source(self):
        """Google Cloud Storage URI.

        :rtype: str
        :returns: String of Google Cloud Storage URI.
        """
        return self._source

    def _detect_annotation(self, features):
        """Generic method for detecting a single annotation.

        :type features: list
        :param features: List of :class:`~google.cloud.vision.feature.Feature`
                         indicating the type of annotations to perform.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`,
                  :class:`~google.cloud.vision.face.Face`,
                  :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`,
                  :class:`~google.cloud.vision.sage.SafeSearchAnnotation`,
        """
        detected_objects = []
        results = self.client.annotate(self, features)
        for feature in features:
            detected_objects.extend(
                _entity_from_response_type(feature.feature_type, results))
        return detected_objects

    def detect_faces(self, limit=10):
        """Detect faces in image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.face.Face`.
        """
        features = [Feature(FeatureTypes.FACE_DETECTION, limit)]
        return self._detect_annotation(features)

    def detect_labels(self, limit=10):
        """Detect labels that describe objects in an image.

        :type limit: int
        :param limit: The maximum number of labels to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.entity.EntityAnnotation`
        """
        features = [Feature(FeatureTypes.LABEL_DETECTION, limit)]
        return self._detect_annotation(features)

    def detect_landmarks(self, limit=10):
        """Detect landmarks in an image.

        :type limit: int
        :param limit: The maximum number of landmarks to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LANDMARK_DETECTION, limit)]
        return self._detect_annotation(features)

    def detect_logos(self, limit=10):
        """Detect logos in an image.

        :type limit: int
        :param limit: The maximum number of logos to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LOGO_DETECTION, limit)]
        return self._detect_annotation(features)

    def detect_properties(self, limit=10):
        """Detect the color properties of an image.

        :type limit: int
        :param limit: The maximum number of image properties to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        """
        features = [Feature(FeatureTypes.IMAGE_PROPERTIES, limit)]
        return self._detect_annotation(features)

    def detect_safe_search(self, limit=10):
        """Retreive safe search properties from an image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.sage.SafeSearchAnnotation`.
        """
        features = [Feature(FeatureTypes.SAFE_SEARCH_DETECTION, limit)]
        return self._detect_annotation(features)

    def detect_text(self, limit=10):
        """Detect text in an image.

        :type limit: int
        :param limit: The maximum instances of text to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.TEXT_DETECTION, limit)]
        return self._detect_annotation(features)


def _entity_from_response_type(feature_type, results):
    """Convert a JSON result to an entity type based on the feature."""

    detected_objects = []
    feature_key = _REVERSE_TYPES[feature_type]

    if feature_type == _FACE_DETECTION:
        detected_objects.extend(
            Face.from_api_repr(face) for face in results[feature_key])
    elif feature_type == _IMAGE_PROPERTIES:
        detected_objects.append(
            ImagePropertiesAnnotation.from_api_repr(results[feature_key]))
    elif feature_type == _SAFE_SEARCH_DETECTION:
        result = results[feature_key]
        detected_objects.append(SafeSearchAnnotation.from_api_repr(result))
    else:
        for result in results[feature_key]:
            detected_objects.append(EntityAnnotation.from_api_repr(result))
    return detected_objects
