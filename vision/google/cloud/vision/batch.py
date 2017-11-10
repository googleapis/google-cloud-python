# Copyright 2017 Google LLC
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

"""Batch multiple images into one request."""


class Batch(object):
    """Batch of images to process.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Vision client.
    """
    def __init__(self, client):
        self._client = client
        self._images = []

    def add_image(self, image, features):
        """Add image to batch request.

        :type image: :class:`~google.cloud.vision.image.Image`
        :param image: Istance of ``Image``.

        :type features: list
        :param features: List of :class:`~google.cloud.vision.feature.Feature`.
        """
        self._images.append((image, features))

    @property
    def images(self):
        """List of images to process.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.image.Image`.
        """
        return self._images

    def detect(self):
        """Perform batch detection of images.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.annotations.Annotations`.
        """
        results = self._client._vision_api.annotate(self.images)
        self._images = []
        return results
