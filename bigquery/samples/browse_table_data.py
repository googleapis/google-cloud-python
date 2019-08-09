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


def browse_table_data(client, to_delete, capsys):

    # [START bigquery_browse_table]
    """Retreive selected row data from a table."""

    # from google.cloud import bigquery
    # client = bigquery.Client()

    dataset_ref = client.dataset("samples", project="bigquery-public-data")
    table_ref = dataset_ref.table("shakespeare")
    table = client.get_table(table_ref)  # API call

    # Load all rows from a table
    rows = client.list_rows(table)
    assert len(list(rows)) == table.num_rows

    # Load the first 10 rows
    rows = client.list_rows(table, max_results=10)
    assert len(list(rows)) == 10

    # Specify selected fields to limit the results to certain columns
    fields = table.schema[:2]  # first two columns
    rows = client.list_rows(table, selected_fields=fields, max_results=10)
    assert len(rows.schema) == 2
    assert len(list(rows)) == 10

    # Use the start index to load an arbitrary portion of the table
    rows = client.list_rows(table, start_index=10, max_results=10)

    # Print row data in tabular format
    format_string = "{!s:<16} " * len(rows.schema)
    field_names = [field.name for field in rows.schema]
    print(format_string.format(*field_names))  # prints column headers
    for row in rows:
        print(format_string.format(*row))  # prints row data

    out, err = capsys.readouterr()
    out = list(filter(bool, out.split("\n")))  # list of non-blank lines
    assert len(out) == 11

    # [END bigquery_browse_table]