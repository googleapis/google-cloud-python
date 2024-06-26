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

import bigframes.streaming


def test_streaming_to_bigtable():
    # launch a continuous query
    job_id_prefix = "test_streaming_"
    sql = """SELECT
        body_mass_g, island as rowkey
        FROM birds.penguins_bigtable_streaming"""
    query_job = bigframes.streaming.to_bigtable(
        sql,
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
        assert query_job.error_result is None
        assert query_job.errors is None
        assert query_job.running()
        assert str(query_job.job_id).startswith(job_id_prefix)
    finally:
        query_job.cancel()


def test_streaming_to_pubsub():
    # launch a continuous query
    job_id_prefix = "test_streaming_pubsub_"
    sql = """SELECT
        island
        FROM birds.penguins_pubsub_streaming"""
    query_job = bigframes.streaming.to_pubsub(
        sql,
        topic="penguins",
        service_account_email="streaming-testing@bigframes-load-testing.iam.gserviceaccount.com",
        job_id=None,
        job_id_prefix=job_id_prefix,
    )

    try:
        # wait 100 seconds in order to ensure the query doesn't stop
        # (i.e. it is continuous)
        time.sleep(100)
        assert query_job.error_result is None
        assert query_job.errors is None
        assert query_job.running()
        assert str(query_job.job_id).startswith(job_id_prefix)
    finally:
        query_job.cancel()
