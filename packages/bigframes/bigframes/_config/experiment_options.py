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

from typing import Optional
import warnings

import bigframes
import bigframes.exceptions as bfe


class ExperimentOptions:
    """
    Encapsulates the configration for experiments
    """

    def __init__(self):
        self._semantic_operators: bool = False
        self._ai_operators: bool = False

    @property
    def semantic_operators(self) -> bool:
        return self._semantic_operators

    @semantic_operators.setter
    def semantic_operators(self, value: bool):
        if value is True:
            msg = bfe.format_message(
                "Semantic operators are deprecated, and will be removed in the future"
            )
            warnings.warn(msg, category=FutureWarning)
        self._semantic_operators = value

    @property
    def ai_operators(self) -> bool:
        return self._ai_operators

    @ai_operators.setter
    def ai_operators(self, value: bool):
        if value is True:
            msg = bfe.format_message(
                "AI operators are still under experiments, and are subject "
                "to change in the future."
            )
            warnings.warn(msg, category=bfe.PreviewWarning)
        self._ai_operators = value

    @property
    def blob(self) -> bool:
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. This flag is no longer needed."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)
        return True

    @blob.setter
    def blob(self, value: bool):
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. This flag is no longer needed."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

    @property
    def blob_display(self) -> bool:
        """Whether to display the blob content in notebook DataFrame preview. Default True."""
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        return bigframes.options.display.blob_display

    @blob_display.setter
    def blob_display(self, value: bool):
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        bigframes.options.display.blob_display = value

    @property
    def blob_display_width(self) -> Optional[int]:
        """Width in pixels that the blob constrained to."""
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display_width."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        return bigframes.options.display.blob_display_width

    @blob_display_width.setter
    def blob_display_width(self, value: Optional[int]):
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display_width."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        bigframes.options.display.blob_display_width = value

    @property
    def blob_display_height(self) -> Optional[int]:
        """Height in pixels that the blob constrained to."""
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display_height."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        return bigframes.options.display.blob_display_height

    @blob_display_height.setter
    def blob_display_height(self, value: Optional[int]):
        msg = bfe.format_message(
            "BigFrames Blob is in preview now. The option has been moved to bigframes.options.display.blob_display_height."
        )
        warnings.warn(msg, category=bfe.ApiDeprecationWarning)

        bigframes.options.display.blob_display_height = value
