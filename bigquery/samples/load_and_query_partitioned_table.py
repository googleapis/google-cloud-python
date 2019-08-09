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


def load_and_query_partitioned_table(client, to_delete):

    # [START bigquery_query_partitioned_table]
    dataset_id = "load_partitioned_table_dataset_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # [START bigquery_load_table_partitioned]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'
    table_id = "us_states_by_date"

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
        bigquery.SchemaField("date", "DATE"),
    ]
    job_config.skip_leading_rows = 1
    job_config.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date",  # name of column to use for partitioning
        expiration_ms=7776000000,
    )  # 90 days
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states-by-date.csv"

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table(table_id), job_config=job_config
    )  # API request

    assert load_job.job_type == "load"

    load_job.result()  # Waits for table load to complete.

    table = client.get_table(dataset_ref.table(table_id))
    print("Loaded {} rows to table {}".format(table.num_rows, table_id))
    # [END bigquery_load_table_partitioned]
    assert table.num_rows == 50

    project_id = client.project

    import datetime

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project_id = 'my-project'
    # dataset_id = 'my_dataset'
    table_id = "us_states_by_date"

    sql_template = """
        SELECT *
        FROM `{}.{}.{}`
        WHERE date BETWEEN @start_date AND @end_date
    """
    sql = sql_template.format(project_id, dataset_id, table_id)
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = [
        bigquery.ScalarQueryParameter("start_date", "DATE", datetime.date(1800, 1, 1)),
        bigquery.ScalarQueryParameter("end_date", "DATE", datetime.date(1899, 12, 31)),
    ]

    # API request
    query_job = client.query(sql, job_config=job_config)

    rows = list(query_job)
    print("{} states were admitted to the US in the 1800s".format(len(rows)))
    assert len(rows) == 29

    # [END bigquery_query_partitioned_table]