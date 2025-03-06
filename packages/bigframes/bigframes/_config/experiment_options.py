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

import bigframes.exceptions as bfe


class ExperimentOptions:
    """
    Encapsulates the configration for experiments
    """

    def __init__(self):
        self._semantic_operators: bool = False
        self._blob: bool = False
        self._udf: bool = False

    @property
    def semantic_operators(self) -> bool:
        return self._semantic_operators

    @semantic_operators.setter
    def semantic_operators(self, value: bool):
        if value is True:
            msg = bfe.format_message(
                "Semantic operators are still under experiments, and are subject "
                "to change in the future."
            )
            warnings.warn(msg, category=bfe.PreviewWarning)
        self._semantic_operators = value

    @property
    def blob(self) -> bool:
        return self._blob

    @blob.setter
    def blob(self, value: bool):
        if value is True:
            msg = bfe.format_message(
                "BigFrames Blob is still under experiments. It may not work and "
                "subject to change in the future."
            )
            warnings.warn(msg, category=bfe.PreviewWarning)
        self._blob = value

    @property
    def udf(self) -> bool:
        return self._udf

    @udf.setter
    def udf(self, value: bool):
        if value is True:
            msg = bfe.format_message(
                "BigFrames managed function (udf) is still under experiments. "
                "It may not work and subject to change in the future."
            )
            warnings.warn(msg, category=bfe.PreviewWarning)
        self._udf = value
