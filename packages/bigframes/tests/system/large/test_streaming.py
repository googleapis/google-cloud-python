# Copyright 2024 Google LLC
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

import pytest

import bigframes
import bigframes.streaming


@pytest.mark.flaky(retries=3, delay=10)
def test_streaming_df_to_bigtable(session_load: bigframes.Session):
    # launch a continuous query
    job_id_prefix = "test_streaming_"
    sdf = session_load.read_gbq_table_streaming("birds.penguins_bigtable_streaming")

    sdf = sdf[["species", "island", "body_mass_g"]]
    sdf = sdf[sdf["body_mass_g"] < 4000]
    sdf = sdf.rename(columns={"island": "rowkey"})

    query_job = sdf.to_bigtable(
        instance="streaming-testing-instance",
        table="table-testing",
        service_account_email="streaming-testing@bigframes-load-testing.iam.gserviceaccount.com",
        app_profile=None,
        truncate=True,
        overwrite=True,
        auto_create_column_families=True,
        bigtable_options={},
        job_id=None,
        job_id_prefix=job_id_prefix,
    )

    try:
        # wait 100 seconds in order to ensure the query doesn't stop
        # (i.e. it is continuous)
        time.sleep(100)
        assert query_job.running()
        assert query_job.error_result is None
        assert str(query_job.job_id).startswith(job_id_prefix)
    finally:
        query_job.cancel()


@pytest.mark.flaky(retries=3, delay=10)
def test_streaming_df_to_pubsub(session_load: bigframes.Session):
    # launch a continuous query
    job_id_prefix = "test_streaming_pubsub_"
    sdf = session_load.read_gbq_table_streaming("birds.penguins_bigtable_streaming")

    sdf = sdf[sdf["body_mass_g"] < 4000]
    sdf = sdf[["island"]]

    query_job = sdf.to_pubsub(
        topic="penguins",
        service_account_email="streaming-testing@bigframes-load-testing.iam.gserviceaccount.com",
        job_id=None,
        job_id_prefix=job_id_prefix,
    )

    try:
        # wait 100 seconds in order to ensure the query doesn't stop
        # (i.e. it is continuous)
        time.sleep(100)
        assert query_job.running()
        assert query_job.error_result is None
        assert str(query_job.job_id).startswith(job_id_prefix)
    finally:
        query_job.cancel()
