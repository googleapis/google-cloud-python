# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import
import io

from google.api_core import protobuf_helpers as protobuf


class VisionHelpers(object):
    """A set of convenience methods to make the Vision GAPIC easier to use.

    This class should be considered abstract; it is used as a superclass
    in a multiple-inheritance construction alongside the applicable GAPIC.
    See the :class:`~google.cloud.vision_v1.ImageAnnotatorClient`.
    """

    def annotate_image(self, request, retry=None, timeout=None):
        """Run image detection and annotation for an image.

        Example:
            >>> from google.cloud.vision_v1 import ImageAnnotatorClient
            >>> client = ImageAnnotatorClient()
            >>> request = {
            ...     'image': {
            ...         'source': {'image_uri': 'https://foo.com/image.jpg'},
            ...     },
            ... }
            >>> response = client.annotate_image(request)

        Args:
            request (:class:`~.vision_v1.types.AnnotateImageRequest`)
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            :class:`~.vision_v1.types.AnnotateImageResponse` The API response.
        """
        # If the image is a file handler, set the content.
        image = protobuf.get(request, "image")
        if hasattr(image, "read"):
            img_bytes = image.read()
            protobuf.set(request, "image", {})
            protobuf.set(request, "image.content", img_bytes)
            image = protobuf.get(request, "image")

        # If a filename is provided, read the file.
        filename = protobuf.get(image, "source.filename", default=None)
        if filename:
            with io.open(filename, "rb") as img_file:
                protobuf.set(request, "image.content", img_file.read())
                protobuf.set(request, "image.source", None)

        # This method allows features not to be specified, and you get all
        # of them.
        protobuf.setdefault(request, "features", self._get_all_features())
        r = self.batch_annotate_images([request], retry=retry, timeout=timeout)
        return r.responses[0]

    def _get_all_features(self):
        """Return a list of all features.

        Returns:
            list: A list of all available features.
        """
        return [
            {"type": feature} for feature in self.enums.Feature.Type if feature != 0
        ]
