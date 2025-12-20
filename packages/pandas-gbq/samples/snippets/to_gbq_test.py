# Copyright 2019. PyData Development Team
# Distributed under BSD 3-Clause License.
# See LICENSE.txt for details.

"""System tests for to_gbq code samples."""

import random

from . import to_gbq_simple


def test_to_gbq_simple(project_id, bigquery_client, dataset_id):
    table_id = f"{dataset_id}.to_gbq_simple_{random.randint(0, 999999)}"
    to_gbq_simple.main(project_id, table_id)
    table = bigquery_client.get_table(table_id)
    assert table.num_rows == 3
