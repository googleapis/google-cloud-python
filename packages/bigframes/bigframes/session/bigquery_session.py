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

import datetime
import logging
import threading
from typing import Callable, Optional, Sequence
import uuid

# TODO: Non-ibis implementation
import bigframes_vendored.ibis.backends.bigquery.datatypes as ibis_bq
import google.cloud.bigquery as bigquery

from bigframes.core.compile import googlesql
from bigframes.session import temporary_storage

KEEPALIVE_QUERY_TIMEOUT_SECONDS = 5.0

KEEPALIVE_FREQUENCY = datetime.timedelta(hours=6)


logger = logging.getLogger(__name__)


class SessionResourceManager(temporary_storage.TemporaryStorageManager):
    """
    Responsible for allocating and cleaning up temporary gbq tables used by a BigFrames session.
    """

    def __init__(self, bqclient: bigquery.Client, location: str):
        self.bqclient = bqclient
        self._location = location
        self._session_id: Optional[str] = None
        self._sessiondaemon: Optional[RecurringTaskDaemon] = None
        self._session_lock = threading.RLock()

    @property
    def location(self):
        return self._location

    def create_temp_table(
        self, schema: Sequence[bigquery.SchemaField], cluster_cols: Sequence[str] = []
    ) -> bigquery.TableReference:
        """Create a temporary session table. Session is an exclusive resource, so throughput is limited"""
        # Can't set a table in _SESSION as destination via query job API, so we
        # run DDL, instead.
        with self._session_lock:
            table_ref = bigquery.TableReference(
                bigquery.DatasetReference(self.bqclient.project, "_SESSION"),
                f"bqdf_{uuid.uuid4()}",
            )
            job_config = bigquery.QueryJobConfig(
                connection_properties=[
                    bigquery.ConnectionProperty("session_id", self._get_session_id())
                ]
            )

            ibis_schema = ibis_bq.BigQuerySchema.to_ibis(list(schema))

            fields = [
                f"{googlesql.identifier(name)} {ibis_bq.BigQueryType.from_ibis(ibis_type)}"
                for name, ibis_type in ibis_schema.fields.items()
            ]
            fields_string = ",".join(fields)

            cluster_string = ""
            if cluster_cols:
                cluster_cols_sql = ", ".join(
                    f"{googlesql.identifier(cluster_col)}"
                    for cluster_col in cluster_cols
                )
                cluster_string = f"\nCLUSTER BY {cluster_cols_sql}"

            ddl = f"CREATE TEMP TABLE `_SESSION`.{googlesql.identifier(table_ref.table_id)} ({fields_string}){cluster_string}"

            job = self.bqclient.query(
                ddl, job_config=job_config, location=self.location
            )
            job.result()
            # return the fully qualified table, so it can be used outside of the session
            return job.destination

    def close(self):
        if self._sessiondaemon is not None:
            self._sessiondaemon.stop()

        if self._session_id is not None and self.bqclient is not None:
            self.bqclient.query_and_wait(
                f"CALL BQ.ABORT_SESSION('{self._session_id}')",
                location=self.location,
            )

    def _get_session_id(self) -> str:
        if self._session_id:
            return self._session_id
        with self._session_lock:
            if self._session_id is None:
                job_config = bigquery.QueryJobConfig(create_session=True)
                # Make sure the session is a new one, not one associated with another query.
                job_config.use_query_cache = False
                query_job = self.bqclient.query(
                    "SELECT 1", job_config=job_config, location=self.location
                )
                query_job.result()  # blocks until finished
                assert query_job.session_info is not None
                assert query_job.session_info.session_id is not None
                self._session_id = query_job.session_info.session_id
                self._sessiondaemon = RecurringTaskDaemon(
                    task=self._keep_session_alive, frequency=KEEPALIVE_FREQUENCY
                )
                self._sessiondaemon.start()
                return query_job.session_info.session_id
            else:
                return self._session_id

    def _keep_session_alive(self):
        # bq sessions will default expire after 24 hours of disuse, but if queried, this is renewed to a maximum of 7 days
        with self._session_lock:
            job_config = bigquery.QueryJobConfig(
                connection_properties=[
                    bigquery.ConnectionProperty("session_id", self._get_session_id())
                ]
            )
            try:
                self.bqclient.query_and_wait(
                    "SELECT 1",
                    location=self.location,
                    job_config=job_config,
                    wait_timeout=KEEPALIVE_QUERY_TIMEOUT_SECONDS,
                )
            except Exception as e:
                logging.warning("BigQuery session keep-alive query errored : %s", e)


class RecurringTaskDaemon:
    def __init__(self, task: Callable[[], None], frequency: datetime.timedelta):
        self._stop_event = threading.Event()
        self._frequency = frequency
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._task = task

    def start(self):
        """Start the daemon. Cannot be restarted once stopped."""
        if self._stop_event.is_set():
            raise RuntimeError("Cannot restart daemon thread.")
        self._thread.start()

    def _run_loop(self):
        while True:
            self._stop_event.wait(self._frequency.total_seconds())
            if self._stop_event.is_set():
                return
            try:
                self._task()
            except Exception as e:
                logging.warning("RecurringTaskDaemon task errorred: %s", e)

    def stop(self, timeout_seconds: Optional[float] = None):
        """Stop and cleanup the daemon."""
        if self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=timeout_seconds)
