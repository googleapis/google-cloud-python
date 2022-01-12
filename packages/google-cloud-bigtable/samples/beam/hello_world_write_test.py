# Copyright 2020 Google Inc.
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
import os
import uuid

from google.cloud import bigtable
import pytest

import hello_world_write

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BIGTABLE_INSTANCE = os.environ["BIGTABLE_INSTANCE"]
TABLE_ID_PREFIX = "mobile-time-series-{}"


@pytest.fixture(scope="module", autouse=True)
def table_id():
    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)

    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = instance.table(table_id)
    if table.exists():
        table.delete()

    table.create(column_families={"stats_summary": None})
    yield table_id

    table.delete()


def test_hello_world_write(table_id):
    hello_world_write.run(
        [
            "--bigtable-project=%s" % PROJECT,
            "--bigtable-instance=%s" % BIGTABLE_INSTANCE,
            "--bigtable-table=%s" % table_id,
        ]
    )

    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)
    table = instance.table(table_id)

    rows = table.read_rows()
    count = 0
    for _ in rows:
        count += 1
    assert count == 2
