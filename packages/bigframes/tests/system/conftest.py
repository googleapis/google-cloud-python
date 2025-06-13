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

from datetime import datetime
import hashlib
import logging
import math
import pathlib
import textwrap
import traceback
import typing
from typing import Dict, Generator, Optional

import google.api_core.exceptions
import google.cloud.bigquery as bigquery
import google.cloud.bigquery_connection_v1 as bigquery_connection_v1
import google.cloud.exceptions
import google.cloud.functions_v2 as functions_v2
import google.cloud.resourcemanager_v3 as resourcemanager_v3
import google.cloud.storage as storage  # type: ignore
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
import pytz
import test_utils.prefixer

import bigframes
import bigframes.dataframe
import bigframes.pandas as bpd
import bigframes.series
import bigframes.testing.utils

# Use this to control the number of cloud functions being deleted in a single
# test session. This should help soften the spike of the number of mutations per
# minute tracked against the quota limit:
#   Cloud Functions API -> Per project mutation requests per minute per region
#   (default 60, increased to 1000 for the test projects)
# We are running pytest with "-n 20". For a rough estimation, let's say all
# parallel sessions run in parallel. So that allows 1000/20 = 50 mutations per
# minute. One session takes about 1 minute to create a remote function. This
# would allow 50-1 = 49 deletions per session.
# However, because of b/356217175 the service may throw ResourceExhausted("Too
# many operations are currently being executed, try again later."), so we peg
# the cleanup to a more controlled rate.
MAX_NUM_FUNCTIONS_TO_DELETE_PER_SESSION = 15

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"
PERMANENT_DATASET = "bigframes_testing"
PERMANENT_DATASET_TOKYO = "bigframes_testing_tokyo"
TOKYO_LOCATION = "asia-northeast1"
prefixer = test_utils.prefixer.Prefixer("bigframes", "tests/system")


def _hash_digest_file(hasher, filepath):
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)


@pytest.fixture(scope="session")
def tokyo_location() -> str:
    return TOKYO_LOCATION


@pytest.fixture(scope="session")
def gcs_client() -> storage.Client:
    # TODO(swast): Ensure same credentials and project are used as in the rest
    # of our tests.
    return storage.Client()


@pytest.fixture(scope="session")
def gcs_folder(gcs_client: storage.Client):
    # TODO(swast): Allow bucket name from environment variable for testing by
    # non-Googlers.
    bucket = "bigframes-dev-testing"
    prefix = prefixer.create_prefix()
    path = f"gs://{bucket}/{prefix}/"
    yield path
    try:
        for blob in gcs_client.list_blobs(bucket, prefix=prefix):
            blob = typing.cast(storage.Blob, blob)
            blob.delete()
    except Exception as exc:
        traceback.print_exception(type(exc), exc, None)


@pytest.fixture(scope="session")
def bigquery_client(session: bigframes.Session) -> bigquery.Client:
    return session.bqclient


@pytest.fixture(scope="session")
def bigquery_client_tokyo(session_tokyo: bigframes.Session) -> bigquery.Client:
    return session_tokyo.bqclient


@pytest.fixture(scope="session")
def bigqueryconnection_client(
    session: bigframes.Session,
) -> bigquery_connection_v1.ConnectionServiceClient:
    return session.bqconnectionclient


@pytest.fixture(scope="session")
def cloudfunctions_client(
    session: bigframes.Session,
) -> functions_v2.FunctionServiceClient:
    return session.cloudfunctionsclient


@pytest.fixture(scope="session")
def project_id(bigquery_client: bigquery.Client) -> str:
    return bigquery_client.project


@pytest.fixture(scope="session")
def resourcemanager_client(
    session: bigframes.Session,
) -> resourcemanager_v3.ProjectsClient:
    return session.resourcemanagerclient


@pytest.fixture(scope="session")
def session() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location="US")
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup time


@pytest.fixture(scope="session")
def session_load() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location="US", project="bigframes-load-testing")
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup time


@pytest.fixture(scope="session", params=["strict", "partial"])
def maybe_ordered_session(request) -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location="US", ordering_mode=request.param)
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup type


@pytest.fixture(scope="session")
def unordered_session() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location="US", ordering_mode="partial")
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup type


@pytest.fixture(scope="session")
def session_tokyo(tokyo_location: str) -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location=tokyo_location)
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup type


@pytest.fixture(scope="session")
def test_session() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(
        client_endpoints_override={
            "bqclient": "https://test-bigquery.sandbox.google.com",
            "bqconnectionclient": "test-bigqueryconnection.sandbox.googleapis.com",
            "bqstoragereadclient": "test-bigquerystorage-grpc.sandbox.googleapis.com",
        },
    )
    session = bigframes.Session(context=context)
    yield session
    session.close()


@pytest.fixture(scope="session")
def bq_connection_name() -> str:
    return "bigframes-rf-conn"


