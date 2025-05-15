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
from typing import List, Optional, Sequence
import uuid

import google.cloud.bigquery as bigquery

from bigframes import constants
from bigframes.session import temporary_storage
import bigframes.session._io.bigquery as bf_io_bigquery

_TEMP_TABLE_ID_FORMAT = "bqdf{date}_{session_id}_{random_id}"


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
        kms_key: Optional[str] = None
    ):
        self.bqclient = bqclient
        self._location = location
        self.dataset = bf_io_bigquery.create_bq_dataset_reference(
            self.bqclient,
            location=self._location,
        )

        self.session_id = session_id
        self._table_ids: List[bigquery.TableReference] = []
        self._kms_key = kms_key

    @property
    def location(self):
        return self._location

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

    def close(self):
        """Delete tables that were created with this session's session_id."""
        for table_ref in self._table_ids:
            self.bqclient.delete_table(table_ref, not_found_ok=True)
        self._table_ids.clear()
