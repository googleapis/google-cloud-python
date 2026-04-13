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

"""Plaintext display representations."""

from __future__ import annotations

import typing

import pandas
import pandas.io.formats

from bigframes._config import display_options, options

if typing.TYPE_CHECKING:
    import pandas as pd


def create_text_representation(
    pandas_df: pd.DataFrame,
    total_rows: typing.Optional[int],
    is_series: bool,
    has_index: bool = True,
    column_count: int = 0,
) -> str:
    """Create a text representation of the DataFrame or Series.

    Args:
        pandas_df:
            The pandas DataFrame containing the data to represent.
        total_rows:
            The total number of rows in the original BigFrames object.
        is_series:
            Whether the object being represented is a Series.
        has_index:
            Whether the object has an index to display.
        column_count:
            The total number of columns in the original BigFrames object.
            Only used for DataFrames.

    Returns:
        A plaintext string representation.
    """
    opts = options.display

    if is_series:
        with display_options.pandas_repr(opts):
            pd_series = pandas_df.iloc[:, 0]
            if not has_index:
                repr_string = pd_series.to_string(
                    length=False, index=False, name=True, dtype=True
                )
            else:
                repr_string = pd_series.to_string(length=False, name=True, dtype=True)

        lines = repr_string.split("\n")
        is_truncated = total_rows is not None and total_rows > len(pandas_df)

        if is_truncated:
            lines.append("...")
            lines.append("")  # Add empty line for spacing only if truncated
            lines.append(f"[{total_rows} rows]")

        return "\n".join(lines)

    else:
        # DataFrame
        with display_options.pandas_repr(opts):
            # safe to mutate this, this dict is owned by this code, and does not affect global config
            to_string_kwargs = (
                pandas.io.formats.format.get_dataframe_repr_params()  # type: ignore
            )
            if not has_index:
                to_string_kwargs.update({"index": False})

            # We add our own dimensions string, so don't want pandas to.
            to_string_kwargs.update({"show_dimensions": False})
            repr_string = pandas_df.to_string(**to_string_kwargs)

        lines = repr_string.split("\n")
        is_truncated = total_rows is not None and total_rows > len(pandas_df)

        if is_truncated:
            lines.append("...")
            lines.append("")  # Add empty line for spacing only if truncated
            lines.append(f"[{total_rows or '?'} rows x {column_count} columns]")
        else:
            # For non-truncated DataFrames, we still need to add dimensions if show_dimensions was False
            lines.append("")
            lines.append(f"[{total_rows or '?'} rows x {column_count} columns]")
        return "\n".join(lines)
