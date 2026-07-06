# Copyright 2026 Google LLC
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

from typing import Any, Callable, Optional, Union

import pandas as pd

import bigframes.dataframe
import bigframes.series


class DeferredBigQueryDataFrame:
    """A proxy object that defers the execution of a BigQuery job until requested."""

    def __init__(
        self,
        execution_func: Callable[
            [],
            Union[
                bigframes.dataframe.DataFrame,
                bigframes.series.Series,
                pd.Series,
                pd.DataFrame,
            ],
        ],
    ):
        self._execution_func = execution_func
        self._result: Optional[
            Union[
                bigframes.dataframe.DataFrame,
                bigframes.series.Series,
                pd.Series,
                pd.DataFrame,
            ]
        ] = None

    @property
    def executed(self) -> bool:
        return self._result is not None

    def execute(
        self,
    ) -> Union[
        bigframes.dataframe.DataFrame,
        bigframes.series.Series,
        pd.Series,
        pd.DataFrame,
    ]:
        """Executes the deferred operation and returns the resulting DataFrame."""
        if self._result is None:
            self._result = self._execution_func()
        return self._result

    def _repr_mimebundle_(self, include=None, exclude=None):
        from bigframes.display.anywidget import TableWidget

        return TableWidget(self)._repr_mimebundle_(include=include, exclude=exclude)  # type: ignore

    def __getattr__(self, name: str) -> Any:
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'. "
            "This is a deferred object. Display it to run the query interactively."
        )
