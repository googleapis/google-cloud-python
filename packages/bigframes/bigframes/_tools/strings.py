# Copyright 2025 Google LLC
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

"""Helper methods for processing strings with minimal dependencies.

Please keep the dependencies used in this subpackage to a minimum to avoid the
risk of circular dependencies.
"""

import numpy


def levenshtein_distance(left: str, right: str) -> int:
    """Compute the edit distance between two strings.

    This is the minumum number of substitutions, insertions, deletions
    to get from left string to right string. See:
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    # TODO(tswast): accelerate with numba (if available) if we end up using this
    # function in contexts other than when raising an exception or there are too
    # many values to compare even in that context.

    distances0 = numpy.zeros(len(right) + 1)
    distances1 = numpy.zeros(len(right) + 1)

    # Maximum distance is to drop all characters and then add the other string.
    distances0[:] = range(len(right) + 1)

    for left_index in range(len(left)):
        # Calculate distance from distances0 to distances1.

        # Edit distance is to delete (i + 1) chars from left to match empty right
        distances1[0] = left_index + 1
        # "ab"
        for right_index in range(len(right)):
            left_char = left[left_index]
            right_char = right[right_index]

            deletion_cost = distances0[right_index + 1] + 1
            insertion_cost = distances1[right_index] + 1
            if left_char == right_char:
                substitution_cost = distances0[right_index]
            else:
                substitution_cost = distances0[right_index] + 1

            distances1[right_index + 1] = min(
                deletion_cost, insertion_cost, substitution_cost
            )

        temp = distances0
        distances0 = distances1
        distances1 = temp

    return distances0[len(right)]
