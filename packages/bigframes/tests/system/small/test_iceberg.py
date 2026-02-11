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
import pytest

import bigframes
import bigframes.pandas as bpd


@pytest.fixture()
def fresh_global_session():
    bpd.reset_session()
    yield None
    bpd.close_session()
    # Undoes side effect of using ths global session to read table
    bpd.options.bigquery.location = None


def test_read_iceberg_table_w_location():
    session = bigframes.Session(bigframes.BigQueryOptions(location="us-central1"))
    df = session.read_gbq(
        "bigquery-public-data.biglake-public-nyc-taxi-iceberg.public_data.nyc_taxicab_2021"
    )
    assert df.shape == (30904427, 20)


def test_read_iceberg_table_w_wrong_location():
    session = bigframes.Session(bigframes.BigQueryOptions(location="europe-west1"))
    with pytest.raises(ValueError, match="Current session is in europe-west1"):
        session.read_gbq(
            "bigquery-public-data.biglake-public-nyc-taxi-iceberg.public_data.nyc_taxicab_2021"
        )


def test_read_iceberg_table_wo_location(fresh_global_session):
    df = bpd.read_gbq(
        "bigquery-public-data.biglake-public-nyc-taxi-iceberg.public_data.nyc_taxicab_2021"
    )
    assert df.shape == (30904427, 20)
