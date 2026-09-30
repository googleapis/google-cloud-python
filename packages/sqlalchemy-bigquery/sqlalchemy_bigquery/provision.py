# Copyright 2026 Google LLC
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

import contextlib
import os

import google.cloud.bigquery
import test_utils.prefixer
from sqlalchemy.engine import make_url
from sqlalchemy.testing.provision import (
    create_db,
    drop_db,
    follower_url_from_main,
)

prefixer = test_utils.prefixer.Prefixer(
    "python-bigquery-sqlalchemy", "tests/compliance"
)


def _dataset_id_from_ident(ident: str) -> str:
    """Derive a deterministic BigQuery dataset ID for an xdist follower ident."""
    run_prefix = os.environ.get("COMPLIANCE_RUN_PREFIX")
    if not run_prefix:
        run_prefix = prefixer.create_prefix()
    return f"{run_prefix}_{ident}"


@follower_url_from_main.for_db("bigquery")
def _bigquery_follower_url_from_main(url, ident):
    url = make_url(url)
    dataset_id = _dataset_id_from_ident(ident)
    return url.set(database=dataset_id)


@create_db.for_db("bigquery")
def _bigquery_create_db(cfg, eng, ident):
    dataset_id = _dataset_id_from_ident(ident)
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        dataset_ref = google.cloud.bigquery.DatasetReference(client.project, dataset_id)
        dataset = google.cloud.bigquery.Dataset(dataset_ref)
        # Set 1-hour expiration as safety net in case of process termination
        dataset.default_table_expiration_ms = 3600 * 1000
        client.create_dataset(dataset, exists_ok=True)


@drop_db.for_db("bigquery")
def _bigquery_drop_db(cfg, eng, ident):
    dataset_id = _dataset_id_from_ident(ident)
    with contextlib.closing(google.cloud.bigquery.Client()) as client:
        client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
