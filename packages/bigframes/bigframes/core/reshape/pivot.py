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

from typing import Optional, TYPE_CHECKING

import bigframes_vendored.pandas.core.reshape.pivot as vendored_pandas_pivot
import pandas as pd

import bigframes
from bigframes.core import convert, utils
from bigframes.core.reshape import concat
from bigframes.dataframe import DataFrame

if TYPE_CHECKING:
    import bigframes.session


def crosstab(
    index,
    columns,
    values=None,
    rownames=None,
    colnames=None,
    aggfunc=None,
    *,
    session: Optional[bigframes.session.Session] = None,
) -> DataFrame:
    if _is_list_of_lists(index):
        index = [
            convert.to_bf_series(subindex, default_index=None, session=session)
            for subindex in index
        ]
    else:
        index = [convert.to_bf_series(index, default_index=None, session=session)]
    if _is_list_of_lists(columns):
        columns = [
            convert.to_bf_series(subcol, default_index=None, session=session)
            for subcol in columns
        ]
    else:
        columns = [convert.to_bf_series(columns, default_index=None, session=session)]

    df = concat.concat([*index, *columns], join="inner", axis=1)
    # for uniqueness
    tmp_index_names = [f"_crosstab_index_{i}" for i in range(len(index))]
    tmp_col_names = [f"_crosstab_columns_{i}" for i in range(len(columns))]
    df.columns = pd.Index([*tmp_index_names, *tmp_col_names])

    values = (
        convert.to_bf_series(values, default_index=df.index, session=session)
        if values is not None
        else 0
    )

    df["_crosstab_values"] = values
    pivot_table = df.pivot_table(
        values="_crosstab_values",
        index=tmp_index_names,
        columns=tmp_col_names,
        aggfunc=aggfunc or "count",
        sort=False,
    )
    pivot_table.index.names = rownames or [i.name for i in index]
    pivot_table.columns.names = colnames or [c.name for c in columns]
    if aggfunc is None:
        # TODO: Push this into pivot_table itself
        pivot_table = pivot_table.fillna(0)
    return pivot_table


def _is_list_of_lists(item) -> bool:
    if not utils.is_list_like(item):
        return False
    return all(convert.can_convert_to_series(subitem) for subitem in item)


crosstab.__doc__ = vendored_pandas_pivot.crosstab.__doc__
