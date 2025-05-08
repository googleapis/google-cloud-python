# Copyright 2025 Google LLC
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

import time
from typing import Generator
import uuid

import pytest

import bigframes

pytest.importorskip("google.cloud.bigtable")

from google.cloud import bigtable  # noqa
from google.cloud.bigtable import column_family, instance, table  # noqa


@pytest.fixture(scope="session")
def bigtable_instance(session_load: bigframes.Session) -> instance.Instance:
    client = bigtable.Client(project=session_load._project, admin=True)

    instance_name = "streaming-testing-instance"
    bt_instance = instance.Instance(
        instance_name,
        client,
    )

    if not bt_instance.exists():
        cluster_id = "streaming-testing-instance-c1"
        cluster = bt_instance.cluster(
            cluster_id,
            location_id="us-west1-a",
            serve_nodes=1,
        )
        operation = bt_instance.create(
            clusters=[cluster],
        )
        operation.result(timeout=480)
    return bt_instance


@pytest.fixture(scope="function")
def bigtable_table(
    bigtable_instance: instance.Instance,
) -> Generator[table.Table, None, None]:
    table_id = "bigframes_test_" + uuid.uuid4().hex
    bt_table = table.Table(
        table_id,
        bigtable_instance,
    )
    max_versions_rule = column_family.MaxVersionsGCRule(1)
    column_family_id = "body_mass_g"
    column_families = {column_family_id: max_versions_rule}
    bt_table.create(column_families=column_families)
    yield bt_table
    bt_table.delete()


@pytest.mark.flaky(retries=3, delay=10)
def test_streaming_df_to_bigtable(
    session_load: bigframes.Session, bigtable_table: table.Table
):
    # launch a continuous query
    job_id_prefix = "test_streaming_"
    sdf = session_load.read_gbq_table_streaming("birds.penguins_bigtable_streaming")

    sdf = sdf[["species", "island", "body_mass_g"]]
    sdf = sdf[sdf["body_mass_g"] < 4000]
    sdf = sdf.rename(columns={"island": "rowkey"})

    try:
        query_job = sdf.to_bigtable(
            instance="streaming-testing-instance",
            table=bigtable_table.table_id,
            service_account_email="streaming-testing-admin@bigframes-load-testing.iam.gserviceaccount.com",
            app_profile=None,
            truncate=True,
            overwrite=True,
            auto_create_column_families=True,
            bigtable_options={},
            job_id=None,
            job_id_prefix=job_id_prefix,
        )

        # wait 100 seconds in order to ensure the query doesn't stop
        # (i.e. it is continuous)
        time.sleep(100)
        assert query_job.running()
        assert query_job.error_result is None
        assert str(query_job.job_id).startswith(job_id_prefix)
        assert len(list(bigtable_table.read_rows())) > 0
    finally:
        query_job.cancel()
