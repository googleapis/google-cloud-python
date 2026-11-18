# Copyright 2024, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Provides helper logic used across samples
"""

import inspect

from google.api_core import exceptions
from google.api_core.retry import Retry, if_exception_type

from google.cloud import bigtable, bigtable_admin_v2
from google.cloud.bigtable.column_family import ColumnFamily
from google.cloud.bigtable.data import BigtableDataClient, ReadRowsQuery
from google.cloud.bigtable_admin_v2.types import ColumnFamily as ColumnFamily_pb

delete_retry = Retry(
    if_exception_type(exceptions.TooManyRequests, exceptions.ServiceUnavailable)
)


class create_table_cm:
    """
    Create a new table using a context manager, to ensure that table.delete() is called to clean up
    the table, even if an exception is thrown
    """

    def __init__(self, *args, verbose=True, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._verbose = verbose

    def __enter__(self):
        self._table = create_table(*self._args, **self._kwargs)
        if self._verbose:
            print(f"created table: {self._table.table_id}")
        return self._table

    def __exit__(self, *args):
        admin_client = bigtable_admin_v2.BigtableTableAdminClient()
        try:
            if self._verbose:
                print(f"deleting table: {self._table.table_id}")
            delete_retry(admin_client.delete_table)(name=self._table.name)
        except exceptions.NotFound:
            if self._verbose:
                print(f"table {self._table.table_id} not found")


def create_table(project, instance_id, table_id, column_families={}):
    """
    Creates a new table, and blocks until it reaches a ready state
    """
    admin_client = bigtable_admin_v2.BigtableTableAdminClient()
    instance_path = admin_client.instance_path(project, instance_id)
    table_path = admin_client.table_path(project, instance_id, table_id)

    try:
        admin_client.delete_table(name=table_path)
    except exceptions.NotFound:
        pass

    client = bigtable.Client(project=project, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    # convert column families to pb if needed
    pb_families = {
        id: ColumnFamily(id, table, rule).to_pb()
        if not isinstance(rule, ColumnFamily_pb)
        else rule
        for (id, rule) in column_families.items()
    }

    admin_client.create_table(
        request={
            "parent": instance_path,
            "table_id": table_id,
            "table": {"column_families": pb_families},
        }
    )

    wait_for_table(table_path)

    return table


@Retry(
    predicate=if_exception_type(
        exceptions.PreconditionFailed,
        exceptions.FailedPrecondition,
        exceptions.NotFound,
    ),
    timeout=120,
)
def wait_for_table(table):
    """
    raises an exception if the table does not exist or is not ready to use

    Because this method is wrapped with an api_core.Retry decorator, it will
    retry with backoff if the table is not ready
    """
    if hasattr(table, "exists"):
        if not table.exists():
            raise exceptions.NotFound("Table does not exist yet")
        return

    # Data-client Table / TableAsync instances and raw table_path strings (e.g.
    # from create_table) do not expose .exists(), so verify via admin + data plane.
    table_path = table.table_name if hasattr(table, "table_name") else str(table)
    admin_client = bigtable_admin_v2.BigtableTableAdminClient()
    admin_client.get_table(
        request={
            "name": table_path,
            "view": bigtable_admin_v2.Table.View.NAME_ONLY,
        }
    )

    # Probe the data plane as well: get_table() can succeed while mutations
    # still return FailedPrecondition ("table ... is still being created").
    if hasattr(table, "read_rows") and not inspect.iscoroutinefunction(table.read_rows):
        table.read_rows(ReadRowsQuery(limit=1))
        return

    parts = table_path.split("/")
    if len(parts) == 6 and parts[0] == "projects":
        with BigtableDataClient(project=parts[1]) as data_client:
            with data_client.get_table(parts[3], parts[5]) as data_table:
                data_table.read_rows(ReadRowsQuery(limit=1))
