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

"""Safe search class for information returned from annotating an image."""

from google.cloud.vision.likelihood import _get_pb_likelihood
from google.cloud.vision.likelihood import Likelihood


class SafeSearchAnnotation(object):
    """Representation of a SafeSearchAnnotation.

    :type adult_likelihood: :class:`~google.cloud.vision.likelihood.Likelihood`
    :param adult_likelihood: Likelihood that image contains adult material.

    :type spoof_likelihood: :class:`~google.cloud.vision.likelihood.Likelihood`
    :param spoof_likelihood: Likelihood that image is a spoof.

    :type medical_likelihood:
        :class:`~google.cloud.vision.likelihood.Likelihood`
    :param medical_likelihood: Likelihood that image contains medical material.

    :type violence_likelihood:
        :class:`~google.cloud.vision.likelihood.Likelihood`
    :param violence_likelihood: Likelihood that image contains violence.
    """

    def __init__(self, adult_likelihood, spoof_likelihood, medical_likelihood,
                 violence_likelihood):
        self._adult_likelihood = adult_likelihood
        self._spoof_likelihood = spoof_likelihood
        self._medical_likelihood = medical_likelihood
        self._violence_likelihood = violence_likelihood

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct SafeSearchAnnotation from Vision API response.

        :type response: dict
        :param response: Dictionary response from Vision API with safe search
                         data.

        :rtype: :class:`~google.cloud.vision.safe_search.SafeSearchAnnotation`
        :returns: Instance of ``SafeSearchAnnotation``.
        """
        adult_likelihood = Likelihood[response['adult']]
        spoof_likelihood = Likelihood[response['spoof']]
        medical_likelihood = Likelihood[response['medical']]
        violence_likelihood = Likelihood[response['violence']]

        return cls(adult_likelihood, spoof_likelihood, medical_likelihood,
                   violence_likelihood)

    @classmethod
    def from_pb(cls, image):
        """Factory: construct SafeSearchAnnotation from Vision API response.

        :type image: :class:`~google.cloud.vision_v1.proto.\
                      image_annotator_pb2.SafeSearchAnnotation`
        :param image: Protobuf response from Vision API with safe search data.

        :rtype: :class:`~google.cloud.vision.safe_search.SafeSearchAnnotation`
        :returns: Instance of ``SafeSearchAnnotation``.
        """
        values = [image.adult, image.spoof, image.medical, image.violence]
        classifications = map(_get_pb_likelihood, values)
        return cls(*classifications)

    @property
    def adult(self):
        """Represents the adult contents likelihood for the image.

        :rtype: :class:`~google.cloud.vision.likelihood.Likelihood`
        :returns: ``Likelihood`` of the image containing adult content.
        """
        return self._adult_likelihood

    @property
    def spoof(self):
        """The likelihood that an obvious modification was made to the image.

        :rtype: :class:`~google.cloud.vision.likelihood.Likelihood`
        :returns: The ``Likelihood`` that an obvious modification was made to
                  the image's canonical version to make it appear funny or
                  offensive.
        """
        return self._spoof_likelihood

    @property
    def medical(self):
        """Likelihood this is a medical image.

        :rtype: :class:`~google.cloud.vision.likelihood.Likelihood`
        :returns: The ``Likelihood`` that the image is medical in origin.
        """
        return self._medical_likelihood

    @property
    def violence(self):
        """Likeliehood that this image contains violence.

        :rtype: :class:`~google.cloud.vision.likelihood.Likelihood`
        :returns: The ``Likelihood`` that the image contains violence.
        """
        return self._violence_likelihood
