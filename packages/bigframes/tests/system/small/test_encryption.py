# Copyright 2023 Google LLC
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


import random

from google.cloud import bigquery
import pandas
import pytest

import bigframes
import bigframes.ml.linear_model
from bigframes.testing import utils


@pytest.fixture(scope="module")
def bq_cmek() -> str:
    """Customer managed encryption key to encrypt BigQuery data at rest.

    This is of the form projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY

    See https://cloud.google.com/bigquery/docs/customer-managed-encryption for steps.
    """

    # NOTE: This key is manually set up through the cloud console
    # TODO(shobs): Automate the the key creation during the test. This will
    # require extra IAM privileges for the test runner.
    return "projects/bigframes-dev-perf/locations/us/keyRings/bigframesKeyRing/cryptoKeys/bigframesKey"


@pytest.fixture(scope="module")
def session_with_bq_cmek(bq_cmek) -> bigframes.Session:
    # allow_large_results = False might not create table, and therefore no encryption config
    session = bigframes.Session(bigframes.BigQueryOptions(kms_key_name=bq_cmek))

    return session


def _assert_bq_table_is_encrypted(
    df: bigframes.dataframe.DataFrame,
    cmek: str,
    session: bigframes.Session,
):
    # Materialize the data in BQ
    df.to_gbq()

    # The df should be backed by a query job with intended encryption on the result table
    assert df.query_job is not None
    assert df.query_job.destination_encryption_configuration.kms_key_name.startswith(
        cmek
    )

    # The result table should exist with the intended encryption
    table = session.bqclient.get_table(df.query_job.destination)
    assert table.encryption_configuration.kms_key_name == cmek


def test_session_query_job(bq_cmek, session_with_bq_cmek):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    query_job = session_with_bq_cmek._loader._start_query_with_job(
        "SELECT 123", job_config=bigquery.QueryJobConfig(use_query_cache=False)
    )
    query_job.result()

    assert query_job.destination_encryption_configuration.kms_key_name.startswith(
        bq_cmek
    )

    # The result table should exist with the intended encryption
    table = session_with_bq_cmek.bqclient.get_table(query_job.destination)
    assert table.encryption_configuration.kms_key_name == bq_cmek


def test_read_gbq(bq_cmek, session_with_bq_cmek, scalars_table_id):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Read the BQ table
    df = session_with_bq_cmek.read_gbq(scalars_table_id)

    # Assert encryption
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)


def test_df_apis(bq_cmek, session_with_bq_cmek, scalars_table_id):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Read a BQ table and assert encryption
    df = session_with_bq_cmek.read_gbq(scalars_table_id)

    # Perform a few dataframe operations and assert encryption
    df1 = df.dropna()
    _assert_bq_table_is_encrypted(df1, bq_cmek, session_with_bq_cmek)

    df2 = df1.head()
    _assert_bq_table_is_encrypted(df2, bq_cmek, session_with_bq_cmek)


@pytest.mark.parametrize(
    "engine",
    [
        pytest.param("bigquery", id="bq_engine"),
        pytest.param(
            None,
            id="default_engine",
        ),
    ],
)
def test_read_csv_gcs(
    bq_cmek, session_with_bq_cmek, scalars_df_index, gcs_folder, engine
):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Let's make the source data non-deterministic so that the test doesn't run
    # into a BQ caching path
    df = scalars_df_index.copy()
    df["int_random"] = random.randint(0, 1_000_000_000)

    # Export the dataframe to a csv in gcs
    write_path = gcs_folder + "test_read_csv_gcs_bigquery_engine*.csv"
    read_path = (
        utils.get_first_file_from_wildcard(write_path) if engine is None else write_path
    )
    df.to_csv(write_path)

    # Read the gcs csv
    df = session_with_bq_cmek.read_csv(read_path, engine=engine)

    # Assert encryption
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)


