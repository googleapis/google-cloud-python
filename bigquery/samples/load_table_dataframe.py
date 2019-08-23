# Copyright 2019 Google LLC
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


def load_table_dataframe(client, table_id):
    # [START bigquery_load_table_dataframe]
    from google.cloud import bigquery
    import pandas

    # TODO(developer): Construct a BigQuery client object.
    # client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    records = [
        {"title": u"The Meaning of Life", "release_year": 1983},
        {"title": u"Monty Python and the Holy Grail", "release_year": 1975},
        {"title": u"Life of Brian", "release_year": 1979},
        {"title": u"And Now for Something Completely Different", "release_year": 1971},
    ]
    # Optionally set explicit indices.
    index = [u"Q24980", u"Q25043", u"Q24953", u"Q16403"]
    dataframe = pandas.DataFrame(records, index=pandas.Index(index, name="wikidata_id"))
    job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
            # Indexes are written if included in the schema by name.
            bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
        ]
    )

    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config, location="US"
    )
    job.result()  # Waits for table load to complete.

    table = client.get_table(table_id)
    print("Wrote {} rows to {}".format(table.num_rows, table_id))
    # [END bigquery_load_table_dataframe]


if __name__ == "__main__":
    import sys
    from google.cloud import bigquery

    load_table_dataframe(bigquery.Client(), sys.argv[1])
