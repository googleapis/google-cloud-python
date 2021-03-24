# Copyright 2021 The PyBigQuery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import pathlib

import pytest
from google.cloud import bigquery

from typing import List


DATA_DIR = pathlib.Path(__file__).parent / "data"


def load_sample_data(
    full_table_id: str,
    bigquery_client: bigquery.Client,
    bigquery_schema: List[bigquery.SchemaField],
    filename: str = "sample.json",
):
    # Delete the table first. Even though we can use WRITE_TRUNCATE, the load
    # job fails if properties such as table description do not match.
    bigquery_client.delete_table(full_table_id, not_found_ok=True)
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
    dataset_id = "test_pybigquery"
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset = bigquery_client.create_dataset(dataset, exists_ok=True)
    empty_table = bigquery.Table(
        f"{project_id}.{dataset_id}.sample_dml", schema=bigquery_schema
    )
    view = bigquery.Table(f"{project_id}.{dataset_id}.sample_view",)
    view.view_query = f"SELECT string FROM `{dataset_id}.sample`"
    job1 = load_sample_data(
        f"{project_id}.{dataset_id}.sample", bigquery_client, bigquery_schema
    )
    job2 = load_sample_data(
        f"{project_id}.{dataset_id}.sample_one_row",
        bigquery_client,
        bigquery_schema,
        filename="sample_one_row.json",
    )
    bigquery_client.create_table(empty_table, exists_ok=True)
    job1.result()
    job2.result()
    bigquery_client.create_table(view, exists_ok=True)
    return dataset_id


@pytest.fixture(scope="session", autouse=True)
def bigquery_alt_dataset(
    bigquery_client: bigquery.Client, bigquery_schema: List[bigquery.SchemaField]
):
    project_id = bigquery_client.project
    dataset_id = "test_pybigquery_alt"
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset = bigquery_client.create_dataset(dataset, exists_ok=True)
    job = load_sample_data(
        f"{project_id}.{dataset_id}.sample_alt", bigquery_client, bigquery_schema
    )
    job.result()
    return dataset_id


@pytest.fixture(scope="session", autouse=True)
def bigquery_regional_dataset(bigquery_client, bigquery_schema):
    project_id = bigquery_client.project
    dataset_id = "test_pybigquery_location"
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = "asia-northeast1"
    dataset = bigquery_client.create_dataset(dataset, exists_ok=True)
    job = load_sample_data(
        f"{project_id}.{dataset_id}.sample_one_row",
        bigquery_client,
        bigquery_schema,
        filename="sample_one_row.json",
    )
    job.result()
    return dataset_id
