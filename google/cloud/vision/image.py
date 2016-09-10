# Copyright 2016 Google Inc. All rights reserved.
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

    def detect_logos(self, limit=10):
        """Detect logos in an image.

        :type limit: int
        :param limit: The maximum number of logos to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        logos = []
        logo_detection_feature = Feature(FeatureTypes.LOGO_DETECTION, limit)
        result = self.client.annotate(self, [logo_detection_feature])
        for logo_response in result['logoAnnotations']:
            logo = EntityAnnotation.from_api_repr(logo_response)
            logos.append(logo)

        return logos
