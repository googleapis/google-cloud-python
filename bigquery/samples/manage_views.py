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


def manage_views(client, to_delete):

    # [START bigquery_grant_view_access]
    project = client.project
    source_dataset_id = "source_dataset_{}".format(_millis())
    source_dataset_ref = client.dataset(source_dataset_id)
    source_dataset = bigquery.Dataset(source_dataset_ref)
    source_dataset = client.create_dataset(source_dataset)
    to_delete.append(source_dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ]
    job_config.skip_leading_rows = 1
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    source_table_id = "us_states"
    load_job = client.load_table_from_uri(
        uri, source_dataset.table(source_table_id), job_config=job_config
    )
    load_job.result()

    shared_dataset_id = "shared_dataset_{}".format(_millis())
    shared_dataset_ref = client.dataset(shared_dataset_id)
    shared_dataset = bigquery.Dataset(shared_dataset_ref)
    shared_dataset = client.create_dataset(shared_dataset)
    to_delete.append(shared_dataset)

    # [START bigquery_create_view]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    # source_table_id = 'us_states'
    # shared_dataset_ref = client.dataset('my_shared_dataset')

    # This example shows how to create a shared view of a source table of
    # US States. The source table contains all 50 states, while the view will
    # contain only states with names starting with 'W'.
    view_ref = shared_dataset_ref.table("my_shared_view")
    view = bigquery.Table(view_ref)
    sql_template = 'SELECT name, post_abbr FROM `{}.{}.{}` WHERE name LIKE "W%"'
    view.view_query = sql_template.format(project, source_dataset_id, source_table_id)
    view = client.create_table(view)  # API request

    print("Successfully created view at {}".format(view.full_table_id))
    # [END bigquery_create_view]

    # [START bigquery_update_view_query]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    # source_table_id = 'us_states'
    # shared_dataset_ref = client.dataset('my_shared_dataset')

    # This example shows how to update a shared view of a source table of
    # US States. The view's query will be updated to contain only states with
    # names starting with 'M'.
    view_ref = shared_dataset_ref.table("my_shared_view")
    view = bigquery.Table(view_ref)
    sql_template = 'SELECT name, post_abbr FROM `{}.{}.{}` WHERE name LIKE "M%"'
    view.view_query = sql_template.format(project, source_dataset_id, source_table_id)
    view = client.update_table(view, ["view_query"])  # API request
    # [END bigquery_update_view_query]

    # [START bigquery_get_view]
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # shared_dataset_id = 'my_shared_dataset'

    view_ref = client.dataset(shared_dataset_id).table("my_shared_view")
    view = client.get_table(view_ref)  # API Request

    # Display view properties
    print("View at {}".format(view.full_table_id))
    print("View Query:\n{}".format(view.view_query))
    # [END bigquery_get_view]
    assert view.view_query is not None

    analyst_group_email = "example-analyst-group@google.com"
    # from google.cloud import bigquery
    # client = bigquery.Client()

    # Assign access controls to the dataset containing the view
    # shared_dataset_id = 'my_shared_dataset'
    # analyst_group_email = 'data_analysts@example.com'
    shared_dataset = client.get_dataset(
        client.dataset(shared_dataset_id)
    )  # API request
    access_entries = shared_dataset.access_entries
    access_entries.append(
        bigquery.AccessEntry("READER", "groupByEmail", analyst_group_email)
    )
    shared_dataset.access_entries = access_entries
    shared_dataset = client.update_dataset(
        shared_dataset, ["access_entries"]
    )  # API request

    # Authorize the view to access the source dataset
    # project = 'my-project'
    # source_dataset_id = 'my_source_dataset'
    source_dataset = client.get_dataset(
        client.dataset(source_dataset_id)
    )  # API request
    view_reference = {
        "projectId": project,
        "datasetId": shared_dataset_id,
        "tableId": "my_shared_view",
    }
    access_entries = source_dataset.access_entries
    access_entries.append(bigquery.AccessEntry(None, "view", view_reference))
    source_dataset.access_entries = access_entries
    source_dataset = client.update_dataset(
        source_dataset, ["access_entries"]
    )  # API request

    # [END bigquery_grant_view_access]