@pytest.fixture(scope="session")
def bq_connection(bigquery_client: bigquery.Client, bq_connection_name: str) -> str:
    return f"{bigquery_client.project}.{bigquery_client.location}.{bq_connection_name}"


@pytest.fixture(scope="session", autouse=True)
def cleanup_datasets(bigquery_client: bigquery.Client) -> None:
    """Cleanup any datasets that were created but not cleaned up."""
    for dataset in bigquery_client.list_datasets():
        if prefixer.should_cleanup(dataset.dataset_id):
            bigquery_client.delete_dataset(
                dataset, delete_contents=True, not_found_ok=True
            )


def get_dataset_id(project_id: str):
    "Get a fully qualified dataset id belonging to the given project."
    dataset_id = f"{project_id}.{prefixer.create_prefix()}_dataset_id"
    return dataset_id


@pytest.fixture(scope="session")
def dataset_id(bigquery_client: bigquery.Client):
    """Create (and cleanup) a temporary dataset."""
    dataset_id = get_dataset_id(bigquery_client.project)
    bigquery_client.create_dataset(dataset_id)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture
def dataset_id_not_created(bigquery_client: bigquery.Client):
    """Return a temporary dataset object without creating it, and clean it up
    after it has been used."""
    dataset_id = get_dataset_id(bigquery_client.project)
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="session")
def dataset_id_permanent(bigquery_client: bigquery.Client, project_id: str) -> str:
    """Create a dataset if it doesn't exist."""
    dataset_id = f"{project_id}.{PERMANENT_DATASET}"
    dataset = bigquery.Dataset(dataset_id)
    bigquery_client.create_dataset(dataset, exists_ok=True)
    return dataset_id


@pytest.fixture(scope="session")
def dataset_id_permanent_tokyo(
    bigquery_client_tokyo: bigquery.Client, tokyo_location: str
) -> str:
    """Create a dataset in Tokyo if it doesn't exist."""
    project_id = bigquery_client_tokyo.project
    dataset_id = f"{project_id}.{PERMANENT_DATASET_TOKYO}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = tokyo_location
    dataset = bigquery_client_tokyo.create_dataset(dataset, exists_ok=True)
    assert dataset.location == tokyo_location
    return dataset_id


@pytest.fixture(scope="session")
def table_id_not_created(dataset_id: str):
    return f"{dataset_id}.{prefixer.create_prefix()}"


@pytest.fixture(scope="function")
def table_id_unique(dataset_id: str):
    return f"{dataset_id}.{prefixer.create_prefix()}"


@pytest.fixture(scope="function")
def routine_id_unique(dataset_id: str):
    return f"{dataset_id}.{prefixer.create_prefix()}"


@pytest.fixture(scope="session")
def scalars_schema(bigquery_client: bigquery.Client):
    # TODO(swast): Add missing scalar data types such as BIGNUMERIC.
    # See also: https://github.com/ibis-project/ibis-bigquery/pull/67
    schema = bigquery_client.schema_from_json(DATA_DIR / "scalars_schema.json")
    return tuple(schema)


def load_test_data(
    table_id: str,
    bigquery_client: bigquery.Client,
    schema_filename: str,
    data_filename: str,
    location: Optional[str],
) -> bigquery.LoadJob:
    """Create a temporary table with test data"""
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = tuple(
        bigquery_client.schema_from_json(DATA_DIR / schema_filename)
    )
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    with open(DATA_DIR / data_filename, "rb") as input_file:
        # TODO(swast): Location is allowed to be None in BigQuery Client.
        # Can remove after
        # https://github.com/googleapis/python-bigquery/pull/1554 is released.
        location = "US" if location is None else location
        job = bigquery_client.load_table_from_file(
            input_file,
            table_id,
            job_config=job_config,
            location=location,
        )
    # No cleanup necessary, as the surrounding dataset will delete contents.
    return typing.cast(bigquery.LoadJob, job.result())


