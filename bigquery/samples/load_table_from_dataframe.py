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


def load_table_from_dataframe(client, to_delete, parquet_engine):

    # [START bigquery_load_table_dataframe]
    if parquet_engine == "pyarrow" and pyarrow is None:
        pytest.skip("Requires `pyarrow`")
    if parquet_engine == "fastparquet" and fastparquet is None:
        pytest.skip("Requires `fastparquet`")

    pandas.set_option("io.parquet.engine", parquet_engine)

    dataset_id = "load_table_from_dataframe_{}".format(_millis())
    dataset = bigquery.Dataset(client.dataset(dataset_id))
    client.create_dataset(dataset)
    to_delete.append(dataset)

    # from google.cloud import bigquery
    # import pandas
    # client = bigquery.Client()
    # dataset_id = 'my_dataset'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table("monty_python")
    records = [
        {"title": "The Meaning of Life", "release_year": 1983},
        {"title": "Monty Python and the Holy Grail", "release_year": 1975},
        {"title": "Life of Brian", "release_year": 1979},
        {"title": "And Now for Something Completely Different", "release_year": 1971},
    ]
    # Optionally set explicit indices.
    # If indices are not specified, a column will be created for the default
    # indices created by pandas.
    index = ["Q24980", "Q25043", "Q24953", "Q16403"]
    dataframe = pandas.DataFrame(records, index=pandas.Index(index, name="wikidata_id"))

    job = client.load_table_from_dataframe(dataframe, table_ref, location="US")

    job.result()  # Waits for table load to complete.

    assert job.state == "DONE"
    table = client.get_table(table_ref)
    assert table.num_rows == 4
    column_names = [field.name for field in table.schema]
    assert sorted(column_names) == ["release_year", "title", "wikidata_id"]

    # [END bigquery_load_table_dataframe]