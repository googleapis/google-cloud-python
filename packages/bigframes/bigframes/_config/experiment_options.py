# Copyright 2024 Google LLC
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

import warnings


class ExperimentOptions:
    """
    Encapsulates the configration for experiments
    """

    def __init__(self):
        self._semantic_operators = False

    @property
    def semantic_operators(self) -> bool:
        return self._semantic_operators

    @semantic_operators.setter
    def semantic_operators(self, value: bool):
        if value is True:
            warnings.warn(
                "Semantic operators are still under experiments, and are subject to change in the future."
            )
        self._semantic_operators = value
