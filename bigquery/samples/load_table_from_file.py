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


def load_table_from_file(client, to_delete):

    # [START bigquery_load_from_file]
    """Upload table data from a CSV file."""
    dataset_id = "load_table_from_file_dataset_{}".format(_millis())
    table_id = "load_table_from_file_table_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    dataset.location = "US"
    client.create_dataset(dataset)
    to_delete.append(dataset)
    snippets_dir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        snippets_dir, "..", "..", "bigquery", "tests", "data", "people.csv"
    )

    # from google.cloud import bigquery
    # client = bigquery.Client()
    # filename = '/path/to/file.csv'
    # dataset_id = 'my_dataset'
    # table_id = 'my_table'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Waits for table load to complete.

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))

    table = client.get_table(table_ref)
    rows = list(client.list_rows(table))  # API request

    assert len(rows) == 2
    # Order is not preserved, so compare individually
    row1 = bigquery.Row(("Wylma Phlyntstone", 29), {"full_name": 0, "age": 1})
    assert row1 in rows
    row2 = bigquery.Row(("Phred Phlyntstone", 32), {"full_name": 0, "age": 1})
    assert row2 in rows

    # [END bigquery_load_from_file]