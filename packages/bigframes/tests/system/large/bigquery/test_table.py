# Copyright 2026 Google LLC
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

import bigframes.bigquery as bbq


def test_create_external_table(session, dataset_id, bq_connection):
    table_name = f"{dataset_id}.test_object_table"
    uri = "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*"

    # Create the external table
    table = bbq.create_external_table(
        table_name,
        connection_name=bq_connection,
        options={"object_metadata": "SIMPLE", "uris": [uri]},
        session=session,
    )
    assert table is not None

    # Read the table to verify
    import bigframes.pandas as bpd

    bf_df = bpd.read_gbq(table_name)
    pd_df = bf_df.to_pandas()
    assert len(pd_df) > 0
