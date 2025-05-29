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

import pandas as pd

import bigframes
import bigframes.pandas as bpd


def test_blob_create_from_uri_str(
    bq_connection: str, session: bigframes.Session, images_uris
):
    uri_series = bpd.Series(images_uris, session=session)
    blob_series = uri_series.str.to_blob(connection=bq_connection)

    pd_blob_df = blob_series.struct.explode().to_pandas()
    expected_pd_df = pd.DataFrame(
        {
            "uri": images_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )

    pd.testing.assert_frame_equal(
        pd_blob_df, expected_pd_df, check_dtype=False, check_index_type=False
    )


def test_blob_create_from_glob_path(
    bq_connection: str, session: bigframes.Session, images_gcs_path, images_uris
):
    blob_df = session.from_glob_path(
        images_gcs_path, connection=bq_connection, name="blob_col"
    )
    pd_blob_df = (
        blob_df["blob_col"]
        .struct.explode()
        .to_pandas()
        .sort_values("uri")
        .reset_index(drop=True)
    )

    expected_df = pd.DataFrame(
        {
            "uri": images_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )

    pd.testing.assert_frame_equal(
        pd_blob_df, expected_df, check_dtype=False, check_index_type=False
    )


def test_blob_create_read_gbq_object_table(
    bq_connection: str, session: bigframes.Session, images_gcs_path, images_uris
):
    obj_table = session._create_object_table(images_gcs_path, bq_connection)

    blob_df = session.read_gbq_object_table(obj_table, name="blob_col")
    pd_blob_df = (
        blob_df["blob_col"]
        .struct.explode()
        .to_pandas()
        .sort_values("uri")
        .reset_index(drop=True)
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )

    pd.testing.assert_frame_equal(
        pd_blob_df, expected_df, check_dtype=False, check_index_type=False
    )
