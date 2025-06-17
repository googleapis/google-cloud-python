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

from __future__ import annotations

import typing

from bigframes import dataframe, dtypes, series
from bigframes.core.reshape import api as rs


def describe(
    input: dataframe.DataFrame | series.Series,
    include: None | typing.Literal["all"],
) -> dataframe.DataFrame | series.Series:
    if isinstance(input, series.Series):
        # Convert the series to a dataframe, describe it, and cast the result back to a series.
        return series.Series(describe(input.to_frame(), include)._block)
    elif not isinstance(input, dataframe.DataFrame):
        raise TypeError(f"Unsupported type: {type(input)}")

    if include is None:
        numeric_df = _select_dtypes(
            input,
            dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE
            + dtypes.TEMPORAL_NUMERIC_BIGFRAMES_TYPES,
        )
        if len(numeric_df.columns) == 0:
            # Describe eligible non-numeric columns
            return _describe_non_numeric(input)

        # Otherwise, only describe numeric columns
        return _describe_numeric(input)

    elif include == "all":
        numeric_result = _describe_numeric(input)
        non_numeric_result = _describe_non_numeric(input)

        if len(numeric_result.columns) == 0:
            return non_numeric_result
        elif len(non_numeric_result.columns) == 0:
            return numeric_result
        else:
            # Use reindex after join to preserve the original column order.
            return rs.concat(
                [non_numeric_result, numeric_result], axis=1
            )._reindex_columns(input.columns)

    else:
        raise ValueError(f"Unsupported include type: {include}")


def _describe_numeric(df: dataframe.DataFrame) -> dataframe.DataFrame:
    number_df_result = typing.cast(
        dataframe.DataFrame,
        _select_dtypes(df, dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE).agg(
            [
                "count",
                "mean",
                "std",
                "min",
                "25%",
                "50%",
                "75%",
                "max",
            ]
        ),
    )
    temporal_df_result = typing.cast(
        dataframe.DataFrame,
        _select_dtypes(df, dtypes.TEMPORAL_NUMERIC_BIGFRAMES_TYPES).agg(["count"]),
    )

    if len(number_df_result.columns) == 0:
        return temporal_df_result
    elif len(temporal_df_result.columns) == 0:
        return number_df_result
    else:
        import bigframes.core.reshape.api as rs

        original_columns = _select_dtypes(
            df,
            dtypes.NUMERIC_BIGFRAMES_TYPES_RESTRICTIVE
            + dtypes.TEMPORAL_NUMERIC_BIGFRAMES_TYPES,
        ).columns

        # Use reindex after join to preserve the original column order.
        return rs.concat(
            [number_df_result, temporal_df_result],
            axis=1,
        )._reindex_columns(original_columns)


def _describe_non_numeric(df: dataframe.DataFrame) -> dataframe.DataFrame:
    return typing.cast(
        dataframe.DataFrame,
        _select_dtypes(
            df,
            [
                dtypes.STRING_DTYPE,
                dtypes.BOOL_DTYPE,
                dtypes.BYTES_DTYPE,
                dtypes.TIME_DTYPE,
            ],
        ).agg(["count", "nunique"]),
    )


def _select_dtypes(
    df: dataframe.DataFrame, dtypes: typing.Sequence[dtypes.Dtype]
) -> dataframe.DataFrame:
    """Selects columns without considering inheritance relationships."""
    columns = [
        col_id
        for col_id, dtype in zip(df._block.value_columns, df._block.dtypes)
        if dtype in dtypes
    ]
    return dataframe.DataFrame(df._block.select_columns(columns))
