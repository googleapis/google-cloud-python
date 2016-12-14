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
from google.cloud.vision.annotations import Annotations
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes


class Image(object):
    """Image representation containing information to be annotate.

    :type content: bytes
    :param content: Byte stream of an image.

    :type filename: str
    :param filename: Filename to image.

    :type source_uri: str
    :param source_uri: Google Cloud Storage URI of image.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Instance of Vision client.
    """

    def __init__(self, client, content=None, filename=None, source_uri=None):
        sources = [source for source in (content, filename, source_uri)
                   if source is not None]
        if len(sources) != 1:
            raise ValueError(
                'Specify exactly one of "content", "filename", or '
                '"source_uri".')

        self.client = client

        if filename is not None:
            with open(filename, 'rb') as file_obj:
                content = file_obj.read()

        if content is not None:
            content = _bytes_to_unicode(b64encode(_to_bytes(content)))

        self._content = content
        self._source = source_uri

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
        """Generic method for detecting annotations.

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
        results = self.client.annotate(self, features)
        return Annotations.from_api_repr(results)

    def detect(self, features):
        """Detect multiple feature types.

        :type features: list of :class:`~google.cloud.vision.feature.Feature`
        :param features: List of the ``Feature`` indication the type of
                         annotation to perform.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        return self._detect_annotation(features)

    def detect_faces(self, limit=10):
        """Detect faces in image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.face.Face`.
        """
        features = [Feature(FeatureTypes.FACE_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.faces

    def detect_labels(self, limit=10):
        """Detect labels that describe objects in an image.

        :type limit: int
        :param limit: The maximum number of labels to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.entity.EntityAnnotation`
        """
        features = [Feature(FeatureTypes.LABEL_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.labels

    def detect_landmarks(self, limit=10):
        """Detect landmarks in an image.

        :type limit: int
        :param limit: The maximum number of landmarks to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LANDMARK_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.landmarks

    def detect_logos(self, limit=10):
        """Detect logos in an image.

        :type limit: int
        :param limit: The maximum number of logos to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LOGO_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.logos

    def detect_properties(self, limit=10):
        """Detect the color properties of an image.

        :type limit: int
        :param limit: The maximum number of image properties to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        """
        features = [Feature(FeatureTypes.IMAGE_PROPERTIES, limit)]
        annotations = self._detect_annotation(features)
        return annotations.properties

    def detect_safe_search(self, limit=10):
        """Retreive safe search properties from an image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.sage.SafeSearchAnnotation`.
        """
        features = [Feature(FeatureTypes.SAFE_SEARCH_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.safe_searches

    def detect_text(self, limit=10):
        """Detect text in an image.

        :type limit: int
        :param limit: The maximum instances of text to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.TEXT_DETECTION, limit)]
        annotations = self._detect_annotation(features)
        return annotations.texts
