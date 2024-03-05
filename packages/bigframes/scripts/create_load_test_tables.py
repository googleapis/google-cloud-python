# Copyright 2024 Google LLC
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

import math
import os
import pathlib
import sys

import google.cloud.bigquery as bigquery

REPO_ROOT = pathlib.Path(__file__).parent.parent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    print(
        "Please set GOOGLE_CLOUD_PROJECT environment variable before running.",
        file=sys.stderr,
    )
    sys.exit(1)

DATASET_ID = f"{PROJECT_ID}.load_testing"
TABLE_ID = f"{DATASET_ID}.scalars"
TABLE_ID_FORMAT = f"{DATASET_ID}.scalars_{{size}}"

KB_BYTES = 1000
MB_BYTES = 1000 * KB_BYTES
GB_BYTES = 1000 * MB_BYTES
TB_BYTES = 1000 * GB_BYTES
SIZES = (
    ("1mb", MB_BYTES),
    ("10mb", 10 * MB_BYTES),
    ("100mb", 100 * MB_BYTES),
    ("1gb", GB_BYTES),
    ("10gb", 10 * GB_BYTES),
    ("100gb", 100 * GB_BYTES),
    ("1tb", TB_BYTES),
)
SCHEMA_PATH = REPO_ROOT / "tests" / "data" / "scalars_schema.json"
DATA_PATH = REPO_ROOT / "tests" / "data" / "scalars.jsonl"
BQCLIENT = bigquery.Client()


def create_dataset():
    dataset = bigquery.Dataset(DATASET_ID)
    BQCLIENT.create_dataset(dataset, exists_ok=True)


def load_scalars_table():
    schema = BQCLIENT.schema_from_json(SCHEMA_PATH)
    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    print(f"Creating {TABLE_ID}")
    with open(DATA_PATH, "rb") as data_file:
        BQCLIENT.load_table_from_file(
            data_file,
            TABLE_ID,
            job_config=job_config,
        ).result()


def multiply_table(previous_table_id, target_table_id, multiplier):
    clauses = [f"SELECT * FROM `{previous_table_id}`"] * multiplier
    query = " UNION ALL ".join(clauses)
    job_config = bigquery.QueryJobConfig()
    job_config.destination = target_table_id
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    print(f"Creating {target_table_id}, {multiplier} x {previous_table_id}")
    BQCLIENT.query_and_wait(query, job_config=job_config)


def create_tables():
    base_table = BQCLIENT.get_table(TABLE_ID)
    previous_bytes = base_table.num_bytes
    previous_table_id = TABLE_ID

    for table_suffix, target_bytes in SIZES:
        # Make sure we exceed the desired bytes by adding to the multiplier.
        multiplier = math.ceil(target_bytes / previous_bytes) + 1
        target_table_id = TABLE_ID_FORMAT.format(size=table_suffix)
        multiply_table(previous_table_id, target_table_id, multiplier)

        table = BQCLIENT.get_table(target_table_id)
        previous_bytes = table.num_bytes
        previous_table_id = target_table_id


def main():
    create_dataset()
    load_scalars_table()
    create_tables()


if __name__ == "__main__":
    main()
