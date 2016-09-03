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

"""Client for interacting with the Google Cloud Vision API."""


from gcloud.client import JSONClient
from gcloud.vision.connection import Connection
from gcloud.vision.feature import Feature
from gcloud.vision.image import Image


class VisionRequest(object):
    """Request container with image and features information to annotate.

    :type features: list of :class:`gcoud.vision.feature.Feature`.
    :param features: The features that dictate which annotations to run.

    :type image: bytes
    :param image: Either Google Cloud Storage URI or raw byte stream of image.
    """
    def __init__(self, image, features):
        self._features = []
        self._image = image

        if isinstance(features, list):
            self._features.extend(features)
        elif isinstance(features, Feature):
            self._features.append(features)
        else:
            raise TypeError('Feature or list of Feature classes are required.')

    def as_dict(self):
        """Dictionary representation of Image."""
        return {
            'image': self.image.as_dict(),
            'features': [feature.as_dict() for feature in self.features]
        }

    @property
    def features(self):
        """List of Feature objects."""
        return self._features

    @property
    def image(self):
        """Image object containing image content."""
        return self._image


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def annotate(self, image, features):
        """Annotate an image to discover it's attributes.

        :type image: str
        :param image: A string which can be a URL, a Google Cloud Storage path,
                      or a byte stream of the image.

        :type features:  list of :class:`gcloud.vision.feature.Feature`
        :param features: The type of detection that the Vision API should
                         use to determine image attributes. Pricing is
                         based on the number of Feature Types.

                         See: https://cloud.google.com/vision/docs/pricing
        :rtype: dict
        :returns: List of annotations.
        """
        img = Image(image, self)
        request = VisionRequest(img, features)

        data = {'requests': [request.as_dict()]}
        response = self.connection.api_request(method='POST',
                                               path='/images:annotate',
                                               data=data)

        return response['responses'][0]
