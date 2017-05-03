# Copyright 2017, Google Inc. All rights reserved.
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
import collections

from google.gax.utils import protobuf

class VisionHelpers(object):
    """A set of convenience methods to make the Vision GAPIC easier to use.

    This class should be considered abstract; it is used as a superclass
    in a multiple-inheritance construction alongside the applicable GAPIC.
    See the :class:`~google.cloud.vision_v1.ImageAnnotatorClient`.
    """
    def annotate_image(self, request, options=None):
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
            request (:class:`~vision_v1.image_annotator.AnnotateImageRequest`)
            options (:class:`google.gax.CallOptions`): Overrides the default
                settings for this call, e.g, timeout, retries, etc.

        Returns:
            :class:`~vision_v1.image_annotator.AnnotateImageResponse`
        """
        # This method allows features not to be specified, and you get all
        # of them.
        protobuf.setdefault(request, 'features', self._get_all_features())
        return self.batch_annotate_images([request], options=options)[0]

    def _get_all_features(self):
        """Return a list of all features.

        Returns:
            list: A list of all available features.
        """
        answer = []
        for key, value in self.enums.Feature.Type.__dict__.items():
            if key.upper() != key:
                continue
            if not isinstance(value, int) or value == 0:
                continue
            answer.append(value)
        return answer
