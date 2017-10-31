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

"""Representation of Vision API's crop hints."""

from google.cloud.vision.geometry import Bounds


class CropHint(object):
    """Representation of a crop hint returned from the Vision API.

    :type bounds: dict
    :param bounds: Dictionary of boundary information of detected entity.

    :type confidence: float
    :param confidence: Confidence of this being a salient region.

    :type importance_fraction: float
    :param importance_fraction: Fraction of importance of this region.
    """
    def __init__(self, bounds, confidence, importance_fraction):
        self._bounds = bounds
        self._confidence = confidence
        self._importance_fraction = importance_fraction

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct ``CropHint`` from Vision API response.

        :type response: dict
        :param response: Dictionary response from Vision API with entity data.

        :rtype: :class:`~google.cloud.vision.crop_hint.CropHint`
        :returns: Instance of ``CropHint``.
        """
        bounds = Bounds.from_api_repr(response.get('boundingPoly'))
        confidence = response.get('confidence', 0.0)
        importance_fraction = response.get('importanceFraction', 0.0)
        return cls(bounds, confidence, importance_fraction)

    @classmethod
    def from_pb(cls, response):
        """Factory: construct ``CropHint`` from Vision gRPC response.

        :type response: :class:`google.cloud.vision_v1.proto.\
                        image_annotator_pb2.CropHint`
        :param response: gRPC response from Vision API with entity data.

        :rtype: :class:`~google.cloud.vision.crop_hint.CropHint`
        :returns: Instance of ``CropHint``.
        """
        bounds = Bounds.from_pb(response.bounding_poly)
        return cls(bounds, response.confidence, response.importance_fraction)

    @property
    def bounds(self):
        """Bounding polygon of crop hints.

        :rtype: :class:`~google.cloud.vision.geometry.Bounds`
        :returns: Instance of ``Bounds`` with populated vertices.
        """
        return self._bounds

    @property
    def confidence(self):
        """Confidence of this being a salient region.  Range [0, 1].

        :rtype: float
        :returns: float between 0 and 1, inclusive.
        """
        return self._confidence

    @property
    def importance_fraction(self):
        """Fraction of importance of this salient region with respect to the
        original image.

        :rtype: float
        :returns: float
        """
        return self._importance_fraction
