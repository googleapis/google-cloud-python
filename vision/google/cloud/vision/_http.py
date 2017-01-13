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

"""HTTP Client for interacting with the Google Cloud Vision API."""

from google.cloud.vision.annotations import Annotations
from google.cloud.vision.feature import Feature


class _HTTPVisionAPI(object):
    """Vision API for interacting with the JSON/HTTP version of Vision

    :type client: :class:`~google.cloud.core.client.Client`
    :param client: Instance of ``Client`` object.
    """

    def __init__(self, client):
        self._client = client
        self._connection = client._connection

    def annotate(self, image, features):
        """Annotate an image to discover it's attributes.

        :type image: :class:`~google.cloud.vision.image.Image`
        :param image: A instance of ``Image``.

        :type features:  list of :class:`~google.cloud.vision.feature.Feature`
        :param features: The type of detection that the Vision API should
                         use to determine image attributes. Pricing is
                         based on the number of Feature Types.

                         See: https://cloud.google.com/vision/docs/pricing
        :rtype: dict
        :returns: List of annotations.
        """
        request = _make_request(image, features)

        data = {'requests': [request]}
        api_response = self._connection.api_request(
            method='POST', path='/images:annotate', data=data)
        images = api_response.get('responses')
        if len(images) == 1:
            return Annotations.from_api_repr(images[0])
        elif len(images) > 1:
            raise NotImplementedError(
                'Multiple image processing is not yet supported.')


def _make_request(image, features):
    """Prepare request object to send to Vision API.

    :type image: :class:`~google.cloud.vision.image.Image`
    :param image: Instance of ``Image``.

    :type features: list of :class:`~google.cloud.vision.feature.Feature`
    :param features: Either a list of ``Feature`` instances or a single
                     instance of ``Feature``.

    :rtype: dict
    :returns: Dictionary prepared to send to the Vision API.
    """
    if isinstance(features, Feature):
        features = [features]

    feature_check = (isinstance(feature, Feature) for feature in features)
    if not any(feature_check):
        raise TypeError('Feature or list of Feature classes are required.')

    return {
        'image': image.as_dict(),
        'features': [feature.as_dict() for feature in features],
    }