def load_test_data_tables(
    session: bigframes.Session, dataset_id_permanent: str
) -> Dict[str, str]:
    """Returns cached references to the test data tables in BigQuery. If no matching table is found
    for the hash of the data and schema, the table will be uploaded."""
    existing_table_ids = [
        table.table_id for table in session.bqclient.list_tables(dataset_id_permanent)
    ]
    table_mapping: Dict[str, str] = {}
    for table_name, schema_filename, data_filename in [
        ("scalars", "scalars_schema.json", "scalars.jsonl"),
        ("scalars_too", "scalars_schema.json", "scalars.jsonl"),
        ("nested", "nested_schema.json", "nested.jsonl"),
        ("nested_structs", "nested_structs_schema.json", "nested_structs.jsonl"),
        ("repeated", "repeated_schema.json", "repeated.jsonl"),
        ("json", "json_schema.json", "json.jsonl"),
        ("penguins", "penguins_schema.json", "penguins.jsonl"),
        ("ratings", "ratings_schema.json", "ratings.jsonl"),
        ("time_series", "time_series_schema.json", "time_series.jsonl"),
        ("hockey_players", "hockey_players.json", "hockey_players.jsonl"),
        ("matrix_2by3", "matrix_2by3.json", "matrix_2by3.jsonl"),
        ("matrix_3by4", "matrix_3by4.json", "matrix_3by4.jsonl"),
        ("urban_areas", "urban_areas_schema.json", "urban_areas.jsonl"),
    ]:
        test_data_hash = hashlib.md5()
        _hash_digest_file(test_data_hash, DATA_DIR / schema_filename)
        _hash_digest_file(test_data_hash, DATA_DIR / data_filename)
        test_data_hash.update(table_name.encode())
        target_table_id = f"{table_name}_{test_data_hash.hexdigest()}"
        target_table_id_full = f"{dataset_id_permanent}.{target_table_id}"
        if target_table_id not in existing_table_ids:
            # matching table wasn't found in the permanent dataset - we need to upload it
            logging.info(
                f"Test data table {table_name} was not found in the permanent dataset, regenerating it..."
            )
            load_test_data(
                target_table_id_full,
                session.bqclient,
                schema_filename,
                data_filename,
                location=session._location,
            )

        table_mapping[table_name] = target_table_id_full

    return table_mapping


@pytest.fixture(scope="session")
def test_data_tables(
    session: bigframes.Session, dataset_id_permanent: str
) -> Dict[str, str]:
    return load_test_data_tables(session, dataset_id_permanent)


@pytest.fixture(scope="session")
def test_data_tables_tokyo(
    session_tokyo: bigframes.Session, dataset_id_permanent_tokyo: str
) -> Dict[str, str]:
    return load_test_data_tables(session_tokyo, dataset_id_permanent_tokyo)


@pytest.fixture(scope="session")
def scalars_table_id(test_data_tables) -> str:
    return test_data_tables["scalars"]


@pytest.fixture(scope="session")
def baseball_schedules_df(session: bigframes.Session) -> bigframes.dataframe.DataFrame:
    """Public BQ table"""
    df = session.read_gbq("bigquery-public-data.baseball.schedules")
    return df


@pytest.fixture(scope="session")
def hockey_table_id(test_data_tables) -> str:
    return test_data_tables["hockey_players"]


@pytest.fixture(scope="session")
def scalars_table_id_2(test_data_tables) -> str:
    return test_data_tables["scalars_too"]


@pytest.fixture(scope="session")
def scalars_table_tokyo(test_data_tables_tokyo) -> str:
    return test_data_tables_tokyo["scalars"]


@pytest.fixture(scope="session")
def nested_table_id(test_data_tables) -> str:
    return test_data_tables["nested"]


@pytest.fixture(scope="session")
def nested_structs_table_id(test_data_tables) -> str:
    return test_data_tables["nested_structs"]


@pytest.fixture(scope="session")
def repeated_table_id(test_data_tables) -> str:
    return test_data_tables["repeated"]


@pytest.fixture(scope="session")
def json_table_id(test_data_tables) -> str:
    return test_data_tables["json"]


@pytest.fixture(scope="session")
def penguins_table_id(test_data_tables) -> str:
    return test_data_tables["penguins"]


@pytest.fixture(scope="session")
def ratings_table_id(test_data_tables) -> str:
    return test_data_tables["ratings"]


@pytest.fixture(scope="session")
def urban_areas_table_id(test_data_tables) -> str:
    return test_data_tables["urban_areas"]


@pytest.fixture(scope="session")
def time_series_table_id(test_data_tables) -> str:
    return test_data_tables["time_series"]


@pytest.fixture(scope="session")
def matrix_2by3_table_id(test_data_tables) -> str:
    return test_data_tables["matrix_2by3"]


@pytest.fixture(scope="session")
def matrix_3by4_table_id(test_data_tables) -> str:
    return test_data_tables["matrix_3by4"]


@pytest.fixture(scope="session")
def nested_df(
    nested_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(nested_table_id, index_col="rowindex")


@pytest.fixture(scope="session")
def nested_pandas_df() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "nested.jsonl",
        lines=True,
    )
    df = df.set_index("rowindex")
    return df


@pytest.fixture(scope="session")
def nested_structs_df(
    nested_structs_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(nested_structs_table_id, index_col="id")


@pytest.fixture(scope="session")
def nested_structs_pandas_df(nested_structs_pandas_type: pd.ArrowDtype) -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "nested_structs.jsonl",
        lines=True,
    )
    df = df.set_index("id")
    df["person"] = df["person"].astype(nested_structs_pandas_type)
    return df


