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
from __future__ import annotations

from typing import Optional

import pandas as pd

from bigframes import dataframe, series, session
from bigframes.core import global_session, indexes


def can_convert_to_series(obj) -> bool:
    if isinstance(obj, series.Series):
        return True
    if isinstance(obj, pd.Series):
        return True
    if isinstance(obj, indexes.Index):
        return True
    if isinstance(obj, pd.Index):
        return True
    if pd.api.types.is_list_like(obj):
        return True

    return False


def to_bf_series(
    obj,
    default_index: Optional[indexes.Index],
    session: Optional[session.Session] = None,
) -> series.Series:
    """
    Convert a an object to a bigframes series

    Args:
        obj (list-like or Series):
            Object to convert to bigframes Series
        default_index (list-like or Index or None):
            Index to use if obj has no index

    Returns
        bigframes.pandas.Series
    """
    if isinstance(obj, series.Series):
        return obj.copy()

    if session is None:
        session = global_session.get_global_session()

    if isinstance(obj, pd.Series):
        return series.Series(obj, session=session)
    if isinstance(obj, indexes.Index):
        return series.Series(obj, default_index, session=session)
    if isinstance(obj, pd.Index):
        return series.Series(obj, default_index, session=session)
    if pd.api.types.is_dict_like(obj):
        return series.Series(obj, session=session)
    if pd.api.types.is_list_like(obj):
        return series.Series(obj, default_index, session=session)

    raise TypeError(f"Cannot interpret {obj} as series.")


def to_pd_series(obj, default_index: pd.Index) -> pd.Series:
    """
    Convert a an object to a pandas series

    Args:
        obj (list-like or Series):
            Object to convert to pandas Series
        default_index (list-like or Index or None):
            Index to use if obj has no index

    Returns
        pandas.Series
    """
    if isinstance(obj, series.Series):
        return obj.to_pandas()
    if isinstance(obj, pd.Series):
        return obj
    if isinstance(obj, indexes.Index):
        return pd.Series(obj.to_pandas(), default_index)
    if isinstance(obj, pd.Index):
        return pd.Series(obj, default_index)
    if pd.api.types.is_dict_like(obj):
        return pd.Series(obj)
    if pd.api.types.is_list_like(obj):
        return pd.Series(obj, default_index)

    raise TypeError(f"Cannot interpret {obj} as series.")


def can_convert_to_dataframe(obj) -> bool:
    if can_convert_to_series(obj):
        return True

    if isinstance(obj, dataframe.DataFrame) or isinstance(obj, pd.DataFrame):
        return True

    return False


def to_bf_dataframe(
    obj,
    default_index: Optional[indexes.Index],
    session: Optional[session.Session] = None,
) -> dataframe.DataFrame:
    if isinstance(obj, dataframe.DataFrame):
        return obj.copy()

    if isinstance(obj, pd.DataFrame):
        if session is None:
            session = global_session.get_global_session()
        return dataframe.DataFrame(obj, session=session)

    if can_convert_to_series(obj):
        return to_bf_series(obj, default_index, session).to_frame()

    raise TypeError(f"Cannot interpret {obj} as a dataframe.")
