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

import pandas as pd

import bigframes.core.indexes as index
import bigframes.series as series


def to_bf_series(obj, default_index: index.Index) -> series.Series:
    if isinstance(obj, series.Series):
        return obj
    if isinstance(obj, pd.Series):
        return series.Series(obj)
    if isinstance(obj, index.Index):
        return series.Series(obj, default_index)
    if isinstance(obj, pd.Index):
        return series.Series(obj, default_index)
    if pd.api.types.is_list_like(obj):
        return series.Series(obj, default_index)
    else:
        raise TypeError(f"Cannot interpret {obj} as series.")


def to_pd_series(obj, default_index: pd.Index) -> pd.Series:
    if isinstance(obj, series.Series):
        return obj.to_pandas()
    if isinstance(obj, pd.Series):
        return obj
    if isinstance(obj, index.Index):
        return pd.Series(obj.to_pandas(), default_index)
    if isinstance(obj, pd.Index):
        return pd.Series(obj, default_index)
    if pd.api.types.is_list_like(obj):
        return pd.Series(obj, default_index)
    else:
        raise TypeError(f"Cannot interpret {obj} as series.")
