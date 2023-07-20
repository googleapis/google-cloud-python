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

import typing
from typing import Any

import ibis.expr.types as ibis_types

if typing.TYPE_CHECKING:
    import bigframes.session


class DeferredScalar:
    """A deferred scalar object."""

    def __init__(self, value: ibis_types.Scalar, session: bigframes.session.Session):
        self._value = value
        self._session = session

    def __repr__(self) -> str:
        """Converts a Series to a string."""
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        return repr(self.compute())

    def compute(self) -> Any:
        """Executes deferred operations and downloads the resulting scalar."""
        result, _ = self._session._start_query(self._value.compile())
        df = self._session._rows_to_dataframe(result)
        return df.iloc[0, 0]


# All public APIs return Any at present
# Later implementation may sometimes return a lazy scalar
Scalar = Any
