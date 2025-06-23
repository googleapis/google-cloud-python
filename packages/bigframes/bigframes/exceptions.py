# Copyright 2023 Google LLC
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

"""Public exceptions and warnings used across BigQuery DataFrames."""

import textwrap

# NOTE: This module should not depend on any others in the package.


# Uses UserWarning for backwards compatibility with warning without a category
# set.
class DefaultLocationWarning(UserWarning):
    """No location was specified, so using a default one."""


class UnknownLocationWarning(Warning):
    """The location is set to an unknown value."""


class CleanupFailedWarning(Warning):
    """Bigframes failed to clean up a table resource."""


class DefaultIndexWarning(Warning):
    """Default index may cause unexpected costs."""


class PreviewWarning(Warning):
    """The feature is in preview."""


class NullIndexPreviewWarning(PreviewWarning):
    """Unused. Kept for backwards compatibility.

    Was used when null index feature was in preview.
    """


class NullIndexError(ValueError):
    """Object has no index."""


class OrderingModePartialPreviewWarning(PreviewWarning):
    """Unused. Kept for backwards compatibility.

    Was used when ordering mode 'partial' was in preview.
    """


class OrderRequiredError(ValueError):
    """Operation requires total row ordering to be enabled."""


class QueryComplexityError(RuntimeError):
    """Query plan is too complex to execute."""


class OperationAbortedError(RuntimeError):
    """Operation is aborted."""


class MaximumResultRowsExceeded(RuntimeError):
    """Maximum number of rows in the result was exceeded."""


class TimeTravelDisabledWarning(Warning):
    """A query was reattempted without time travel."""


class AmbiguousWindowWarning(Warning):
    """A query may produce nondeterministic results as the window may be ambiguously ordered."""


class UnknownDataTypeWarning(Warning):
    """Data type is unknown."""


class ApiDeprecationWarning(FutureWarning):
    """The API has been deprecated."""


class BadIndexerKeyWarning(Warning):
    """The indexer key is not used correctly."""


class ObsoleteVersionWarning(Warning):
    """The BigFrames version is too old."""


class FunctionAxisOnePreviewWarning(PreviewWarning):
    """Remote Function and Managed UDF with axis=1 preview."""


def format_message(message: str, fill: bool = True):
    """Formats a warning message with ANSI color codes for the warning color.

    Args:
        message: The warning message string.
        fill: Whether to wrap the message text using `textwrap.fill`.
            Defaults to True.  Set to False to prevent wrapping,
            especially if the message already contains newlines.

    Returns:
        The formatted message string. If `fill` is True, the message will be wrapped
        to fit the terminal width.
    """
    if fill:
        message = textwrap.fill(message)
    return message
