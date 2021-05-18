# Copyright 2021 The PyBigQuery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import datetime
import pathlib
import random
from typing import List

import pytest

from google.cloud import bigquery


DATA_DIR = pathlib.Path(__file__).parent / "data"


def temp_suffix():
    timestamp = datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")
    random_string = hex(random.randrange(1000000))[2:]
    return f"{timestamp}_{random_string}"


def load_sample_data(
    full_table_id: str,
    bigquery_client: bigquery.Client,
    bigquery_schema: List[bigquery.SchemaField],
    filename: str = "sample.json",
):
    sample_config = bigquery.LoadJobConfig()
    sample_config.destination_table_description = (
        "A sample table containing most data types."
    )
    sample_config.schema = bigquery_schema
    sample_config.time_partitioning = bigquery.TimePartitioning(field="timestamp")
    sample_config.clustering_fields = ["integer", "string"]
    sample_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    sample_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

    with open(DATA_DIR / filename, "rb") as data_file:
        return bigquery_client.load_table_from_file(
            data_file, full_table_id, job_config=sample_config,
        )


@pytest.fixture(scope="session")
def bigquery_client():
    return bigquery.Client()


@pytest.fixture(scope="session")
def bigquery_schema(bigquery_client: bigquery.Client):
    return bigquery_client.schema_from_json(DATA_DIR / "schema.json")


@pytest.fixture(scope="session", autouse=True)
def bigquery_dataset(
    bigquery_client: bigquery.Client, bigquery_schema: List[bigquery.SchemaField]
):
    project_id = bigquery_client.project
    dataset_id = f"test_pybigquery_{temp_suffix()}"
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset = bigquery_client.create_dataset(dataset)
    sample_table_id = f"{project_id}.{dataset_id}.sample"
    job1 = load_sample_data(sample_table_id, bigquery_client, bigquery_schema)
    job1.result()
    one_row_table_id = f"{project_id}.{dataset_id}.sample_one_row"
    job2 = load_sample_data(
        one_row_table_id,
        bigquery_client,
        bigquery_schema,
        filename="sample_one_row.json",
    )
    job2.result()
    view = bigquery.Table(f"{project_id}.{dataset_id}.sample_view",)
    view.view_query = f"SELECT string FROM `{dataset_id}.sample`"
    bigquery_client.create_table(view)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="session", autouse=True)
def bigquery_empty_table(
    bigquery_dataset: str,
    bigquery_client: bigquery.Client,
    bigquery_schema: List[bigquery.SchemaField],
):
    project_id = bigquery_client.project
    # Create new table in its own dataset.
    dataset_id = bigquery_dataset
    table_id = f"{project_id}.{dataset_id}.sample_dml_empty"
    empty_table = bigquery.Table(table_id, schema=bigquery_schema)
    bigquery_client.create_table(empty_table)
    return table_id


@pytest.fixture(scope="session", autouse=True)
def bigquery_regional_dataset(bigquery_client, bigquery_schema):
    project_id = bigquery_client.project
    dataset_id = f"test_pybigquery_location_{temp_suffix()}"
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = "asia-northeast1"
    dataset = bigquery_client.create_dataset(dataset)
    sample_table_id = f"{project_id}.{dataset_id}.sample_one_row"
    job = load_sample_data(
        sample_table_id,
        bigquery_client,
        bigquery_schema,
        filename="sample_one_row.json",
    )
    job.result()
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)
