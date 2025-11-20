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

from __future__ import annotations

import inspect
import sys

from bigframes.core import log_adapter
import bigframes.core.global_session as global_session
from bigframes.pandas.io.api import _set_default_session_location_if_possible
import bigframes.session
import bigframes.streaming.dataframe as streaming_dataframe


def read_gbq_table(table: str) -> streaming_dataframe.StreamingDataFrame:
    _set_default_session_location_if_possible(table)
    return global_session.with_default_session(
        bigframes.session.Session.read_gbq_table_streaming, table
    )


read_gbq_table.__doc__ = inspect.getdoc(
    bigframes.session.Session.read_gbq_table_streaming
)

StreamingDataFrame = streaming_dataframe.StreamingDataFrame

_module = sys.modules[__name__]
_functions = [read_gbq_table]

for _function in _functions:
    _decorated_object = log_adapter.method_logger(_function, custom_base_name="pandas")
    setattr(_module, _function.__name__, _decorated_object)

__all__ = ["read_gbq_table", "StreamingDataFrame"]