@pytest.fixture(scope="session")
def nested_structs_pandas_type() -> pd.ArrowDtype:
    address_struct_schema = pa.struct(
        [pa.field("city", pa.string()), pa.field("country", pa.string())]
    )

    person_struct_schema = pa.struct(
        [
            pa.field("name", pa.string()),
            pa.field("age", pa.int64()),
            pa.field("address", address_struct_schema),
        ]
    )

    return pd.ArrowDtype(person_struct_schema)


@pytest.fixture(scope="session")
def repeated_df(
    repeated_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """Returns a DataFrame containing columns of list type."""
    return session.read_gbq(repeated_table_id, index_col="rowindex")


@pytest.fixture(scope="session")
def repeated_pandas_df() -> pd.DataFrame:
    """Returns a DataFrame containing columns of list type."""

    df = pd.read_json(
        DATA_DIR / "repeated.jsonl",
        lines=True,
    )
    df = df.set_index("rowindex")
    return df


@pytest.fixture(scope="session")
def json_df(
    json_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """Returns a DataFrame containing columns of JSON type."""
    return session.read_gbq(json_table_id, index_col="rowindex")


@pytest.fixture(scope="session")
def json_pandas_df() -> pd.DataFrame:
    """Returns a DataFrame containing columns of JSON type."""
    df = pd.read_json(
        DATA_DIR / "json.jsonl",
        lines=True,
    )
    df = df.set_index("rowindex")
    return df


@pytest.fixture(scope="session")
def scalars_df_default_index(
    scalars_df_index: bigframes.dataframe.DataFrame,
    scalars_pandas_df_default_index: pd.DataFrame,
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    df = scalars_df_index.reset_index(drop=False)
    # Ensure the order of the columns is the same.
    df = typing.cast(
        bigframes.dataframe.DataFrame, df[scalars_pandas_df_default_index.columns]
    )
    return df


@pytest.fixture(scope="session")
def scalars_df_index(
    scalars_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(scalars_table_id, index_col="rowindex")


@pytest.fixture(scope="session")
def scalars_df_partial_ordering(
    scalars_table_id: str, unordered_session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return unordered_session.read_gbq(
        scalars_table_id, index_col="rowindex"
    ).sort_index()


@pytest.fixture(scope="session")
def scalars_df_null_index(
    scalars_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(
        scalars_table_id, index_col=bigframes.enums.DefaultIndexKind.NULL
    ).sort_values("rowindex")


@pytest.fixture(scope="session")
def scalars_df_2_default_index(
    scalars_df_2_index: bigframes.dataframe.DataFrame,
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return scalars_df_2_index.reset_index(drop=False)


@pytest.fixture(scope="session")
def scalars_df_2_index(
    scalars_table_id_2: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(scalars_table_id_2, index_col="rowindex")


@pytest.fixture(scope="session")
def scalars_pandas_df_default_index() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    bigframes.testing.utils.convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    df.index.name = None
    return df


@pytest.fixture(scope="session")
def scalars_pandas_df_index(
    scalars_pandas_df_default_index: pd.DataFrame,
) -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""
    return scalars_pandas_df_default_index.set_index("rowindex").sort_index()


@pytest.fixture(scope="session")
def scalars_pandas_df_multi_index(
    scalars_pandas_df_default_index: pd.DataFrame,
) -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""
    return scalars_pandas_df_default_index.set_index(
        ["rowindex", "timestamp_col"]
    ).sort_index()


@pytest.fixture(scope="session")
def scalars_dfs(
    scalars_df_index,
    scalars_pandas_df_index,
):
    return scalars_df_index, scalars_pandas_df_index


@pytest.fixture(scope="session")
def scalars_dfs_maybe_ordered(
    maybe_ordered_session,
    scalars_pandas_df_index,
):
    return (
        maybe_ordered_session.read_pandas(scalars_pandas_df_index),
        scalars_pandas_df_index,
    )


@pytest.fixture(scope="session")
def scalars_df_numeric_150_columns_maybe_ordered(
    maybe_ordered_session,
    scalars_pandas_df_index,
):
    """DataFrame pointing at test data."""
    # TODO(b/379911038): After the error fixed, add numeric type.
    pandas_df = scalars_pandas_df_index.reset_index(drop=False)[
        [
            "rowindex",
            "rowindex_2",
            "float64_col",
            "int64_col",
            "int64_too",
        ]
        * 30
    ]

    df = maybe_ordered_session.read_pandas(pandas_df)
    return (df, pandas_df)


@pytest.fixture(scope="session")
def hockey_df(
    hockey_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return (
        session.read_gbq(hockey_table_id)
        .set_index(["player_name", "season"])
        .sort_index()
    )


@pytest.fixture(scope="session")
def hockey_pandas_df() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""
    df = pd.read_json(
        DATA_DIR / "hockey_players.jsonl",
        lines=True,
        dtype={
            "team_name": pd.StringDtype(storage="pyarrow"),
            "position": pd.StringDtype(storage="pyarrow"),
            "player_name": pd.StringDtype(storage="pyarrow"),
            "goals": pd.Int64Dtype(),
            "assists": pd.Int64Dtype(),
            "number": pd.Int64Dtype(),
            "season": pd.Int64Dtype(),
        },
    )
    df = df.set_index(["player_name", "season"]).sort_index()
    return df


@pytest.fixture(scope="session")
def matrix_2by3_df(
    matrix_2by3_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at a test 2-by-3 matrix data."""
    df = session.read_gbq(matrix_2by3_table_id)
    df = df.set_index("rowindex").sort_index()
    return df


@pytest.fixture(scope="session")
def matrix_2by3_pandas_df() -> pd.DataFrame:
    """pd.DataFrame pointing at a test 2-by-3 matrix data."""
    df = pd.read_json(
        DATA_DIR / "matrix_2by3.jsonl",
        lines=True,
        dtype={
            "rowindex": pd.Int64Dtype(),
            "a": pd.Int64Dtype(),
            "b": pd.Int64Dtype(),
            "c": pd.Int64Dtype(),
        },
    )
    df = df.set_index("rowindex").sort_index()
    df.index = df.index.astype("Int64")
    return df


@pytest.fixture(scope="session")
def matrix_3by4_df(
    matrix_3by4_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at a test 3-by-4 matrix data."""
    df = session.read_gbq(matrix_3by4_table_id)
    df = df.set_index("rowindex").sort_index()
    return df


@pytest.fixture(scope="session")
def matrix_3by4_pandas_df() -> pd.DataFrame:
    """pd.DataFrame pointing at a test 3-by-4 matrix data."""
    df = pd.read_json(
        DATA_DIR / "matrix_3by4.jsonl",
        lines=True,
        dtype={
            "rowindex": pd.StringDtype(storage="pyarrow"),
            "w": pd.Int64Dtype(),
            "x": pd.Int64Dtype(),
            "y": pd.Int64Dtype(),
            "z": pd.Int64Dtype(),
        },
    )
    df = df.set_index("rowindex").sort_index()
    return df


@pytest.fixture(scope="session")
def penguins_df_default_index(
    penguins_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(penguins_table_id)


@pytest.fixture(scope="session")
def penguins_df_null_index(
    penguins_table_id: str, unordered_session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return unordered_session.read_gbq(penguins_table_id)


@pytest.fixture(scope="session")
def ratings_df_default_index(
    ratings_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(ratings_table_id)


@pytest.fixture(scope="session")
def time_series_df_default_index(
    time_series_table_id: str, session: bigframes.Session
) -> bigframes.dataframe.DataFrame:
    """DataFrame pointing at test data."""
    return session.read_gbq(time_series_table_id)


@pytest.fixture(scope="session")
def new_time_series_pandas_df():
    """Additional data matching the time series dataset. The values are dummy ones used to basically check the prediction scores."""
    utc = pytz.utc
    return pd.DataFrame(
        {
            "parsed_date": [
                datetime(2017, 8, 2, tzinfo=utc),
                datetime(2017, 8, 3, tzinfo=utc),
                datetime(2017, 8, 4, tzinfo=utc),
            ],
            "total_visits": [2500, 2500, 2500],
        }
    )


@pytest.fixture(scope="session")
def new_time_series_df(session, new_time_series_pandas_df):
    return session.read_pandas(new_time_series_pandas_df)


@pytest.fixture(scope="session")
def new_time_series_pandas_df_w_id():
    """Additional data matching the time series dataset. The values are dummy ones used to basically check the prediction scores."""
    utc = pytz.utc
    return pd.DataFrame(
        {
            "parsed_date": [
                datetime(2017, 8, 2, tzinfo=utc),
                datetime(2017, 8, 2, tzinfo=utc),
                datetime(2017, 8, 3, tzinfo=utc),
                datetime(2017, 8, 3, tzinfo=utc),
                datetime(2017, 8, 4, tzinfo=utc),
                datetime(2017, 8, 4, tzinfo=utc),
            ],
            "id": ["1", "2", "1", "2", "1", "2"],
            "total_visits": [2500, 2500, 2500, 2500, 2500, 2500],
        }
    )


@pytest.fixture(scope="session")
def new_time_series_df_w_id(session, new_time_series_pandas_df_w_id):
    return session.read_pandas(new_time_series_pandas_df_w_id)


@pytest.fixture(scope="session")
def penguins_pandas_df_default_index() -> pd.DataFrame:
    """Consistently ordered pandas dataframe for penguins test data"""
    df = pd.read_json(
        f"{DATA_DIR}/penguins.jsonl",
        lines=True,
        dtype={
            "species": pd.StringDtype(storage="pyarrow"),
            "island": pd.StringDtype(storage="pyarrow"),
            "culmen_length_mm": pd.Float64Dtype(),
            "culmen_depth_mm": pd.Float64Dtype(),
            "flipper_length_mm": pd.Float64Dtype(),
            "sex": pd.StringDtype(storage="pyarrow"),
            "body_mass_g": pd.Float64Dtype(),
        },
    )
    df.index = df.index.astype("Int64")
    return df


@pytest.fixture(scope="session")
def new_penguins_pandas_df():
    """Additional data matching the penguins dataset, with a new index"""
    return pd.DataFrame(
        {
            "tag_number": [1633, 1672, 1690],
            "species": [
                "Adelie Penguin (Pygoscelis adeliae)",
                "Adelie Penguin (Pygoscelis adeliae)",
                "Chinstrap penguin (Pygoscelis antarctica)",
            ],
            "island": ["Torgersen", "Torgersen", "Dream"],
            "culmen_length_mm": [39.5, 38.5, 37.9],
            "culmen_depth_mm": [18.8, 17.2, 18.1],
            "flipper_length_mm": [196.0, 181.0, 188.0],
            "body_mass_g": [3750.0, 5200.0, 3325.0],
            "sex": ["MALE", "FEMALE", "FEMALE"],
        }
    ).set_index("tag_number")


@pytest.fixture(scope="session")
def missing_values_penguins_df():
    """Additional data matching the missing values penguins dataset"""
    return bpd.DataFrame(
        {
            "culmen_length_mm": [39.5, 38.5, 37.9],
            "culmen_depth_mm": [np.nan, 17.2, 18.1],
            "flipper_length_mm": [np.nan, 181.0, 188.0],
        }
    )


@pytest.fixture(scope="session")
def new_penguins_df(session, new_penguins_pandas_df):
    return session.read_pandas(new_penguins_pandas_df)


@pytest.fixture(scope="session")
def llm_text_pandas_df():
    """Additional data matching the penguins dataset, with a new index"""
    return pd.DataFrame(
        {
            "prompt": [
                "What is BigQuery?",
                "What is BQML?",
                "What is BigQuery DataFrame?",
            ],
        }
    )


@pytest.fixture(scope="session")
def llm_text_df(session, llm_text_pandas_df):
    return session.read_pandas(llm_text_pandas_df)


@pytest.fixture(scope="session")
def penguins_linear_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='linear_reg',
    input_label_cols=['body_mass_g'],
    data_split_method='NO_SPLIT'
) AS
SELECT
  *
FROM
  `{penguins_table_id}`
WHERE
  body_mass_g IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_linear_reg_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_linear_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_logistic_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='logistic_reg',
    input_label_cols=['sex'],
    data_split_method='NO_SPLIT'
) AS SELECT
    *
FROM `{penguins_table_id}`
WHERE
  sex IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_logistic_reg_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_logistic_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_kmeans_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='kmeans',
    num_clusters=3
) AS SELECT
    culmen_length_mm,
    culmen_depth_mm,
    flipper_length_mm,
    sex
FROM `{penguins_table_id}`"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_logistic_reg_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_logistic_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_pca_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    # TODO(garrettwu): Create a shared method to get different types of pretrained models.
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='pca',
    num_principal_components=3
) AS SELECT
    *
FROM `{penguins_table_id}`"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = (
        f"{dataset_id_permanent}.penguins_pca_{hashlib.md5(sql.encode()).hexdigest()}"
    )
    sql = sql.replace("$model_name", model_name)

    try:
        return session.read_gbq_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_pca_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_xgbregressor_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='BOOSTED_TREE_REGRESSOR',
    num_parallel_tree=1,
    booster_type='GBTREE',
    early_stop=True,
    data_split_method='NO_SPLIT',
    subsample=1.0,
    input_label_cols=['body_mass_g']
) AS SELECT
    *
FROM `{penguins_table_id}`
WHERE
  body_mass_g IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_xgbregressor_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_xgbregressor_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


def _get_or_create_arima_plus_model(
    session: bigframes.Session, dataset_id_permanent, sql
) -> str:
    """Internal helper to compute a model name by hasing the given SQL.
    attempst to retreive the model, create it if not exist.
    retursn the fully qualitifed model"""

    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.time_series_arima_plus_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)
    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "time_series_arima_plus_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def time_series_arima_plus_model_name(
    session: bigframes.Session, dataset_id_permanent, time_series_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...).
    This version does not include time_series_id_col."""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='ARIMA_PLUS',
    time_series_timestamp_col = 'parsed_date',
    time_series_data_col = 'total_visits'
) AS SELECT
    parsed_date,
    total_visits
FROM `{time_series_table_id}`"""
    return _get_or_create_arima_plus_model(session, dataset_id_permanent, sql)


@pytest.fixture(scope="session")
def time_series_arima_plus_model_name_w_id(
    session: bigframes.Session, dataset_id_permanent, time_series_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...).
    This version includes time_series_id_col."""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='ARIMA_PLUS',
    time_series_timestamp_col = 'parsed_date',
    time_series_data_col = 'total_visits',
    time_series_id_col = 'id'
) AS SELECT
    *
FROM `{time_series_table_id}`"""
    return _get_or_create_arima_plus_model(session, dataset_id_permanent, sql)


@pytest.fixture(scope="session")
def penguins_xgbclassifier_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type="BOOSTED_TREE_CLASSIFIER",
    num_parallel_tree=1,
    booster_type='GBTREE',
    early_stop=True,
    data_split_method='NO_SPLIT',
    subsample=1.0,
    input_label_cols=['sex']
) AS SELECT
    *
FROM `{penguins_table_id}`
WHERE
  sex IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_classifier_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_classifier_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_randomforest_regressor_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='RANDOM_FOREST_REGRESSOR',
    num_parallel_tree=100,
    early_stop=True,
    data_split_method='NO_SPLIT',
    subsample=0.8,
    input_label_cols=['body_mass_g']
) AS SELECT
    *
FROM `{penguins_table_id}`
WHERE
  body_mass_g IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_randomforest_regressor_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_randomforest_regressor_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def penguins_randomforest_classifier_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type="RANDOM_FOREST_CLASSIFIER",
    num_parallel_tree=100,
    early_stop=True,
    data_split_method='NO_SPLIT',
    subsample=0.8,
    input_label_cols=['sex']
) AS SELECT
    *
FROM `{penguins_table_id}`
WHERE
  sex IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_randomforest_classifier_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_randomforest_classifier_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name


@pytest.fixture(scope="session")
def llm_fine_tune_df_default_index(
    session: bigframes.Session,
) -> bigframes.dataframe.DataFrame:
    training_table_name = "llm_tuning.emotion_classification_train"
    df = session.read_gbq(training_table_name).dropna().head(30)
    prefix = "Please do sentiment analysis on the following text and only output a number from 0 to 5 where 0 means sadness, 1 means joy, 2 means love, 3 means anger, 4 means fear, and 5 means surprise. Text: "
    df["prompt"] = prefix + df["text"]
    df["label"] = df["label"].astype("string")
    return df


@pytest.fixture(scope="session")
def usa_names_grouped_table(
    session: bigframes.Session, dataset_id_permanent
) -> bigquery.Table:
    """Provides a table with primary key(s) set."""
    table_id = f"{dataset_id_permanent}.usa_names_grouped"
    try:
        return session.bqclient.get_table(table_id)
    except google.cloud.exceptions.NotFound:
        query = textwrap.dedent(
            f"""
            CREATE TABLE `{dataset_id_permanent}.usa_names_grouped`
            (
                total_people INT64,
                name STRING,
                gender STRING,
                year INT64,
                PRIMARY KEY(name, gender, year) NOT ENFORCED
            )
            AS
            SELECT SUM(`number`) AS total_people, name, gender, year
            FROM `bigquery-public-data.usa_names.usa_1910_2013`
            GROUP BY name, gender, year
            """
        )
        job = session.bqclient.query(query)
        job.result()
        return session.bqclient.get_table(table_id)


@pytest.fixture()
def restore_sampling_settings():
    enable_downsampling = bigframes.options.sampling.enable_downsampling
    max_download_size = bigframes.options.sampling.max_download_size
    yield
    bigframes.options.sampling.enable_downsampling = enable_downsampling
    bigframes.options.sampling.max_download_size = max_download_size


@pytest.fixture()
def with_multiquery_execution():
    original_setting = bigframes.options.compute.enable_multi_query_execution
    bigframes.options.compute.enable_multi_query_execution = True
    yield
    bigframes.options.compute.enable_multi_query_execution = original_setting


@pytest.fixture()
def weird_strings_pd():
    df = pd.DataFrame(
        {
            "string_col": [
                "٠١٢٣٤٥٦٧٨٩",
                "",
                "0",
                "字",
                "五",
                "0123456789",
                pd.NA,
                "abc 123 mixed letters and numbers",
                "no numbers here",
                "123a",
                "23!",
                " 45",
                "a45",
                "ǅ",
                "tT",
                "-123",
                "-123.4",
                "-0",
                "-.0",
                ".0",
                ".1",
                "⅙",
                "²",
                "\t",
                "a\ta",
                "p1\np2",
                "  ",
            ]
        },
        dtype=pd.StringDtype(storage="pyarrow"),
    )
    df.index = df.index.astype("Int64")
    return df.string_col


@pytest.fixture()
def weird_strings(session, weird_strings_pd):
    return session.read_pandas(weird_strings_pd.to_frame()).string_col


@pytest.fixture()
def floats_pd():
    df = pd.DataFrame(
        {
            "float64_col": [
                float("-inf"),
                float("inf"),
                float("nan"),
                float(-234239487.4),
                float(-1.0),
                float(-0.000000001),
                float(0),
                float(0.000000001),
                float(0.9999999999),
                float(1.0),
                float(1.0000001),
                float(math.pi / 2),
                float(math.e),
                float(math.pi),
                float(234239487.4),
                float(1.23124 * (2**70)),
                pd.NA,
            ]
        },
        dtype=pd.Float64Dtype(),
    )
    # Index helps debug failed cases
    df.index = df.float64_col  # type: ignore
    # Upload fails if index name same as column name
    df.index.name = None
    return df.float64_col


@pytest.fixture()
def floats_product_pd(floats_pd):
    df = pd.merge(floats_pd, floats_pd, how="cross")
    # Index helps debug failed cases
    df = df.set_index([df.float64_col_x, df.float64_col_y])  # type: ignore
    df.index.names = ["left", "right"]
    return df


@pytest.fixture()
def floats_bf(session, floats_pd):
    return session.read_pandas(floats_pd.to_frame()).float64_col


@pytest.fixture()
def floats_product_bf(session, floats_product_pd):
    return session.read_pandas(floats_product_pd)


@pytest.fixture(scope="session", autouse=True)
def use_fast_query_path():
    with bpd.option_context("compute.allow_large_results", False):
        yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_cloud_functions(session, cloudfunctions_client, dataset_id_permanent):
    """Clean up stale cloud functions."""
    permanent_endpoints = bigframes.testing.utils.get_remote_function_endpoints(
        session.bqclient, dataset_id_permanent
    )
    delete_count = 0
    try:
        for cloud_function in bigframes.testing.utils.get_cloud_functions(
            cloudfunctions_client,
            session.bqclient.project,
            session.bqclient.location,
            name_prefix="bigframes-",
        ):
            # Ignore bigframes cloud functions referred by the remote functions in
            # the permanent dataset
            if cloud_function.service_config.uri in permanent_endpoints:
                continue

            # Ignore the functions less than one day old
            age = datetime.now() - datetime.fromtimestamp(
                cloud_function.update_time.timestamp()
            )
            if age.days <= 0:
                continue

            # Go ahead and delete
            try:
                bigframes.testing.utils.delete_cloud_function(
                    cloudfunctions_client, cloud_function.name
                )
                delete_count += 1
                if delete_count >= MAX_NUM_FUNCTIONS_TO_DELETE_PER_SESSION:
                    break
            except google.api_core.exceptions.NotFound:
                # This can happen when multiple pytest sessions are running in
                # parallel. Two or more sessions may discover the same cloud
                # function, but only one of them would be able to delete it
                # successfully, while the other instance will run into this
                # exception. Ignore this exception.
                pass
    except Exception as exc:
        # Don't fail the tests for unknown exceptions.
        #
        # This can happen if we are hitting GCP limits, e.g.
        # google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded
        # for quota metric 'Per project mutation requests' and limit
        # 'Per project mutation requests per minute per region' of service
        # 'cloudfunctions.googleapis.com' for consumer
        # 'project_number:1084210331973'.
        # [reason: "RATE_LIMIT_EXCEEDED" domain: "googleapis.com" ...
        #
        # It can also happen occasionally with
        # google.api_core.exceptions.ServiceUnavailable when there is some
        # backend flakiness.
        #
        # Let's stop further clean up and leave it to later.
        traceback.print_exception(type(exc), exc, None)


@pytest.fixture(scope="session")
def images_gcs_path() -> str:
    return "gs://bigframes_blob_test/images/*"


@pytest.fixture(scope="session")
def images_uris() -> list[str]:
    return [
        "gs://bigframes_blob_test/images/img0.jpg",
        "gs://bigframes_blob_test/images/img1.jpg",
    ]


@pytest.fixture(scope="session")
def images_mm_df(
    images_uris, session: bigframes.Session, bq_connection: str
) -> bpd.DataFrame:
    blob_series = bpd.Series(images_uris, session=session).str.to_blob(
        connection=bq_connection
    )
    return blob_series.rename("blob_col").to_frame()


@pytest.fixture()
def reset_default_session_and_location():
    bpd.close_session()
    with bpd.option_context("bigquery.location", None):
        yield
    bpd.close_session()
    bpd.options.bigquery.location = None


@pytest.fixture(scope="session")
def pdf_gcs_path() -> str:
    return "gs://bigframes_blob_test/pdfs/*"


@pytest.fixture(scope="session")
def pdf_mm_df(
    pdf_gcs_path, session: bigframes.Session, bq_connection: str
) -> bpd.DataFrame:
    return session.from_glob_path(pdf_gcs_path, name="pdf", connection=bq_connection)


@pytest.fixture(scope="session")
def audio_gcs_path() -> str:
    return "gs://bigframes_blob_test/audio/*"


@pytest.fixture(scope="session")
def audio_mm_df(
    audio_gcs_path, session: bigframes.Session, bq_connection: str
) -> bpd.DataFrame:
    return session.from_glob_path(
        audio_gcs_path, name="audio", connection=bq_connection
    )
