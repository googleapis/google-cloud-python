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


from google.cloud import bigtable
from google.cloud.bigtable.column_family import ColumnFamily
from google.cloud.bigtable_admin_v2.types import ColumnFamily as ColumnFamily_pb
from google.api_core import exceptions
from google.api_core.retry import Retry
from google.api_core.retry import if_exception_type

delete_retry = Retry(if_exception_type(exceptions.TooManyRequests, exceptions.ServiceUnavailable))

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
        if self._table.exists():
            if self._verbose:
                print(f"deleting table: {self._table.table_id}")
            delete_retry(self._table.delete())
        else:
            if self._verbose:
                print(f"table {self._table.table_id} not found")


def create_table(project, instance_id, table_id, column_families={}):
    """
    Creates a new table, and blocks until it reaches a ready state
    """
    client = bigtable.Client(project=project, admin=True)
    instance = client.instance(instance_id)

    table = instance.table(table_id)
    if table.exists():
        table.delete()

    # convert column families to pb if needed
    pb_families = {
        id: ColumnFamily(id, table, rule).to_pb() if not isinstance(rule, ColumnFamily_pb) else rule
        for (id, rule) in column_families.items()
    }

    # create table using gapic layer
    instance._client.table_admin_client.create_table(
        request={
            "parent": instance.name,
            "table_id": table_id,
            "table": {"column_families": pb_families},
        }
    )

    wait_for_table(table)

    return table

@Retry(
    on_error=if_exception_type(
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
    if not table.exists():
        raise exceptions.NotFound