def test_to_gbq(bq_cmek, session_with_bq_cmek, scalars_table_id):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Read a BQ table and assert encryption
    df = session_with_bq_cmek.read_gbq(scalars_table_id)
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)

    # Modify the dataframe and assert encryption
    df = df.dropna().head()
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)

    # Write the result to BQ and assert encryption
    output_table_id = df.to_gbq()
    output_table = session_with_bq_cmek.bqclient.get_table(output_table_id)
    assert output_table.encryption_configuration.kms_key_name == bq_cmek

    # Write the result to BQ custom table and assert encryption
    session_with_bq_cmek.bqclient.get_table(output_table_id)
    output_table_ref = session_with_bq_cmek._anon_dataset_manager.allocate_temp_table()
    output_table_id = str(output_table_ref)
    df.to_gbq(output_table_id)
    output_table = session_with_bq_cmek.bqclient.get_table(output_table_id)
    assert output_table.encryption_configuration.kms_key_name == bq_cmek

    # Lastly, assert that the encryption is not because of any default set at
    # the dataset level
    output_table_dataset = session_with_bq_cmek.bqclient.get_dataset(
        output_table.dataset_id
    )
    assert output_table_dataset.default_encryption_configuration is None


def test_read_pandas(bq_cmek, session_with_bq_cmek):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Read a pandas dataframe
    df = session_with_bq_cmek.read_pandas(
        pandas.DataFrame([random.randint(0, 1_000_000_000)])
    )

    # Assert encryption
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)


def test_read_pandas_large(bq_cmek, session_with_bq_cmek):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    # Read a pandas dataframe large enough to trigger a BQ load job
    df = session_with_bq_cmek.read_pandas(pandas.DataFrame(range(10_000)))

    # Assert encryption
    _assert_bq_table_is_encrypted(df, bq_cmek, session_with_bq_cmek)


def test_kms_encryption_bqml(bq_cmek, session_with_bq_cmek, penguins_table_id):
    if not bq_cmek:  # pragma: NO COVER
        pytest.skip("no cmek set for testing")  # pragma: NO COVER

    model = bigframes.ml.linear_model.LinearRegression()
    df = session_with_bq_cmek.read_gbq(penguins_table_id).dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_train = df[["body_mass_g"]]
    model.fit(X_train, y_train)

    assert model is not None
    assert model._bqml_model is not None
    assert model._bqml_model.model.encryption_configuration is not None
    assert model._bqml_model.model.encryption_configuration.kms_key_name == bq_cmek

    # Assert that model exists in BQ with intended encryption
    model_bq = session_with_bq_cmek.bqclient.get_model(model._bqml_model.model_name)
    assert model_bq.encryption_configuration.kms_key_name == bq_cmek

    # Explicitly save the model to a destination and assert that encryption holds
    model_ref = model._bqml_model_factory._create_model_ref(
        session_with_bq_cmek._anonymous_dataset
    )
    model_ref_full_name = (
        f"{model_ref.project}.{model_ref.dataset_id}.{model_ref.model_id}"
    )
    new_model = model.to_gbq(model_ref_full_name)
    assert new_model._bqml_model is not None
    assert new_model._bqml_model.model.encryption_configuration is not None
    assert new_model._bqml_model.model.encryption_configuration.kms_key_name == bq_cmek

    # Assert that model exists in BQ with intended encryption
    model_bq = session_with_bq_cmek.bqclient.get_model(new_model._bqml_model.model_name)
    assert model_bq.encryption_configuration.kms_key_name == bq_cmek

    # Assert that model registration keeps the encryption
    # Note that model registration only creates an entry (metadata) to be
    # included in the Vertex AI Model Registry. See for more details
    # https://cloud.google.com/bigquery/docs/update_vertex#add-existing.
    # When use deploys the model to an endpoint from the Model Registry then
    # they can specify an encryption key to further protect the artifacts at
    # rest on the Vertex AI side. See for more details:
    # https://cloud.google.com/vertex-ai/docs/general/deployment#deploy_a_model_to_an_endpoint,
    # https://cloud.google.com/vertex-ai/docs/general/cmek#create_resources_with_the_kms_key.
    # bigframes.ml does not provide any API for the model deployment.
    model_registered = new_model.register()
    assert model_registered._bqml_model is not None
    assert model_registered._bqml_model.model.encryption_configuration is not None
    assert (
        model_registered._bqml_model.model.encryption_configuration.kms_key_name
        == bq_cmek
    )
    model_bq = session_with_bq_cmek.bqclient.get_model(new_model._bqml_model.model_name)
    assert model_bq.encryption_configuration.kms_key_name == bq_cmek
