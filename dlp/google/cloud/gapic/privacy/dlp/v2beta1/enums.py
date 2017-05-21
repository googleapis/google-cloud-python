# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""


class Likelihood(object):
    """
    Categorization of results based on how likely they are to represent a match,
    based on the number of elements they contain which imply a match.

    Attributes:
      LIKELIHOOD_UNSPECIFIED (int): Default value; information with all likelihoods will be included.
      VERY_UNLIKELY (int): Few matching elements.
      UNLIKELY (int)
      POSSIBLE (int): Some matching elements.
      LIKELY (int)
      VERY_LIKELY (int): Many matching elements.
    """
    LIKELIHOOD_UNSPECIFIED = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5
