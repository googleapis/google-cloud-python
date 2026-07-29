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
# See the License for for the specific language governing permissions and
# limitations under the License.

import bigframes.bigquery as bbq


def test_load_data(session, dataset_id):
    table_name = f"{dataset_id}.test_load_data"
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

    # Create the external table
    table = bbq.load_data(
        table_name,
        columns={
            "name": "STRING",
            "post_abbr": "STRING",
        },
        from_files_options={"format": "CSV", "uris": [uri], "skip_leading_rows": 1},
        session=session,
    )
    assert table is not None

    # Read the table to verify
    import bigframes.pandas as bpd

    bf_df = bpd.read_gbq(table_name)
    pd_df = bf_df.to_pandas()
    assert len(pd_df) > 0
