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


def browse_table_data(client, table_id):

    # [START bigquery_browse_table]
    """Retreive selected row data from a table."""

    from google.cloud import bigquery

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows
    # table_id = "your-project.your_dataset.your_table_name"

    table = client.get_table(table_id)  # API call

    # Load all rows from a table
    rows = client.list_rows(table)
    if len(list(rows)) == table.num_rows:
        print("The amount of rows in the table = {}".format(table.num_rows))

    # Load the first 10 rows
    rows = client.list_rows(table, max_results=10)
    number_of_rows = len(list(rows))
    if number_of_rows == 10:
        print("First {} rows of the table are loaded".format(number_of_rows))

    # Specify selected fields to limit the results to certain columns
    fields = table.schema[:2]  # first two columns
    rows = client.list_rows(table, selected_fields=fields, max_results=10)
    if len(rows.schema) == 2:
        print("Fields number set to {}".format(len(rows.schema)))
    if len(list(rows)) == 10:
        print("{} rows of the table loaded".format(number_of_rows))

    # Use the start index to load an arbitrary portion of the table
    rows = client.list_rows(table, start_index=10, max_results=10)

    # Print row data in tabular format
    format_string = "{!s:<16} " * len(rows.schema)
    field_names = [field.name for field in rows.schema]
    print(format_string.format(*field_names))  # prints column headers
    for number_of_rows, row in enumerate(rows, 1):
        print(format_string.format(*row))  # prints row data

    print("Printed data contains {} rows".format(number_of_rows))

    # [END bigquery_browse_table]
