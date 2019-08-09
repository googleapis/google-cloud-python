# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def ddl_create_view(client, to_delete, capsys):

    # [START bigquery_ddl_create_view]
    """Create a view via a DDL query."""
    project = client.project
    dataset_id = "ddl_view_{}".format(_millis())
    table_id = "new_view"
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # project = 'my-project'
    # dataset_id = 'my_dataset'
    # table_id = 'new_view'
    # client = bigquery.Client(project=project)

    sql = """
    CREATE VIEW `{}.{}.{}`
    OPTIONS(
        expiration_timestamp=TIMESTAMP_ADD(
            CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),
        friendly_name="new_view",
        description="a view that expires in 2 days",
        labels=[("org_unit", "development")]
    )
    AS SELECT name, state, year, number
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state LIKE 'W%'
    """.format(
        project, dataset_id, table_id
    )

    job = client.query(sql)  # API request.
    job.result()  # Waits for the query to finish.

    print(
        'Created new view "{}.{}.{}".'.format(
            job.destination.project,
            job.destination.dataset_id,
            job.destination.table_id,
        )
    )

    out, _ = capsys.readouterr()
    assert 'Created new view "{}.{}.{}".'.format(project, dataset_id, table_id) in out

    # Test that listing query result rows succeeds so that generic query
    # processing tools work with DDL statements.
    rows = list(job)
    assert len(rows) == 0

    if pandas is not None:
        df = job.to_dataframe()
        assert len(df) == 0

    # [END bigquery_ddl_create_view]