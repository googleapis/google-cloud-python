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

import bigframes.constants as constants
import bigframes.session._io.bigquery as bf_io_bigquery

_TEMP_TABLE_ID_FORMAT = "bqdf{date}_{session_id}_{random_id}"


class TemporaryGbqStorageManager:
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
        self.location = location
        self.dataset = bf_io_bigquery.create_bq_dataset_reference(
            self.bqclient,
            location=self.location,
            api_name="session-__init__",
        )

        self.session_id = session_id
        self._table_ids: List[str] = []
        self._kms_key = kms_key

    def create_temp_table(
        self, schema: Sequence[bigquery.SchemaField], cluster_cols: Sequence[str]
    ) -> bigquery.TableReference:
        # Can't set a table in _SESSION as destination via query job API, so we
        # run DDL, instead.
        expiration = (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )
        table = bf_io_bigquery.create_temp_table(
            self.bqclient,
            self._random_table(),
            expiration,
            schema=schema,
            cluster_columns=list(cluster_cols),
            kms_key=self._kms_key,
        )
        return bigquery.TableReference.from_string(table)

    def _random_table(self, skip_cleanup: bool = False) -> bigquery.TableReference:
        """Generate a random table ID with BigQuery DataFrames prefix.

        The generated ID will be stored and checked for deletion when the
        session is closed, unless skip_cleanup is True.

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
        if not skip_cleanup:
            self._table_ids.append(table_id)
        return self.dataset.table(table_id)

    def clean_up_tables(self):
        """Delete tables that were created with this session's session_id."""
        client = self.bqclient
        project_id = self.dataset.project
        dataset_id = self.dataset.dataset_id

        for table_id in self._table_ids:
            full_id = ".".join([project_id, dataset_id, table_id])
            client.delete_table(full_id, not_found_ok=True)
