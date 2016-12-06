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

"""Likelihood constants returned from Vision API."""


from enum import Enum


class Likelihood(Enum):
    """A representation of likelihood to give stable results across upgrades.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#likelihood
    """
    UNKNOWN = 'UNKNOWN'
    VERY_UNLIKELY = 'VERY_UNLIKELY'
    UNLIKELY = 'UNLIKELY'
    POSSIBLE = 'POSSIBLE'
    LIKELY = 'LIKELY'
    VERY_LIKELY = 'VERY_LIKELY'
