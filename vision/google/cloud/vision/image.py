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
from google.cloud.vision.entity import EntityAnnotation
from google.cloud.vision.face import Face
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes
from google.cloud.vision.color import ImagePropertiesAnnotation
from google.cloud.vision.safe import SafeSearchAnnotation


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
            self._content = b64encode(_to_bytes(content))

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

    def _detect_annotation(self, feature):
        """Generic method for detecting a single annotation.

        :type feature: :class:`~google.cloud.vision.feature.Feature`
        :param feature: The ``Feature`` indication the type of annotation to
                        perform.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        reverse_types = {
            'LABEL_DETECTION': 'labelAnnotations',
            'LANDMARK_DETECTION': 'landmarkAnnotations',
            'LOGO_DETECTION': 'logoAnnotations',
            'TEXT_DETECTION': 'textAnnotations',
        }
        detected_objects = []
        result = self.client.annotate(self, [feature])
        for response in result[reverse_types[feature.feature_type]]:
            detected_object = EntityAnnotation.from_api_repr(response)
            detected_objects.append(detected_object)
        return detected_objects

    def detect_faces(self, limit=10):
        """Detect faces in image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.face.Face`.
        """
        faces = []
        face_detection_feature = Feature(FeatureTypes.FACE_DETECTION, limit)
        result = self.client.annotate(self, [face_detection_feature])
        for face_response in result['faceAnnotations']:
            face = Face.from_api_repr(face_response)
            faces.append(face)

        return faces

    def detect_labels(self, limit=10):
        """Detect labels that describe objects in an image.

        :type limit: int
        :param limit: The maximum number of labels to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.entity.EntityAnnotation`
        """
        feature = Feature(FeatureTypes.LABEL_DETECTION, limit)
        return self._detect_annotation(feature)

    def detect_landmarks(self, limit=10):
        """Detect landmarks in an image.

        :type limit: int
        :param limit: The maximum number of landmarks to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        feature = Feature(FeatureTypes.LANDMARK_DETECTION, limit)
        return self._detect_annotation(feature)

    def detect_logos(self, limit=10):
        """Detect logos in an image.

        :type limit: int
        :param limit: The maximum number of logos to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        feature = Feature(FeatureTypes.LOGO_DETECTION, limit)
        return self._detect_annotation(feature)

    def detect_properties(self, limit=10):
        """Detect the color properties of an image.

        :type limit: int
        :param limit: The maximum number of image properties to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        """
        feature = Feature(FeatureTypes.IMAGE_PROPERTIES, limit)
        result = self.client.annotate(self, [feature])
        response = result['imagePropertiesAnnotation']
        return ImagePropertiesAnnotation.from_api_repr(response)

    def detect_safe_search(self, limit=10):
        """Retreive safe search properties from an image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.sage.SafeSearchAnnotation`.
        """
        safe_detection_feature = Feature(FeatureTypes.SAFE_SEARCH_DETECTION,
                                         limit)
        result = self.client.annotate(self, [safe_detection_feature])
        safe_search_response = result['safeSearchAnnotation']
        return SafeSearchAnnotation.from_api_repr(safe_search_response)

    def detect_text(self, limit=10):
        """Detect text in an image.

        :type limit: int
        :param limit: The maximum instances of text to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        feature = Feature(FeatureTypes.TEXT_DETECTION, limit)
        return self._detect_annotation(feature)
