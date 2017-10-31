# Copyright 2016 Google LLC
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

"""Likelihood constants returned from Vision API."""


from enum import Enum

from google.cloud.vision_v1.proto import image_annotator_pb2


def _get_pb_likelihood(likelihood):
    """Convert protobuf Likelihood integer value to Likelihood enum.

    :type likelihood: int
    :param likelihood: Protobuf integer representing ``Likelihood``.

    :rtype: :class:`~google.cloud.vision.likelihood.Likelihood`
    :returns: Enum ``Likelihood`` converted from protobuf value.
    """
    likelihood_pb = image_annotator_pb2.Likelihood.Name(likelihood)
    return Likelihood[likelihood_pb]


class Likelihood(Enum):
    """A representation of likelihood to give stable results across upgrades.

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#likelihood
    """
    UNKNOWN = 'UNKNOWN'
    VERY_UNLIKELY = 'VERY_UNLIKELY'
    UNLIKELY = 'UNLIKELY'
    POSSIBLE = 'POSSIBLE'
    LIKELY = 'LIKELY'
    VERY_LIKELY = 'VERY_LIKELY'
