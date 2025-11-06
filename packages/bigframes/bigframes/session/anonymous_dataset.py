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

import datetime
import threading
from typing import List, Optional, Sequence
import uuid
import warnings

from google.api_core import retry as api_core_retry
import google.cloud.bigquery as bigquery

from bigframes import constants
import bigframes.core.events
import bigframes.exceptions as bfe
from bigframes.session import temporary_storage
import bigframes.session._io.bigquery as bf_io_bigquery

_TEMP_TABLE_ID_FORMAT = "bqdf{date}_{session_id}_{random_id}"
# UDFs older than this many days are considered stale and will be deleted
# from the anonymous dataset before creating a new UDF.
_UDF_CLEANUP_THRESHOLD_DAYS = 3


class AnonymousDatasetManager(temporary_storage.TemporaryStorageManager):
    """
    Responsible for allocating and cleaning up temporary gbq tables used by a BigFrames session.
    """

    def __init__(
        self,
        bqclient: bigquery.Client,
        location: str,
        session_id: str,
        *,
        kms_key: Optional[str] = None,
        publisher: bigframes.core.events.Publisher,
    ):
        self.bqclient = bqclient
        self._location = location
        self._publisher = publisher

        self.session_id = session_id
        self._table_ids: List[bigquery.TableReference] = []
        self._kms_key = kms_key

        self._dataset_lock = threading.Lock()
        self._datset_ref: Optional[bigquery.DatasetReference] = None

    @property
    def location(self):
        return self._location

    @property
    def dataset(self) -> bigquery.DatasetReference:
        if self._datset_ref is not None:
            return self._datset_ref
        with self._dataset_lock:
            if self._datset_ref is None:
                self._datset_ref = bf_io_bigquery.create_bq_dataset_reference(
                    self.bqclient,
                    location=self._location,
                    publisher=self._publisher,
                )
        return self._datset_ref

    def _default_expiration(self):
        """When should the table expire automatically?"""
        return (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )

    def create_temp_table(
        self, schema: Sequence[bigquery.SchemaField], cluster_cols: Sequence[str] = []
    ) -> bigquery.TableReference:
        """
        Allocates and and creates a table in the anonymous dataset.
        The table will be cleaned up by clean_up_tables.
        """
        expiration = self._default_expiration()
        table = bf_io_bigquery.create_temp_table(
            self.bqclient,
            self.allocate_temp_table(),
            expiration,
            schema=schema,
            cluster_columns=list(cluster_cols),
            kms_key=self._kms_key,
        )
        return bigquery.TableReference.from_string(table)

    def create_temp_view(self, sql: str) -> bigquery.TableReference:
        """
        Allocates and and creates a view in the anonymous dataset.
        The view will be cleaned up by clean_up_tables.
        """
        expiration = self._default_expiration()
        table = bf_io_bigquery.create_temp_view(
            self.bqclient,
            self.allocate_temp_table(),
            expiration=expiration,
            sql=sql,
        )
        return bigquery.TableReference.from_string(table)

    def allocate_temp_table(self) -> bigquery.TableReference:
        """
        Allocates a unique table id, but does not create the table.
        The table will be cleaned up by clean_up_tables.
        """
        table_id = self.generate_unique_resource_id()
        self._table_ids.append(table_id)
        return table_id

    def generate_unique_resource_id(self) -> bigquery.TableReference:
        """Generate a random table ID with BigQuery DataFrames prefix.

        This resource will not be cleaned up by this manager.

        Args:
            skip_cleanup (bool, default False):
                If True, do not add the generated ID to the list of tables
                to clean up when the session is closed.

        Returns:
            google.cloud.bigquery.TableReference:
                Fully qualified table ID of a table that doesn't exist.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        random_id = uuid.uuid4().hex
        table_id = _TEMP_TABLE_ID_FORMAT.format(
            date=now.strftime("%Y%m%d"), session_id=self.session_id, random_id=random_id
        )
        return self.dataset.table(table_id)

    def _cleanup_old_udfs(self):
        """Clean up old UDFs in the anonymous dataset."""
        dataset = self.dataset
        routines = list(self.bqclient.list_routines(dataset))
        cleanup_cutoff_time = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=_UDF_CLEANUP_THRESHOLD_DAYS)

        for routine in routines:
            if (
                routine.created < cleanup_cutoff_time
                and routine._properties["routineType"] == "SCALAR_FUNCTION"
            ):
                try:
                    self.bqclient.delete_routine(
                        routine.reference,
                        not_found_ok=True,
                        retry=api_core_retry.Retry(timeout=0),
                    )
                except Exception as e:
                    msg = bfe.format_message(
                        f"Unable to clean this old UDF '{routine.reference}': {e}"
                    )
                    warnings.warn(msg, category=bfe.CleanupFailedWarning)

    def close(self):
        """Delete tables that were created with this session's session_id."""
        for table_ref in self._table_ids:
            self.bqclient.delete_table(table_ref, not_found_ok=True)
        self._table_ids.clear()

        try:
            # Before closing the session, attempt to clean up any uncollected,
            # old Python UDFs residing in the anonymous dataset. These UDFs
            # accumulate over time and can eventually exceed resource limits.
            # See more from b/450913424.
            self._cleanup_old_udfs()
        except Exception as e:
            # Log a warning on the failure, do not interrupt the workflow.
            msg = bfe.format_message(
                f"Failed to clean up the old Python UDFs before closing the session: {e}"
            )
            warnings.warn(msg, category=bfe.CleanupFailedWarning)
