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
from typing import Any, Optional

import google.cloud.bigquery as bigquery
import ibis.expr.types as ibis_types

import bigframes
import bigframes.formatting_helpers as formatter

if typing.TYPE_CHECKING:
    import bigframes.session


class DeferredScalar:
    """A deferred scalar object."""

    def __init__(self, value: ibis_types.Scalar, session: bigframes.session.Session):
        self._value = value
        self._session = session
        self._query_job: Optional[bigquery.QueryJob] = None

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        """BigQuery job metadata for the most recent query."""
        if self._query_job is None:
            self._query_job = self._compute_dry_run()
        return self._query_job

    def __repr__(self) -> str:
        """Converts a Series to a string."""
        # TODO(swast): Add a timeout here? If the query is taking a long time,
        # maybe we just print the job metadata that we have so far?
        opts = bigframes.options.display
        if opts.repr_mode == "deferred":
            return formatter.repr_query_job(self.query_job)
        else:
            return repr(self.to_pandas())

    def to_pandas(self) -> Any:
        """Executes deferred operations and downloads the resulting scalar."""
        result, query_job = self._session._start_query(self._value.compile())
        self._query_job = query_job
        df = self._session._rows_to_dataframe(result)
        return df.iloc[0, 0]

    def _compute_dry_run(self):
        job_config = bigquery.QueryJobConfig(dry_run=True)
        return self._session._start_query(self._value.compile(), job_config=job_config)


# All public APIs return Any at present
# Later implementation may sometimes return a lazy scalar
Scalar = Any
